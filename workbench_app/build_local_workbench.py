import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT / "transcript_repo"
ITEMS_DIR = REPO / "items"
EDITORIAL_DIR = REPO / "editorial" / "daily"
OUTPUT = ROOT / "workbench.html"
LEGACY_OUTPUT = ROOT / "本地工作台.html"

TODAY = datetime.now().date().isoformat()

CATEGORY_DEFAULTS = [
    ("skill_tools", "Skill / 工具"),
    ("ai_knowledge", "AI领域知识"),
    ("ops_content", "运营与内容"),
    ("work_efficiency", "职场效率"),
    ("personal_growth", "个人成长"),
    ("packaging_reference", "包装参考"),
    ("uncategorized", "待分类"),
]

VALUE_LABELS = [
    "需求证据",
    "知识线索",
    "包装参考",
    "表达参考",
    "证据素材",
    "补充已有主题",
    "仅保留",
]

NEXT_ACTIONS = {
    "merge_demand": "合并需求",
    "add_knowledge": "进入知识核查",
    "save_packaging": "保存包装",
    "save_evidence": "保存证据",
    "enter_topic": "进入选题",
    "deep_research": "深度研究",
    "manual_review": "人工判断",
    "archive": "归档",
}


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def value_to_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return "；".join(value_to_text(item) for item in value if value_to_text(item))
    if isinstance(value, dict):
        for key in ("name", "label", "value", "text", "title", "canonical_name", "statement"):
            if value.get(key):
                return value_to_text(value[key])
        return "；".join(value_to_text(item) for item in value.values() if value_to_text(item))
    return str(value).strip()


def as_list(value):
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [item for item in value if item not in (None, "")]
    return [value]


def split_terms(value):
    raw = [value_to_text(item) for item in value] if isinstance(value, list) else re.split(r"[;；、，,\n]+", value_to_text(value))
    out = []
    seen = set()
    for item in raw:
        text = item.strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def normalize_key(value):
    text = re.sub(r"\s+", "", value_to_text(value)).lower()
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", text)


def strip_frontmatter(markdown):
    text = markdown.strip()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text


def excerpt(text, limit=150):
    compact = re.sub(r"\s+", " ", value_to_text(text)).strip()
    return compact[:limit] + ("..." if len(compact) > limit else "")


def date_only(value):
    text = value_to_text(value)
    match = re.search(r"\d{4}-\d{1,2}-\d{1,2}", text)
    return match.group(0) if match else text


def first_value(*values):
    for value in values:
        if value not in (None, ""):
            return value
    return ""


def extract_last_json_block(markdown):
    if not markdown.strip():
        return {}, "analysis.md 为空或不存在"
    blocks = re.findall(r"```(?:json)?\s*([\s\S]*?)```", markdown, flags=re.I)
    if not blocks:
        return {}, "没有找到 JSON 代码块"
    last_error = ""
    for raw in reversed(blocks):
        candidate = raw.strip()
        if not candidate.startswith("{"):
            continue
        try:
            return json.loads(candidate), ""
        except json.JSONDecodeError as exc:
            last_error = f"JSON 解析失败：第 {exc.lineno} 行第 {exc.colno} 列，{exc.msg}"
    return {}, last_error or "没有找到合法 JSON 对象"


def category_from(value):
    text = value_to_text(value)
    if text in dict(CATEGORY_DEFAULTS):
        return text, dict(CATEGORY_DEFAULTS)[text]
    label_map = {label: key for key, label in CATEGORY_DEFAULTS}
    if text in label_map:
        return label_map[text], text
    lower = text.lower()
    if any(word in lower for word in ("skill", "工具", "插件", "agent")):
        return "skill_tools", "Skill / 工具"
    if "ai" in lower or "模型" in text:
        return "ai_knowledge", "AI领域知识"
    if "运营" in text or "内容" in text or "小红书" in text:
        return "ops_content", "运营与内容"
    if "职场" in text or "效率" in text:
        return "work_efficiency", "职场效率"
    if "成长" in text:
        return "personal_growth", "个人成长"
    if "封面" in text or "标题" in text or "包装" in text:
        return "packaging_reference", "包装参考"
    return "uncategorized", "待分类"


def ingestion_source(meta):
    source = value_to_text(meta.get("ingestion_source") or meta.get("source") or meta.get("collection_source"))
    if source:
        source_lower = source.lower()
        if "feishu" in source_lower or "飞书" in source:
            return "feishu"
        if "qiangua" in source_lower or "千瓜" in source:
            return "qiangua"
        if "manual" in source_lower or "手动" in source:
            return "manual"
        return source_lower
    if meta.get("record_id"):
        return "feishu"
    return "unknown"


def source_label(source):
    return {
        "feishu": "飞书",
        "qiangua": "千瓜",
        "manual": "手动",
        "unknown": "未知来源",
    }.get(source, source or "未知来源")


def cover_for(item_dir, meta):
    cover = first_value(
        meta.get("cover_url"),
        meta.get("cover_image"),
        meta.get("cover"),
        meta.get("thumbnail"),
        meta.get("thumbnail_url"),
        meta.get("local_cover"),
    )
    local_cover = ROOT / "covers" / f"{item_dir.name}.jpg"
    if local_cover.exists():
        return local_cover.relative_to(ROOT).as_posix()
    return value_to_text(cover)


def metric_dict(meta):
    return {
        "likes": meta.get("likes", ""),
        "collects": meta.get("collects", ""),
        "comments": meta.get("comments", ""),
        "shares": meta.get("shares", ""),
    }


def map_status(value):
    text = value_to_text(value)
    if text in ("tested", "已实测"):
        return "已实测"
    if text in ("source_confirmed", "confirmed", "已找到来源"):
        return "已找到来源"
    if text in ("pending_source", "pending", "mentioned", "仅提及"):
        return "仅提及"
    return text or "仅提及"


def map_v2_knowledge(candidate):
    source_urls = []
    for evidence in as_list(candidate.get("evidence")):
        if isinstance(evidence, dict) and evidence.get("url"):
            source_urls.append(evidence["url"])
    return {
        "canonical_name": value_to_text(candidate.get("canonical_name")),
        "knowledge_group": "skill_library" if "skill" in value_to_text(candidate.get("asset_type")).lower() else "knowledge",
        "asset_type": value_to_text(candidate.get("asset_type") or "knowledge"),
        "one_liner": value_to_text(candidate.get("direct_value") or candidate.get("user_problem")),
        "material_claim": value_to_text(candidate.get("material_claim") or candidate.get("direct_value")),
        "source_status": map_status(candidate.get("verification_status")),
        "source_urls": source_urls,
        "verification_needed": as_list(candidate.get("next_action")) + as_list(candidate.get("verification_needed")),
        "dedupe_key": value_to_text(candidate.get("dedupe_key") or f"{candidate.get('canonical_name')}|{candidate.get('asset_type')}"),
        "source_material_ids": [],
    }


def map_v3_knowledge(asset):
    return {
        "canonical_name": value_to_text(asset.get("canonical_name") or asset.get("name") or asset.get("title")),
        "knowledge_group": value_to_text(asset.get("knowledge_group") or "knowledge"),
        "asset_type": value_to_text(asset.get("asset_type") or asset.get("type") or "knowledge"),
        "one_liner": value_to_text(asset.get("one_liner") or asset.get("value") or asset.get("summary")),
        "material_claim": value_to_text(asset.get("material_claim") or asset.get("claim") or asset.get("summary")),
        "source_status": map_status(asset.get("source_status") or asset.get("verification_status")),
        "source_urls": as_list(asset.get("source_urls") or asset.get("urls")),
        "verification_needed": as_list(asset.get("verification_needed") or asset.get("next_action")),
        "dedupe_key": value_to_text(asset.get("dedupe_key") or asset.get("canonical_name") or asset.get("name")),
        "source_material_ids": [],
    }


def map_v2_topic(pack):
    if not isinstance(pack, dict) or not pack:
        return {}
    status = value_to_text(pack.get("status"))
    current_status = "待研究" if status == "needs_evidence" else "可制作" if status == "ready" else "需求发现"
    return {
        "should_enter_pool": status in ("ready", "needs_evidence"),
        "user_problem": value_to_text(pack.get("user_task") or pack.get("user_worry")),
        "why_worth_testing": value_to_text(pack.get("core_conclusion") or pack.get("market_evidence")),
        "current_status": current_status,
        "answer_gap": value_to_text(pack.get("content_gap") or pack.get("missing_information")),
        "production_cost": value_to_text(pack.get("production_fit") or "需要补证据后再估算"),
        "next_step": "补证据" if status == "needs_evidence" else "制作门禁检查",
        "raw_package": pack,
    }


def parse_analysis_schema(analysis, schema_version):
    if schema_version == "4.1":
        return {
            "cardValue": value_to_text(analysis.get("card_value")),
            "summary": value_to_text(analysis.get("summary")),
            "primaryCategory": value_to_text(analysis.get("primary_category")),
            "categoryLabel": value_to_text(analysis.get("category_label")),
            "analysisDepth": value_to_text(analysis.get("analysis_depth") or "light"),
            "useModes": split_terms(analysis.get("use_modes")),
            "demandSignal": analysis.get("demand_signal") if isinstance(analysis.get("demand_signal"), dict) else {},
            "knowledgeLeads": as_list(analysis.get("knowledge_leads")),
            "contentInsight": analysis.get("content_insight") if isinstance(analysis.get("content_insight"), dict) else {},
            "creatorTransfer": analysis.get("creator_transfer") if isinstance(analysis.get("creator_transfer"), dict) else {},
            "topicOpportunity": analysis.get("topic_opportunity") if isinstance(analysis.get("topic_opportunity"), dict) else {},
            "nextAction": analysis.get("next_action") if isinstance(analysis.get("next_action"), dict) else {},
        }
    if schema_version == "3.0":
        topic_seed = {}
        for seed in as_list(analysis.get("topic_seeds")):
            if isinstance(seed, dict):
                topic_seed = seed
                break
        viral = analysis.get("viral_replication") if isinstance(analysis.get("viral_replication"), dict) else {}
        return {
            "cardValue": value_to_text(analysis.get("card_value") or analysis.get("summary")),
            "summary": value_to_text(analysis.get("summary")),
            "primaryCategory": value_to_text(analysis.get("primary_category")),
            "categoryLabel": value_to_text(analysis.get("category_label")),
            "analysisDepth": "light",
            "useModes": split_terms(analysis.get("use_modes")),
            "demandSignal": {
                "statement": value_to_text(topic_seed.get("user_problem") or topic_seed.get("topic") or analysis.get("summary")),
                "evidence": as_list(topic_seed.get("evidence")),
                "answer_gap": value_to_text(topic_seed.get("answer_gap") or "旧 V3 候选需求，需重新判断"),
                "confidence": "low",
            } if topic_seed else {},
            "knowledgeLeads": [map_v3_knowledge(asset) for asset in as_list(analysis.get("knowledge_assets")) if isinstance(asset, dict)],
            "contentInsight": viral,
            "creatorTransfer": {},
            "topicOpportunity": {
                "should_enter_pool": bool(topic_seed),
                "user_problem": value_to_text(topic_seed.get("user_problem") or topic_seed.get("topic")),
                "why_worth_testing": value_to_text(topic_seed.get("why") or "V3 候选需求，需重新判断"),
                "current_status": "需求发现",
                "answer_gap": value_to_text(topic_seed.get("answer_gap") or "需重新判断"),
            } if topic_seed else {},
            "nextAction": {"action": "manual_review", "reason": "V3 旧结构需要人工复核"},
        }
    if schema_version == "2.0":
        knowledge = []
        for candidate in as_list(analysis.get("knowledge_candidates")):
            if isinstance(candidate, dict) and value_to_text(candidate.get("admission")) in ("formal", "pending"):
                knowledge.append(map_v2_knowledge(candidate))
        topic = map_v2_topic(analysis.get("topic_package"))
        return {
            "cardValue": value_to_text(analysis.get("card_value") or analysis.get("summary")),
            "summary": value_to_text(analysis.get("summary")),
            "primaryCategory": value_to_text(analysis.get("primary_topic")),
            "categoryLabel": value_to_text(analysis.get("primary_topic")),
            "analysisDepth": "light",
            "useModes": split_terms(analysis.get("use_modes")),
            "demandSignal": {
                "statement": value_to_text(topic.get("user_problem")),
                "evidence": as_list(analysis.get("source_intent")),
                "answer_gap": value_to_text(topic.get("answer_gap")),
                "confidence": "medium",
            } if topic else {},
            "knowledgeLeads": knowledge,
            "contentInsight": {
                "original_title": value_to_text(analysis.get("title_analysis")),
                "cover_expression": value_to_text(analysis.get("rewrite_cover")),
                "title_cover_roles": value_to_text(analysis.get("reference_logic")),
                "click_or_stop_reason": value_to_text(analysis.get("viral_points")),
                "strongest_transferable_points": as_list(analysis.get("expression_assets")),
                "non_transferable_points": [],
                "promise_delivered": "unknown",
            },
            "creatorTransfer": {
                "new_capability": value_to_text(analysis.get("rewrite_user_value") or analysis.get("reference_logic")),
                "readiness": "needs_rejudge",
                "missing_pieces": as_list((analysis.get("topic_package") or {}).get("missing_information")) if isinstance(analysis.get("topic_package"), dict) else [],
                "production_fit": value_to_text(topic.get("production_cost")),
            },
            "topicOpportunity": topic,
            "nextAction": {"action": "add_knowledge", "reason": "V2 结构已映射，需按 V4.1 复核"},
        }
    return {
        "cardValue": value_to_text(analysis.get("card_value") or analysis.get("summary")),
        "summary": value_to_text(analysis.get("summary")),
        "primaryCategory": value_to_text(analysis.get("primary_topic")),
        "categoryLabel": value_to_text(analysis.get("primary_topic")),
        "analysisDepth": "legacy",
        "useModes": split_terms(analysis.get("use_modes")),
        "demandSignal": {},
        "knowledgeLeads": [],
        "contentInsight": {},
        "creatorTransfer": {},
        "topicOpportunity": {},
        "nextAction": {"action": "manual_review", "reason": "旧分析没有 schema_version，只安全展示，不自动升级"},
    }


def parse_material(item_dir):
    meta = read_json(item_dir / "meta.json")
    transcript = strip_frontmatter(read_text(item_dir / "transcript.md"))
    analysis_md = read_text(item_dir / "analysis.md")
    analysis, parse_error = extract_last_json_block(analysis_md)
    schema_version = value_to_text(analysis.get("schema_version")) if analysis else ""
    if not schema_version and analysis:
        schema_version = "legacy"
    mapped = parse_analysis_schema(analysis, schema_version)
    primary_category, category_label = category_from(mapped.get("primaryCategory") or mapped.get("categoryLabel"))
    if mapped.get("categoryLabel"):
        category_label = value_to_text(mapped["categoryLabel"])
    source = ingestion_source(meta)
    exported_at = date_only(meta.get("exported_at"))
    collected_at = date_only(meta.get("collected_at") or meta.get("captured_at") or exported_at)
    title = value_to_text(meta.get("title") or item_dir.name)
    next_action = mapped.get("nextAction") or {}
    action = value_to_text(next_action.get("action")) or ("manual_review" if parse_error else "archive")
    if action not in NEXT_ACTIONS:
        action = "manual_review"
    use_modes = mapped.get("useModes") or []
    value_tags = []
    mode_map = {
        "demand_signal": "需求证据",
        "knowledge_lead": "知识线索",
        "packaging_reference": "包装参考",
        "expression_reference": "表达参考",
        "evidence_material": "证据素材",
        "supplement_existing_topic": "补充已有主题",
        "material_only": "仅保留",
        "viral_reference": "包装参考",
    }
    for mode in use_modes:
        value_tags.append(mode_map.get(mode, mode if mode in VALUE_LABELS else "知识线索"))
    if not value_tags and parse_error:
        value_tags = ["仅保留"]
    if not value_tags:
        value_tags = ["知识线索"] if mapped.get("knowledgeLeads") else ["仅保留"]
    return {
        "id": item_dir.name,
        "kind": "material",
        "recordId": value_to_text(meta.get("record_id")),
        "sourceUrl": value_to_text(meta.get("source_url")),
        "ingestionSource": source,
        "ingestionSourceLabel": source_label(source),
        "platform": value_to_text(meta.get("platform") or "未知平台"),
        "collectedAt": collected_at,
        "exportedAt": exported_at,
        "publishedAt": date_only(meta.get("published_at")),
        "cover": cover_for(item_dir, meta),
        "title": title,
        "author": value_to_text(meta.get("author")),
        "authorHome": value_to_text(meta.get("author_home")),
        "metrics": metric_dict(meta),
        "durationSeconds": meta.get("duration_seconds", ""),
        "status": value_to_text(meta.get("status")),
        "transcript": transcript,
        "transcriptExcerpt": excerpt(transcript, 260),
        "rawAnalysisMarkdown": analysis_md,
        "schemaVersion": schema_version or "missing",
        "primaryCategory": primary_category,
        "categoryLabel": category_label,
        "tags": split_terms(analysis.get("tags", [])) if analysis else [],
        "summary": mapped.get("summary") or excerpt(transcript, 130) or title,
        "cardValue": mapped.get("cardValue") or mapped.get("summary") or title,
        "analysisDepth": mapped.get("analysisDepth") or "light",
        "useModes": use_modes,
        "valueTags": list(dict.fromkeys(value_tags)),
        "demandSignal": mapped.get("demandSignal") or {},
        "knowledgeLeads": mapped.get("knowledgeLeads") or [],
        "contentInsight": mapped.get("contentInsight") or {},
        "creatorTransfer": mapped.get("creatorTransfer") or {},
        "topicOpportunity": mapped.get("topicOpportunity") or {},
        "nextAction": {
            "action": action,
            "label": NEXT_ACTIONS[action],
            "reason": value_to_text(next_action.get("reason")) or ("缺少结构化分析，需人工判断" if parse_error else ""),
        },
        "parseError": parse_error,
        "isArchived": action == "archive" or "仅保留" in value_tags,
    }


def source_key(material):
    return value_to_text(material.get("sourceUrl")).strip().lower() or normalize_key(material.get("title") + material.get("author"))


def dedupe_materials(materials):
    grouped = defaultdict(list)
    for material in materials:
        grouped[source_key(material)].append(material)
    output = []
    for group in grouped.values():
        primary = sorted(group, key=lambda x: (not x.get("parseError"), x.get("schemaVersion") == "4.1", bool(x.get("cover"))), reverse=True)[0]
        primary = dict(primary)
        primary["duplicateCount"] = len(group)
        primary["duplicateIds"] = [item["id"] for item in group]
        output.append(primary)
    return sorted(output, key=lambda item: (item.get("publishedAt") or item.get("exportedAt") or "", item.get("id")), reverse=True)


def build_demands(materials):
    demands = {}
    for material in materials:
        signal = material.get("demandSignal") or {}
        statement = value_to_text(signal.get("statement"))
        topic = material.get("topicOpportunity") or {}
        if not statement:
            statement = value_to_text(topic.get("user_problem"))
        if not statement:
            continue
        key = normalize_key(statement)
        if key not in demands:
            demands[key] = {
                "id": f"demand-{len(demands)+1}",
                "kind": "demand",
                "statement": statement,
                "evidence": [],
                "answerGap": value_to_text(signal.get("answer_gap") or topic.get("answer_gap")),
                "confidence": value_to_text(signal.get("confidence") or "medium"),
                "sourceMaterialIds": [],
                "status": value_to_text(topic.get("current_status") or "需求发现"),
            }
        demand = demands[key]
        demand["sourceMaterialIds"].append(material["id"])
        demand["evidence"].extend(value_to_text(item) for item in as_list(signal.get("evidence")) if value_to_text(item))
    return list(demands.values())


def build_knowledge(materials):
    knowledge = {}
    for material in materials:
        for lead in as_list(material.get("knowledgeLeads")):
            if not isinstance(lead, dict):
                continue
            name = value_to_text(lead.get("canonical_name"))
            if not name:
                continue
            asset_type = value_to_text(lead.get("asset_type") or "knowledge")
            key = normalize_key(lead.get("dedupe_key") or f"{name}|{asset_type}")
            if key not in knowledge:
                knowledge[key] = {
                    "id": f"knowledge-{len(knowledge)+1}",
                    "kind": "knowledge",
                    "canonicalName": name,
                    "oneLiner": value_to_text(lead.get("one_liner") or lead.get("direct_value")),
                    "assetType": asset_type,
                    "group": value_to_text(lead.get("knowledge_group") or "knowledge"),
                    "sourceStatus": map_status(lead.get("source_status")),
                    "sourceUrls": [],
                    "verificationNeeded": [],
                    "materialClaims": [],
                    "sourceMaterialIds": [],
                    "updatedAt": material.get("exportedAt") or material.get("collectedAt"),
                }
            row = knowledge[key]
            row["sourceMaterialIds"].append(material["id"])
            row["sourceUrls"].extend(value_to_text(url) for url in as_list(lead.get("source_urls")) if value_to_text(url))
            row["verificationNeeded"].extend(value_to_text(item) for item in as_list(lead.get("verification_needed")) if value_to_text(item))
            claim = value_to_text(lead.get("material_claim"))
            if claim:
                row["materialClaims"].append({"materialId": material["id"], "claim": claim})
            if row["sourceStatus"] == "仅提及" and map_status(lead.get("source_status")) != "仅提及":
                row["sourceStatus"] = map_status(lead.get("source_status"))
    for row in knowledge.values():
        row["sourceMaterialIds"] = list(dict.fromkeys(row["sourceMaterialIds"]))
        row["sourceUrls"] = list(dict.fromkeys(row["sourceUrls"]))
        row["verificationNeeded"] = list(dict.fromkeys(row["verificationNeeded"]))
    return list(knowledge.values())


def build_packaging_references(materials):
    refs = []
    for material in materials:
        insight = material.get("contentInsight") or {}
        if not insight:
            continue
        refs.append({
            "id": f"packaging-{material['id']}",
            "kind": "packagingReference",
            "materialId": material["id"],
            "title": material["title"],
            "cover": material["cover"],
            "originalTitle": value_to_text(insight.get("original_title") or material["title"]),
            "coverExpression": value_to_text(insight.get("cover_expression")),
            "roles": value_to_text(insight.get("title_cover_roles")),
            "stopReason": value_to_text(insight.get("click_or_stop_reason")),
            "transferable": as_list(insight.get("strongest_transferable_points")),
            "nonTransferable": as_list(insight.get("non_transferable_points")),
            "promiseDelivered": value_to_text(insight.get("promise_delivered")),
        })
    return refs


def build_content_projects(materials, demands, knowledge):
    demand_by_statement = {normalize_key(d["statement"]): d for d in demands}
    projects = []
    for material in materials:
        topic = material.get("topicOpportunity") or {}
        if not topic or not topic.get("should_enter_pool"):
            continue
        user_problem = value_to_text(topic.get("user_problem"))
        demand_id = demand_by_statement.get(normalize_key(user_problem), {}).get("id")
        status = value_to_text(topic.get("current_status") or "需求发现")
        ready = status == "可制作"
        projects.append({
            "id": f"project-{material['id']}",
            "kind": "contentProject",
            "title": user_problem or material["title"],
            "demandId": demand_id,
            "sourceMaterialIds": [material["id"]],
            "knowledgeIds": [row["id"] for row in knowledge if material["id"] in row["sourceMaterialIds"]],
            "status": status,
            "whyWorthTesting": value_to_text(topic.get("why_worth_testing")),
            "answerGap": value_to_text(topic.get("answer_gap")),
            "productionCost": value_to_text(topic.get("production_cost") or "需要人工补充制作成本"),
            "nextStep": value_to_text(topic.get("next_step") or material.get("nextAction", {}).get("label")),
            "readyToWrite": ready,
            "rawPackage": topic.get("raw_package") or {},
        })
    return projects


def load_materials():
    if not ITEMS_DIR.exists():
        return []
    return [parse_material(path) for path in sorted(ITEMS_DIR.iterdir()) if path.is_dir() and (path / "meta.json").exists()]


def load_editorial():
    result = {"daily": [], "errors": []}
    if not EDITORIAL_DIR.exists():
        return result
    for path in sorted(EDITORIAL_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data["_file"] = path.name
                result["daily"].append(data)
        except json.JSONDecodeError as exc:
            result["errors"].append(f"{path.name}: 第 {exc.lineno} 行 JSON 解析失败")
    return result


def repo_commit():
    try:
        result = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, encoding="utf-8")
        return result.stdout.strip()
    except Exception:
        return ""


def build_stats(materials, raw_materials):
    sources = Counter(item["ingestionSource"] for item in materials)
    today_by_source = Counter(item["ingestionSource"] for item in materials if item.get("collectedAt") == TODAY)
    platforms = Counter(item["platform"] or "未知平台" for item in materials)
    categories = Counter(item["categoryLabel"] for item in materials)
    return {
        "today": TODAY,
        "total": len(materials),
        "rawTotal": len(raw_materials),
        "duplicatesHidden": max(0, len(raw_materials) - len(materials)),
        "feishu": sources.get("feishu", 0),
        "feishuToday": today_by_source.get("feishu", 0),
        "qiangua": sources.get("qiangua", 0),
        "qianguaToday": today_by_source.get("qiangua", 0),
        "unknown": sources.get("unknown", 0),
        "parseErrors": sum(1 for item in materials if item.get("parseError")),
        "schemaVersions": Counter(item["schemaVersion"] for item in materials).most_common(),
        "platforms": platforms.most_common(),
        "categories": categories.most_common(),
        "builtAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI内容创作工作台</title>
  <style>
    :root{--bg:#f4f7fb;--panel:#fff;--ink:#172033;--muted:#667085;--line:#d8dee8;--soft:#f8fafc;--blue:#1d4ed8;--blue2:#0f766e;--blueSoft:#eff6ff;--green:#16794c;--amber:#a15c07;--red:#b42318;--purple:#6d3fc2}
    *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif;letter-spacing:0}.app{min-height:100vh;display:grid;grid-template-rows:auto 1fr}
    header{background:var(--panel);border-bottom:1px solid var(--line);padding:14px 24px}.head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}.title h1{margin:0;font-size:23px}.title p{margin:5px 0 0;color:var(--muted);font-size:13px}.actions{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:12px;flex-wrap:wrap}.btn{border:1px solid #bfdbfe;background:var(--blueSoft);color:var(--blue);border-radius:8px;padding:8px 11px;font-weight:700;cursor:pointer}.btn.secondary{border-color:var(--line);background:#fff;color:var(--ink)}.btn.danger{border-color:#fecaca;background:#fff5f5;color:var(--red)}.btn:disabled{opacity:.45;cursor:not-allowed}
    .data-strip{display:flex;gap:10px;flex-wrap:wrap;margin-top:11px;font-size:12px;color:var(--muted)}.data-pill{border:1px solid var(--line);background:var(--soft);border-radius:999px;padding:5px 9px;cursor:pointer}.data-pill strong{color:var(--ink)}
    .shell{padding:16px 22px 24px}.today-box{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;margin-bottom:12px}.today-head{display:flex;justify-content:space-between;gap:10px;align-items:center}.today-head h2{font-size:16px;margin:0}.today-list{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:10px}.todo{border:1px solid var(--line);border-radius:8px;padding:10px;background:var(--soft)}.todo h3{font-size:14px;margin:0 0 4px}.todo p{font-size:12px;color:var(--muted);line-height:1.5;margin:0 0 8px}
    .topbar{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:12px}.tabs{display:flex;gap:8px;flex-wrap:wrap}.tab{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:8px;padding:10px 15px;font-size:14px;cursor:pointer}.tab.active{border-color:#93c5fd;background:var(--blueSoft);color:var(--blue);font-weight:800}.search{width:360px;height:40px;border:1px solid var(--line);border-radius:8px;background:#fff;padding:0 12px;font-size:14px}
    .layout{display:grid;grid-template-columns:minmax(760px,1fr)460px;gap:14px;align-items:start}.layout.no-detail{grid-template-columns:1fr}.panel{background:#fff;border:1px solid var(--line);border-radius:8px;padding:16px}.section-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;margin-bottom:12px}.section-head h2{font-size:20px;margin:0}.section-head p{font-size:13px;color:var(--muted);line-height:1.5;margin:6px 0 0}.hint{font-size:12px;color:var(--muted)}
    .split{display:grid;grid-template-columns:190px minmax(0,1fr);gap:12px}.filters{display:grid;gap:7px;align-content:start}.filter-btn{display:flex;justify-content:space-between;gap:8px;width:100%;border:1px solid var(--line);background:#fff;border-radius:8px;padding:9px 10px;cursor:pointer;text-align:left;font-size:13px}.filter-btn.active{border-color:#93c5fd;background:var(--blueSoft);color:var(--blue);font-weight:800}.filter-title{font-size:12px;color:var(--muted);font-weight:800;margin:8px 0 2px}
    .cards,.rows{display:grid;gap:10px}.media-card{border:1px solid var(--line);background:#fff;border-radius:8px;padding:10px;display:grid;grid-template-columns:154px minmax(0,1fr);gap:12px;cursor:pointer}.media-card:hover,.row-card:hover{border-color:#93c5fd}.media-card.active,.row-card.active{border-color:var(--blue);box-shadow:inset 3px 0 0 var(--blue)}.cover{width:154px;aspect-ratio:16/10;border-radius:6px;background:#e9eef5;border:1px solid #d7deea;overflow:hidden;display:grid;place-items:center;color:#667085;text-align:center;font-size:12px}.cover img{width:100%;height:100%;object-fit:cover;display:block}.card-title{font-size:16px;line-height:1.42;margin:0 0 6px;font-weight:800}.card-value{font-size:13px;line-height:1.55;color:#344054;margin:6px 0 0}.meta{display:flex;flex-wrap:wrap;gap:4px 12px;color:var(--muted);font-size:12px;line-height:1.45}.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.chip{border:1px solid var(--line);border-radius:999px;padding:4px 8px;background:#fff;color:#344054;font-size:12px;line-height:1.1}.chip.blue{border-color:#bfdbfe;background:var(--blueSoft);color:var(--blue)}.chip.green{border-color:#bbf7d0;background:#f0fdf4;color:var(--green)}.chip.amber{border-color:#fed7aa;background:#fff7ed;color:var(--amber)}.chip.red{border-color:#fecaca;background:#fff5f5;color:var(--red)}.chip.purple{border-color:#ddd6fe;background:#f5f3ff;color:var(--purple)}
    .row-card{border:1px solid var(--line);background:#fff;border-radius:8px;padding:12px;cursor:pointer}.row-card h3{font-size:16px;line-height:1.45;margin:0 0 5px}.row-card p{font-size:13px;line-height:1.6;color:#475467;margin:5px 0}.grid-2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.grid-3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.mini{border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff}.mini h3{font-size:15px;margin:0 0 8px}.empty,.alert{border:1px dashed var(--line);border-radius:8px;padding:16px;color:var(--muted);background:var(--soft)}.alert{border-color:#fecaca;background:#fff5f5;color:var(--red)}
    .detail{position:sticky;top:14px;max-height:calc(100vh - 100px);overflow:auto}.detail-title{font-size:16px;line-height:1.45;margin:0 0 10px}.detail-tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin:10px 0 12px}.detail-tab{border:1px solid var(--line);background:#fff;border-radius:7px;padding:8px 6px;cursor:pointer;font-size:13px;text-align:center}.detail-tab.active{border-color:#93c5fd;background:var(--blueSoft);color:var(--blue);font-weight:800}.field{border-top:1px solid #e8edf3;padding:11px 0}.field label{display:block;color:var(--muted);font-size:12px;font-weight:800;margin-bottom:5px}.field div{white-space:pre-wrap;font-size:14px;line-height:1.65}details{border-top:1px solid #e8edf3;padding:11px 0}summary{cursor:pointer;color:var(--muted);font-weight:800;font-size:12px}.text-box{margin-top:10px;border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff;max-height:300px;overflow:auto;white-space:pre-wrap;font-size:13px;line-height:1.7}.task-box{width:100%;min-height:220px;border:1px solid var(--line);border-radius:8px;padding:10px;white-space:pre-wrap}
    .form-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.form-grid input,.form-grid textarea,.form-grid select{width:100%;border:1px solid var(--line);border-radius:8px;padding:9px 10px;background:#fff}.form-grid textarea{grid-column:span 2;min-height:84px;resize:vertical}.form-actions{display:flex;gap:8px;align-items:center;margin-top:10px;flex-wrap:wrap}
    @media(max-width:1220px){.layout{grid-template-columns:1fr}.detail{position:static;max-height:none}.split{grid-template-columns:1fr}.today-list,.grid-3{grid-template-columns:1fr}.grid-2,.form-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.search{width:100%}.topbar{align-items:stretch;flex-direction:column}.media-card{grid-template-columns:130px minmax(0,1fr)}.cover{width:130px}}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <div class="head">
        <div class="title"><h1>AI内容创作工作台</h1><p>把外部信息变成自己的知识和原创内容</p></div>
        <div class="actions"><button class="btn" id="syncBtn">同步 GitHub</button><button class="btn secondary" id="exportStateBtn">导出状态</button><label class="btn secondary">导入状态<input id="importStateInput" type="file" accept="application/json" hidden></label><span id="builtAt"></span></div>
      </div>
      <div class="data-strip" id="dataStrip"></div>
    </header>
    <div class="shell">
      <section class="today-box" id="todayBox"></section>
      <div class="topbar"><div class="tabs" id="tabs"></div><input id="search" class="search" placeholder="搜索标题、作者、需求、知识、Skill、工具、选题、来源和平台"></div>
      <div class="layout" id="layout"><main class="panel" id="main"></main><aside class="panel detail" id="detail" hidden></aside></div>
    </div>
  </div>
  <script id="workbench-data" type="application/json">__DATA__</script>
  <script>
    const payload = JSON.parse(document.getElementById('workbench-data').textContent);
    const baseMaterials = payload.objects.materials || [];
    const baseDemands = payload.objects.demands || [];
    const baseKnowledge = payload.objects.knowledge || [];
    const basePackaging = payload.objects.packagingReferences || [];
    const baseProjects = payload.objects.contentProjects || [];
    const editorial = payload.editorial || {daily: [], errors: []};
    const stats = payload.stats || {};
    const stateKey = 'ai-content-workbench-v4.1-state';
    const oldReviewKey = 'short-video-workbench-review-v1';
    const modules = [
      {id:'materials',name:'素材总览'},
      {id:'editorial',name:'AI编辑部'},
      {id:'knowledge',name:'知识库'},
      {id:'topics',name:'选题与学习'},
      {id:'reviews',name:'复盘库'}
    ];
    const categoryDefaults = payload.categoryDefaults || [];
    const valueLabels = payload.valueLabels || [];
    let currentModule = new URLSearchParams(location.search).get('module') || location.hash.replace('#','') || 'materials';
    if(!modules.some(m=>m.id===currentModule)) currentModule='materials';
    let currentCategory = '全部';
    let currentValue = '全部';
    let currentSource = '全部';
    let currentFilter = '全部';
    let selected = null;
    let detailTab = 'raw';
    let taskText = '';

    function loadState(){
      let state={materialEdits:{},reviews:[],editorialDaily:[],contentProjects:{}};
      try{state={...state,...JSON.parse(localStorage.getItem(stateKey)||'{}')}}catch{}
      if(!state.reviews.length){
        try{state.reviews=JSON.parse(localStorage.getItem(oldReviewKey)||'[]')}catch{}
      }
      return state;
    }
    let state = loadState();
    function saveState(){localStorage.setItem(stateKey, JSON.stringify(state,null,2));}
    function text(value){
      if(value===null||value===undefined)return '';
      if(typeof value==='string')return value.trim();
      if(typeof value==='number'||typeof value==='boolean')return String(value);
      if(Array.isArray(value))return value.map(text).filter(Boolean).join('；');
      if(typeof value==='object'){
        for(const key of ['name','label','value','text','title','canonical_name','statement']) if(value[key]) return text(value[key]);
        return Object.values(value).map(text).filter(Boolean).join('；');
      }
      return String(value).trim();
    }
    function arr(value){if(!value)return[];return Array.isArray(value)?value:[value];}
    function material(item){
      const edit=state.materialEdits[item.id]||{};
      return {...item,...edit,metrics:{...(item.metrics||{}),...(edit.metrics||{})},valueTags:edit.valueTags||item.valueTags||[],tags:edit.tags||item.tags||[]};
    }
    function materials(){return baseMaterials.map(material);}
    function materialById(id){return materials().find(item=>item.id===id)||baseMaterials.find(item=>item.id===id)||{};}
    function itemText(item){return JSON.stringify(item).toLowerCase();}
    function visibleMaterials(){
      const q=document.getElementById('search').value.trim().toLowerCase();
      return materials().filter(item=>{
        if(q && !itemText(item).includes(q)) return false;
        if(currentSource!=='全部' && item.ingestionSource!==currentSource) return false;
        if(currentCategory!=='全部' && item.categoryLabel!==currentCategory) return false;
        if(currentValue!=='全部' && !(item.valueTags||[]).includes(currentValue)) return false;
        if(currentValue!=='仅保留' && item.isArchived && !q) return false;
        return true;
      });
    }
    function chipClass(value){const v=text(value);if(/失败|错误|暂不|缺/.test(v))return'red';if(/已实测|可制作|正式|飞书|需求证据/.test(v))return'green';if(/待|研究|知识|Skill|工具|仅提及/.test(v))return'purple';if(/包装|表达|证据|来源|需/.test(v))return'amber';return'blue'}
    function fmt(n){if(n===null||n===undefined||n==='')return'-';const x=Number(n);if(!Number.isFinite(x))return text(n);return x>=10000?`${(x/10000).toFixed(x>=100000?0:1)}万`:String(x)}
    function escapeHtml(value){return String(value||'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));}
    function escapeAttr(value){return escapeHtml(value).replace(/`/g,'&#96;')}
    function field(label,value){const v=text(value);return v?`<div class="field"><label>${escapeHtml(label)}</label><div>${escapeHtml(v)}</div></div>`:''}

    function renderHeader(){
      document.getElementById('builtAt').textContent=`生成：${stats.builtAt||'-'} · repo ${payload.repoCommit||'-'}`;
      document.getElementById('dataStrip').innerHTML=[
        ['all',`总收录 <strong>${stats.total||0}</strong> 条`],
        ['feishu',`飞书 <strong>${stats.feishu||0}</strong> 条｜今日 +${stats.feishuToday||0}`],
        ['qiangua',`千瓜 <strong>${stats.qiangua||0}</strong> 条｜今日 +${stats.qianguaToday||0}`],
        ['unknown',`未知来源 <strong>${stats.unknown||0}</strong> 条`]
      ].map(([source,label])=>`<button class="data-pill" data-source="${source}">${label}</button>`).join('');
      document.querySelectorAll('[data-source]').forEach(btn=>btn.onclick=()=>{currentSource=btn.dataset.source==='all'?'全部':btn.dataset.source;currentModule='materials';selected=null;render();});
    }
    function todayActions(){
      const actions=[];
      const unparsed=materials().filter(m=>m.parseError&&!m.isArchived);
      if(unparsed.length) actions.push({title:`处理 ${unparsed.length} 条未结构化素材`,desc:'有逐字稿但缺 V4.1 JSON，先判断是否值得分析。',button:'处理素材',module:'materials'});
      const pendingKnowledge=baseKnowledge.filter(k=>k.sourceStatus==='仅提及');
      if(pendingKnowledge.length) actions.push({title:`核查 ${pendingKnowledge.length} 条知识线索`,desc:'二手提及不能直接变成正式知识，先找来源或实测。',button:'开始核查',module:'knowledge'});
      const notReady=baseProjects.filter(p=>p.status!=='可制作');
      if(notReady.length) actions.push({title:`推进 ${notReady.length} 个需求机会`,desc:'先补证据、学习或实测，未过门禁不生成完整稿。',button:'进入选题',module:'topics'});
      return actions.slice(0,3);
    }
    function renderToday(){
      const actions=todayActions();
      document.getElementById('todayBox').innerHTML=`
        <div class="today-head"><h2>今天先做什么</h2><span class="hint">最多 3 项，避免变成高级收藏夹</span></div>
        ${actions.length?`<div class="today-list">${actions.map(a=>`<div class="todo"><h3>${escapeHtml(a.title)}</h3><p>${escapeHtml(a.desc)}</p><button class="btn secondary" data-jump="${a.module}">${escapeHtml(a.button)}</button></div>`).join('')}</div>`:'<div class="empty" style="margin-top:10px">今天暂无必须处理内容。</div>'}
      `;
      document.querySelectorAll('[data-jump]').forEach(btn=>btn.onclick=()=>{currentModule=btn.dataset.jump;history.replaceState(null,'',`#${currentModule}`);selected=null;render();});
    }
    function renderTabs(){
      document.getElementById('tabs').innerHTML=modules.map(m=>`<button class="tab ${m.id===currentModule?'active':''}" data-module="${m.id}">${m.name}</button>`).join('');
      document.querySelectorAll('[data-module]').forEach(btn=>btn.onclick=()=>{currentModule=btn.dataset.module;history.replaceState(null,'',`#${currentModule}`);selected=null;detailTab='raw';currentFilter='全部';render();});
    }

    function renderMaterials(){
      const list=visibleMaterials();
      const byCategory=countBy(materials().filter(m=>currentValue==='全部'||(m.valueTags||[]).includes(currentValue)),m=>m.categoryLabel||'待分类');
      const byValue=countBy(materials(),m=>m.valueTags||[]);
      if(!selected&&list[0])selected=list[0];
      document.getElementById('main').innerHTML=`
        <div class="section-head"><div><h2>素材总览</h2><p>先判断外部内容对我有什么创作增量；普通素材默认轻分析，每条只有一个主要下一步。</p></div><div class="hint">${list.length} / ${materials().length} 条</div></div>
        ${stats.parseErrors?`<div class="alert" style="margin-bottom:12px">${stats.parseErrors} 条素材缺少合法 JSON，已安全保留，不影响其他内容。</div>`:''}
        <div class="split"><aside class="filters">
          <div class="filter-title">分类</div>${filterButtons(byCategory,currentCategory,'category')}
          <div class="filter-title">价值标签</div>${filterButtons(byValue,currentValue,'value')}
        </aside><section class="cards">${list.length?list.map(renderMaterialCard).join(''):'<div class="empty">当前筛选下没有素材。</div>'}</section></div>
      `;
      bindFilters();bindRows();
    }
    function countBy(list,fn){const map=new Map();for(const item of list){const keys=arr(fn(item));for(const k of keys){const key=text(k)||'未标注';map.set(key,(map.get(key)||0)+1)}}return [['全部',list.length],...[...map.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0],'zh-CN'))]}
    function filterButtons(rows,current,type){return rows.map(([name,count])=>`<button class="filter-btn ${current===name?'active':''}" data-filter-type="${type}" data-filter-value="${escapeAttr(name)}"><span>${escapeHtml(name)}</span><span>${count}</span></button>`).join('')}
    function bindFilters(){document.querySelectorAll('[data-filter-type]').forEach(btn=>btn.onclick=()=>{if(btn.dataset.filterType==='category')currentCategory=btn.dataset.filterValue;else currentValue=btn.dataset.filterValue;selected=null;render();});}
    function renderCover(item){return item.cover?`<img src="${escapeAttr(item.cover)}" alt="">`:`<span>${escapeHtml(item.platform||'素材')}<br>封面待采集</span>`}
    function renderMaterialCard(item){return `<article class="media-card ${selected?.id===item.id?'active':''}" data-kind="material" data-id="${escapeAttr(item.id)}"><div class="cover">${renderCover(item)}</div><div><h3 class="card-title">${escapeHtml(item.title)}</h3><div class="meta"><span>${escapeHtml(item.ingestionSourceLabel)}</span><span>${escapeHtml(item.platform)}</span><span>${escapeHtml(item.author||'未知作者')}</span><span>${escapeHtml(item.publishedAt||'-')}</span><span>赞 ${fmt(item.metrics.likes)}</span><span>藏 ${fmt(item.metrics.collects)}</span><span>评 ${fmt(item.metrics.comments)}</span><span>转 ${fmt(item.metrics.shares)}</span></div><p class="card-value">${escapeHtml(item.cardValue||item.summary)}</p><div class="chips"><span class="chip ${chipClass(item.categoryLabel)}">${escapeHtml(item.categoryLabel)}</span>${(item.valueTags||[]).slice(0,3).map(t=>`<span class="chip ${chipClass(t)}">${escapeHtml(t)}</span>`).join('')}<span class="chip ${chipClass(item.nextAction.label)}">${escapeHtml(item.nextAction.label)}</span>${item.parseError?'<span class="chip red">缺JSON</span>':''}</div></div></article>`}

    function renderEditorial(){
      const imported=state.editorialDaily||[];
      const daily=[...imported,...(editorial.daily||[])];
      const latest=daily[0]||{};
      const items=arr(latest.items||latest.entries||latest.daily||[]);
      const knowledge=items.filter(i=>['knowledge','research'].includes(text(i.recommended_action)));
      const demands=items.filter(i=>['demand','topic'].includes(text(i.recommended_action)));
      document.getElementById('main').innerHTML=`
        <div class="section-head"><div><h2>AI编辑部</h2><p>这里只做信息发现与筛选。AI HOT 是入口，不是最终事实源；进入知识或选题前必须保留原始来源。</p></div><div class="hint">${latest.date||latest._file||'暂无日报'}</div></div>
        <div class="form-actions" style="margin-bottom:12px"><button class="btn" id="aihotTaskBtn">更新AI编辑部</button><label class="btn secondary">导入日报 JSON<input id="editorialImport" type="file" accept="application/json" hidden></label></div>
        ${(editorial.errors||[]).length?`<div class="alert">${editorial.errors.map(escapeHtml).join('<br>')}</div>`:''}
        <div class="grid-2"><section><h2 style="font-size:17px">今日新增知识</h2><div class="rows">${knowledge.length?knowledge.map(renderEditorialRow).join(''):'<div class="empty">暂无已筛选知识。AI HOT 不可用时不影响其他板块。</div>'}</div></section><section><h2 style="font-size:17px">今日需求机会</h2><div class="rows">${demands.length?demands.map(renderEditorialRow).join(''):'<div class="empty">暂无需求机会。没有重要信息时允许为空。</div>'}</div></section></div>
        ${taskText?renderTaskPanel():''}
      `;
      document.getElementById('aihotTaskBtn').onclick=()=>{taskText=makeAihotTask();render();};
      document.getElementById('editorialImport').onchange=importEditorial;
    }
    function renderEditorialRow(row){return `<article class="row-card"><h3>${escapeHtml(text(row.title))}</h3><p>${escapeHtml(text(row.summary||row.user_task))}</p><div class="chips"><span class="chip ${chipClass(row.verification_status)}">${escapeHtml(text(row.verification_status||'discovered'))}</span><span class="chip ${chipClass(row.recommended_action)}">${escapeHtml(text(row.recommended_action||'ignore'))}</span>${row.original_url?`<a class="chip blue" href="${escapeAttr(row.original_url)}" target="_blank">原始来源</a>`:''}</div></article>`}

    function renderKnowledge(){
      const filters=['全部','仅提及','已找到来源','已实测'];
      const list=baseKnowledge.filter(k=>currentFilter==='全部'||k.sourceStatus===currentFilter);
      if(!selected&&list[0])selected=list[0];
      document.getElementById('main').innerHTML=`<div class="section-head"><div><h2>知识库</h2><p>可查、可用、持续合并的个人知识清单；同一实体按规范名称和类型合并来源。</p></div><div class="hint">${list.length} / ${baseKnowledge.length} 条知识</div></div><nav class="tabs" style="margin-bottom:12px">${filters.map(f=>`<button class="tab ${currentFilter===f?'active':''}" data-current-filter="${f}">${f}</button>`).join('')}</nav><section class="rows">${list.length?list.map(renderKnowledgeRow).join(''):'<div class="empty">当前没有知识。旧 legacy 不会自动升级为正式知识。</div>'}</section>`;
      bindCurrentFilter();bindRows();
    }
    function renderKnowledgeRow(k){return `<article class="row-card ${selected?.id===k.id?'active':''}" data-kind="knowledge" data-id="${escapeAttr(k.id)}"><h3>${escapeHtml(k.canonicalName)}</h3><p>${escapeHtml(k.oneLiner||'暂无一句话用途')}</p><div class="chips"><span class="chip ${chipClass(k.assetType)}">${escapeHtml(k.assetType)}</span><span class="chip">来源 ${k.sourceMaterialIds.length}</span><span class="chip ${chipClass(k.sourceStatus)}">${escapeHtml(k.sourceStatus)}</span></div></article>`}

    function renderTopics(){
      const statusRows=countBy(baseProjects,p=>p.status||'需求发现');
      const list=baseProjects.filter(p=>currentFilter==='全部'||p.status===currentFilter);
      if(!selected&&list[0])selected=list[0];
      document.getElementById('main').innerHTML=`<div class="section-head"><div><h2>选题与学习</h2><p>先判断需求值不值得做、我现在能不能讲。未过门禁时只生成学习、研究或实测任务。</p></div><div class="hint">${list.length} / ${baseProjects.length} 个机会</div></div><nav class="tabs" style="margin-bottom:12px">${statusRows.map(([s,c])=>`<button class="tab ${currentFilter===s?'active':''}" data-current-filter="${escapeAttr(s)}">${escapeHtml(s)} ${c}</button>`).join('')}</nav><section class="rows">${list.length?list.map(renderProjectRow).join(''):'<div class="empty">目前没有可展示的需求机会。</div>'}</section>`;
      bindCurrentFilter();bindRows();
    }
    function renderProjectRow(p){return `<article class="row-card ${selected?.id===p.id?'active':''}" data-kind="project" data-id="${escapeAttr(p.id)}"><h3>${escapeHtml(p.title)}</h3><p>${escapeHtml(p.answerGap||p.whyWorthTesting||'暂无答案缺口')}</p><div class="chips"><span class="chip ${chipClass(p.status)}">${escapeHtml(p.status)}</span><span class="chip">来源 ${p.sourceMaterialIds.length}</span><span class="chip ${p.readyToWrite?'green':'amber'}">${p.readyToWrite?'可生成创作任务':'未过制作门禁'}</span></div></article>`}
    function bindCurrentFilter(){document.querySelectorAll('[data-current-filter]').forEach(btn=>btn.onclick=()=>{currentFilter=btn.dataset.currentFilter;selected=null;render();});}

    function renderReviews(){
      const list=state.reviews||[];
      document.getElementById('main').innerHTML=`<div class="section-head"><div><h2>复盘库</h2><p>导入或手动记录发布数据，输出四层复盘；少于 10 条只给观察和假设。</p></div><div class="hint">${list.length} 条复盘</div></div>${reviewForm()}<section class="rows" style="margin-top:12px">${list.length?list.map(renderReviewRow).join(''):'<div class="empty">还没有复盘记录。</div>'}</section>`;
      bindReviewForm();
    }
    function reviewForm(){return `<form id="reviewForm" class="mini"><input type="hidden" name="id"><div class="form-grid"><input name="title" placeholder="内容标题 / 项目" required><input name="views" placeholder="观看/阅读"><input name="impressions" placeholder="曝光"><input name="cover_click_rate" placeholder="封面点击率"><input name="likes" placeholder="点赞"><input name="collects" placeholder="收藏"><input name="comments" placeholder="评论"><input name="shares" placeholder="分享"><input name="new_followers" placeholder="新增关注"><input name="avg_watch_ratio" placeholder="平均观看占比"><select name="test_status"><option>标准测试</option><option>非标准测试</option><option>观察样本</option></select><input name="traffic_source" placeholder="流量来源"><textarea name="four_layer" placeholder="四层复盘：需求是否成立 / 包装是否有效 / 内容是否兑现 / 是否形成关注理由"></textarea><textarea name="next_action" placeholder="下次保留什么，只改一个什么，下一条验证什么"></textarea></div><div class="form-actions"><button class="btn" type="submit">保存复盘</button><button class="btn secondary" type="button" id="clearReview">清空</button><button class="btn secondary" type="button" id="exportReviews">导出复盘JSON</button><label class="btn secondary">导入复盘JSON<input id="importReviews" type="file" accept="application/json" hidden></label></div></form>`}
    function renderReviewRow(r){const views=Number(r.views)||0, likes=Number(r.likes)||0, collects=Number(r.collects)||0, shares=Number(r.shares)||0, comments=Number(r.comments)||0, followers=Number(r.new_followers)||0;const collectRate=views?`${(collects/views*100).toFixed(1)}%`:'-';const shareRate=views?`${(shares/views*100).toFixed(1)}%`:'-';const interactRate=views?`${((likes+collects+comments+shares)/views*100).toFixed(1)}%`:'-';const fpk=views?`${(followers/views*1000).toFixed(1)}`:'-';return `<article class="row-card"><h3>${escapeHtml(r.title)}</h3><p>${escapeHtml(r.four_layer||'暂无四层复盘')}</p><div class="chips"><span class="chip">收藏率 ${collectRate}</span><span class="chip">分享率 ${shareRate}</span><span class="chip">互动率 ${interactRate}</span><span class="chip">千次涨粉 ${fpk}</span><span class="chip ${chipClass(r.test_status)}">${escapeHtml(r.test_status||'观察样本')}</span></div><div class="form-actions"><button class="btn secondary" data-review-edit="${escapeAttr(r.id)}">编辑</button><button class="btn danger" data-review-delete="${escapeAttr(r.id)}">删除</button></div></article>`}

    function bindRows(){document.querySelectorAll('[data-kind][data-id]').forEach(row=>row.onclick=()=>{selected=findRecord(row.dataset.kind,row.dataset.id);detailTab='raw';taskText='';render();});}
    function findRecord(kind,id){if(kind==='material')return materials().find(m=>m.id===id);if(kind==='knowledge')return baseKnowledge.find(k=>k.id===id);if(kind==='project')return baseProjects.find(p=>p.id===id);return null}
    function renderDetail(){
      const root=document.getElementById('detail'), layout=document.getElementById('layout');
      if(!selected||currentModule==='editorial'||currentModule==='reviews'){root.hidden=true;layout.classList.add('no-detail');root.innerHTML='';return}
      root.hidden=false;layout.classList.remove('no-detail');
      if(selected.kind==='knowledge') return renderKnowledgeDetail(selected);
      if(selected.kind==='contentProject') return renderProjectDetail(selected);
      renderMaterialDetail(selected);
    }
    function tabs(rows){return `<div class="detail-tabs">${rows.map(([id,label])=>`<button class="detail-tab ${detailTab===id?'active':''}" data-detail-tab="${id}">${label}</button>`).join('')}</div>`}
    function bindDetailTabs(){document.querySelectorAll('[data-detail-tab]').forEach(btn=>btn.onclick=()=>{detailTab=btn.dataset.detailTab;taskText='';renderDetail();});}
    function renderMaterialDetail(item){
      const root=document.getElementById('detail');
      const tabRows=[['raw','原始材料'],['demand','用户需求'],['knowledge','知识与包装'],['transfer','创作增量']];
      if(!tabRows.some(([id])=>id===detailTab))detailTab='raw';
      let body='';
      if(detailTab==='raw')body=`${item.parseError?`<div class="alert">${escapeHtml(item.parseError)}</div>`:''}${editMaterialBox(item)}${field('一句话内容',item.summary)}<details><summary>逐字稿</summary><button class="btn secondary" onclick="copyTextById('transcript-${escapeAttr(item.id)}')">复制逐字稿</button><div class="text-box" id="transcript-${escapeAttr(item.id)}">${escapeHtml(item.transcript||'暂无逐字稿')}</div></details><details><summary>原 Markdown / 旧分析</summary><div class="text-box">${escapeHtml(item.rawAnalysisMarkdown||'暂无 analysis.md')}</div></details>`;
      if(detailTab==='demand')body=`${field('核心需求',item.demandSignal?.statement)}${field('需求证据',item.demandSignal?.evidence)}${field('最大答案缺口',item.demandSignal?.answer_gap)}${field('置信度',item.demandSignal?.confidence)}${!item.demandSignal?.statement?'<div class="empty">这条素材没有结构化需求。旧素材不会被自动升级。</div>':''}`;
      if(detailTab==='knowledge')body=`${renderKnowledgeLeads(item)}${renderPackagingForMaterial(item)}`;
      if(detailTab==='transfer')body=`${field('新增能力 / 创作增量',item.creatorTransfer?.new_capability)}${field('当前准备状态',item.creatorTransfer?.readiness)}${field('需要补充',item.creatorTransfer?.missing_pieces)}${field('制作适配',item.creatorTransfer?.production_fit)}${field('主要下一步',`${item.nextAction.label}：${item.nextAction.reason||''}`)}<button class="btn secondary" id="deepTaskBtn">生成深度分析任务包</button>${taskText?renderTaskPanel():''}`;
      root.innerHTML=`<h2 class="detail-title">${escapeHtml(item.title)}</h2><div class="chips">${item.sourceUrl?`<a class="chip blue" href="${escapeAttr(item.sourceUrl)}" target="_blank">打开原链接</a>`:''}<span class="chip ${chipClass(item.ingestionSourceLabel)}">${escapeHtml(item.ingestionSourceLabel)}</span><span class="chip ${chipClass(item.schemaVersion)}">${escapeHtml(item.schemaVersion)}</span><span class="chip ${chipClass(item.nextAction.label)}">${escapeHtml(item.nextAction.label)}</span></div>${tabs(tabRows)}${body||'<div class="empty">没有可展示内容。</div>'}`;
      bindDetailTabs();
      const btn=document.getElementById('deepTaskBtn'); if(btn) btn.onclick=()=>{taskText=makeCosmosTask(item);renderDetail();};
    }
    function editMaterialBox(item){return `<details><summary>人工修改分类 / 价值标签 / 来源 / 下一步</summary><div class="form-grid" style="margin-top:10px"><select id="editCategory">${categoryDefaults.map(([key,label])=>`<option value="${escapeAttr(label)}" ${item.categoryLabel===label?'selected':''}>${escapeHtml(label)}</option>`).join('')}</select><select id="editSource"><option value="feishu" ${item.ingestionSource==='feishu'?'selected':''}>飞书</option><option value="qiangua" ${item.ingestionSource==='qiangua'?'selected':''}>千瓜</option><option value="manual" ${item.ingestionSource==='manual'?'selected':''}>手动</option><option value="unknown" ${item.ingestionSource==='unknown'?'selected':''}>未知来源</option></select><select id="editNext">${Object.entries(payload.nextActions).map(([key,label])=>`<option value="${key}" ${item.nextAction.action===key?'selected':''}>${label}</option>`).join('')}</select><input id="editTags" value="${escapeAttr((item.valueTags||[]).join('；'))}" placeholder="价值标签，用分号分隔"></div><div class="form-actions"><button class="btn secondary" onclick="saveMaterialEdit('${escapeAttr(item.id)}')">保存修改</button></div></details>`}
    function saveMaterialEdit(id){const item=materialById(id);const category=document.getElementById('editCategory').value;const source=document.getElementById('editSource').value;const next=document.getElementById('editNext').value;const tags=document.getElementById('editTags').value.split(/[；;、，,]/).map(s=>s.trim()).filter(Boolean);state.materialEdits[id]={...(state.materialEdits[id]||{}),categoryLabel:category,ingestionSource:source,ingestionSourceLabel:{feishu:'飞书',qiangua:'千瓜',manual:'手动',unknown:'未知来源'}[source]||source,valueTags:tags,nextAction:{action:next,label:payload.nextActions[next],reason:'人工修改'}};saveState();selected=material(item);render();}
    window.saveMaterialEdit=saveMaterialEdit;
    function renderKnowledgeLeads(item){const list=arr(item.knowledgeLeads);if(!list.length)return'<div class="empty">没有可提取知识。</div>';return `<h3 style="font-size:15px">可提取知识</h3>`+list.slice(0,3).map(k=>`<div class="mini" style="margin-top:8px"><h3>${escapeHtml(text(k.canonical_name))}</h3>${field('一句话用途',k.one_liner)}${field('素材中说了什么',k.material_claim)}${field('状态',k.source_status)}${field('下一步核查',k.verification_needed)}</div>`).join('')}
    function renderPackagingForMaterial(item){const ref=basePackaging.find(r=>r.materialId===item.id);if(!ref)return'<div class="empty" style="margin-top:10px">没有包装与表达参考。</div>';return `<h3 style="font-size:15px;margin-top:14px">包装与表达</h3>${field('标题封面分工',ref.roles)}${field('点击/停下理由',ref.stopReason)}${field('可迁移点',ref.transferable)}${field('不能照搬',ref.nonTransferable)}${field('承诺兑现',ref.promiseDelivered)}`}
    function renderKnowledgeDetail(k){document.getElementById('detail').innerHTML=`<h2 class="detail-title">${escapeHtml(k.canonicalName)}</h2><div class="chips"><span class="chip ${chipClass(k.sourceStatus)}">${escapeHtml(k.sourceStatus)}</span><span class="chip">${escapeHtml(k.assetType)}</span><span class="chip">来源 ${k.sourceMaterialIds.length}</span></div>${field('它是什么 / 解决什么',k.oneLiner)}${field('素材说法',k.materialClaims?.map(x=>x.claim))}${field('原始来源',k.sourceUrls)}${field('下一步核查',k.verificationNeeded)}${field('关联素材',k.sourceMaterialIds.map(id=>materialById(id).title))}`;}
    function renderProjectDetail(p){const source=p.sourceMaterialIds.map(id=>materialById(id));const ready=p.readyToWrite;const saved=(state.contentProjects[p.id]||{}).returnResult||'';document.getElementById('detail').innerHTML=`<h2 class="detail-title">${escapeHtml(p.title)}</h2><div class="chips"><span class="chip ${chipClass(p.status)}">${escapeHtml(p.status)}</span><span class="chip ${ready?'green':'amber'}">${ready?'已过制作门禁':'未过制作门禁'}</span></div>${field('需求证据',source.map(s=>s.title))}${field('答案缺口',p.answerGap)}${field('当前准备状态',p.status)}${field('预计制作成本',p.productionCost)}${field('下一步',p.nextStep)}<div class="form-actions"><button class="btn secondary" id="hvTaskBtn">生成深度研究任务包</button><button class="btn secondary" id="titleTaskBtn">标题任务包</button><button class="btn secondary" id="coverTaskBtn">封面任务包</button><button class="btn" id="writeTaskBtn" ${ready?'':'disabled'}>正式创作任务包</button></div>${!ready?'<div class="empty" style="margin-top:10px">未通过制作门禁：只生成学习、研究或实测任务，不生成完整稿。</div>':''}${taskText?renderTaskPanel():''}<details open><summary>导入返回结果 / 保存为内容项目</summary><textarea class="task-box" id="projectReturn" placeholder="把 GPT 或 Codex 返回的正文、标题、封面方案粘贴到这里。">${escapeHtml(saved)}</textarea><div class="form-actions"><button class="btn secondary" id="saveProjectReturn">保存返回结果</button></div>${saved?field('已保存返回结果',saved):''}</details>`;document.getElementById('hvTaskBtn').onclick=()=>{taskText=makeHvTask(p);renderProjectDetail(p)};document.getElementById('titleTaskBtn').onclick=()=>{taskText=makeTitleTask(p);renderProjectDetail(p)};document.getElementById('coverTaskBtn').onclick=()=>{taskText=makeCoverTask(p);renderProjectDetail(p)};const wb=document.getElementById('writeTaskBtn');if(wb)wb.onclick=()=>{taskText=makeWriteTask(p);renderProjectDetail(p)};document.getElementById('saveProjectReturn').onclick=()=>{state.contentProjects[p.id]={...(state.contentProjects[p.id]||{}),returnResult:document.getElementById('projectReturn').value,savedAt:new Date().toISOString()};saveState();renderProjectDetail(p)};}
    function renderTaskPanel(){return `<div class="field"><label>可复制任务包</label><textarea class="task-box" id="taskText">${escapeHtml(taskText)}</textarea><div class="form-actions"><button class="btn secondary" onclick="copyTextById('taskText')">复制任务包</button></div></div>`}
    function copyTextById(id){const el=document.getElementById(id);const text=el.value||el.textContent; if(navigator.clipboard)navigator.clipboard.writeText(text); else {const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy');}}
    window.copyTextById=copyTextById;

    function makeAihotTask(){return `任务阶段：AI资讯发现\n建议 Skill：aihot\nSkill 来源：https://aihot.virxact.com/aihot-skill/\n用户目标：为“替普通人试 AI、学 AI，把真正能用到工作和内容里的方法讲清楚”的账号发现少量值得进一步研究的信息。\n输入材料：最近 24 小时精选；必要时关键词 Codex / Agent / 小红书 / AI工具\n必须遵守：默认拉精选而不是全量；按账号承诺过滤；打开原始来源核查重要事实；输出 discovered|source_checked|tested；动作只能是 ignore|knowledge|demand|research|topic。\n期望输出：editorial/daily/YYYY-MM-DD.json，字段含 title/category/published_at/aihot_url/original_url/summary/user_task/account_value/verification_status/recommended_action。\n保存位置：导入本工作台 AI编辑部。`; }
    function makeCosmosTask(item){return `任务阶段：素材深拆\n建议 Skill：cosmos-xiaohongshuvideo-breakdown\nSkill 来源：https://github.com/Cosmoslmj/cosmos-xiaohongshuvideo-breakdown\n用户目标：只对高价值素材做深度拆解，判断需求、知识、包装和创作增量，不从单条素材直接仿写。\n输入材料：素材ID ${item.id}；标题 ${item.title}；平台 ${item.platform}；原链接 ${item.sourceUrl}\n逐字稿：\n${item.transcript}\n必须遵守：ANALYSIS_PROMPT.md V4.1 优先；不延展 5-10 条系列；不直接生成大量迁移标题或完整稿；先判断需求与创作增量。\n期望输出：V4.1 analysis.md JSON，并绑定素材ID ${item.id}。\n保存位置：items/${item.id}/analysis.md。`; }
    function makeHvTask(p){return `任务阶段：深度研究\n建议 Skill：hv-analysis\nSkill 来源：https://github.com/KKKKhazix/khazix-skills/tree/main/hv-analysis\n用户目标：系统搞懂该需求/工具/概念，判断是否值得投入实测或内容制作。\n输入材料：内容项目ID ${p.id}；用户问题 ${p.title}\n必须遵守：这是重型任务，只在用户主动选择后执行；不要用于普通短内容；保留官方来源和竞品/历史演进。\n期望输出：研究结论、可靠来源、仍需实测的问题、是否进入内容制作。`; }
    function makeTitleTask(p){return `任务阶段：标题\n建议 Skill：xhs-title\nSkill 来源：https://github.com/ren644/xhs-title-skill\n用户目标：在内容结构和核心承诺确定后生成标题候选。\n输入材料：内容项目ID ${p.id}；目标用户/任务 ${p.title}；当前状态 ${p.status}\n必须遵守：20字以内是上限不是越短越好；语义完整；允许适度夸张和悬念；不编造结果；标题与封面互补；只保留1主+最多2备选。\n期望输出：主标题、最多2个备用标题、每个标题为什么成立。`; }
    function makeCoverTask(p){return `任务阶段：封面\n建议 Skill：cover-anchor-system\nSkill 来源：https://github.com/ponyodong2026/ponyo-cover-anchor-system/tree/main/cover-anchor-system\n用户目标：为已确定标题设计小红书3:4封面信息层级。\n输入材料：内容项目ID ${p.id}；标题/用户任务 ${p.title}\n必须遵守：优先真实截图、成品和结果证据；不强制固定配色；账号视觉一致性优先；不添加他人水印、Logo或虚假数据。\n期望输出：封面主标题、副标题、视觉锚点、可用真实素材、不可做事项。`; }
    function makeWriteTask(p){return `任务阶段：正式内容创作\n建议 Skill：ChatGPT / Codex（不接API，手动复制）\n用户目标：基于已过制作门禁的需求，生成原创小红书内容任务包。\n输入材料：内容项目ID ${p.id}；用户任务 ${p.title}；来源素材 ${p.sourceMaterialIds.join(', ')}\n必须遵守：用用户本人理解、真实经验和可展示证据；包含标题规则、封面规则、逐字稿要求和剪辑标注；不自动发布；不声称自动剪辑。\n期望输出：目标用户、内容承诺、知识证据、封面、标题、逐字稿、画面和发布前检查。`; }

    function bindReviewForm(){const form=document.getElementById('reviewForm');if(!form)return;form.onsubmit=e=>{e.preventDefault();const data=Object.fromEntries(new FormData(form).entries());data.id=data.id||`review-${Date.now()}`;const idx=state.reviews.findIndex(r=>r.id===data.id);if(idx>=0)state.reviews[idx]=data;else state.reviews.unshift(data);saveState();form.reset();render();};document.getElementById('clearReview').onclick=()=>form.reset();document.getElementById('exportReviews').onclick=()=>downloadJson('复盘库.json',state.reviews);document.getElementById('importReviews').onchange=e=>importJsonFile(e,file=>{state.reviews=Array.isArray(file)?file:[];saveState();render();});document.querySelectorAll('[data-review-edit]').forEach(btn=>btn.onclick=()=>{const r=state.reviews.find(x=>x.id===btn.dataset.reviewEdit);if(!r)return;for(const[k,v]of Object.entries(r)){if(form.elements[k])form.elements[k].value=v}window.scrollTo({top:0,behavior:'smooth'});});document.querySelectorAll('[data-review-delete]').forEach(btn=>btn.onclick=()=>{state.reviews=state.reviews.filter(r=>r.id!==btn.dataset.reviewDelete);saveState();render();});}
    function importEditorial(e){importJsonFile(e,data=>{state.editorialDaily=[data,...(state.editorialDaily||[])];saveState();render();});}
    function importJsonFile(e,cb){const file=e.target.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{cb(JSON.parse(reader.result))}catch(err){alert(`导入失败：${err.message}`)}};reader.readAsText(file,'utf-8');}
    function downloadJson(name,data){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();URL.revokeObjectURL(url)}
    document.getElementById('exportStateBtn').onclick=()=>downloadJson(`工作台状态-${new Date().toISOString().slice(0,10)}.json`,state);
    document.getElementById('importStateInput').onchange=e=>importJsonFile(e,data=>{state={...state,...data};saveState();render();});
    document.getElementById('syncBtn').onclick=()=>alert('本地 HTML 不能直接执行 git pull。请双击桌面入口“短视频收集助手工作台”刷新；它会同步 GitHub、补封面并重建页面。');
    document.getElementById('search').oninput=()=>{selected=null;render();};
    function render(){renderHeader();renderToday();renderTabs();if(currentModule==='materials')renderMaterials();if(currentModule==='editorial')renderEditorial();if(currentModule==='knowledge')renderKnowledge();if(currentModule==='topics')renderTopics();if(currentModule==='reviews')renderReviews();renderDetail();}
    render();
  </script>
</body>
</html>
"""


def main():
    raw_materials = load_materials()
    materials = dedupe_materials(raw_materials)
    demands = build_demands(materials)
    knowledge = build_knowledge(materials)
    packaging = build_packaging_references(materials)
    projects = build_content_projects(materials, demands, knowledge)
    payload = {
        "app": {
            "title": "AI内容创作工作台",
            "subtitle": "把外部信息变成自己的知识和原创内容",
            "specVersion": "4.1",
            "modules": [
                {"id": "materials", "label": "素材总览"},
                {"id": "editorial", "label": "AI编辑部"},
                {"id": "knowledge", "label": "知识库"},
                {"id": "topics", "label": "选题与学习"},
                {"id": "reviews", "label": "复盘库"},
            ],
        },
        "objects": {
            "materials": materials,
            "demands": demands,
            "knowledge": knowledge,
            "packagingReferences": packaging,
            "contentProjects": projects,
            "reviews": [],
        },
        "editorial": load_editorial(),
        "stats": build_stats(materials, raw_materials),
        "repoCommit": repo_commit(),
        "categoryDefaults": CATEGORY_DEFAULTS,
        "valueLabels": VALUE_LABELS,
        "nextActions": NEXT_ACTIONS,
    }
    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    OUTPUT.write_text(html, encoding="utf-8")
    LEGACY_OUTPUT.write_text(html, encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT),
        "legacy_output": str(LEGACY_OUTPUT),
        "materials": len(materials),
        "demands": len(demands),
        "knowledge": len(knowledge),
        "packaging_references": len(packaging),
        "content_projects": len(projects),
        "repo_commit": payload["repoCommit"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
