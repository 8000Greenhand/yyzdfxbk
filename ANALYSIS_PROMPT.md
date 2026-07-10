# 素材分析标准 · 工作台 V3

## 1. 任务

读取 `items/**/meta.json` 与 `items/**/transcript.md`，把分析写入对应 `analysis.md`。

不要修改逐字稿，不上传媒体，不调用付费服务，不自动发布。

目标只有三个：

1. 让素材进入“链接处理”后能快速看懂；
2. 提取真正可利用的技能和知识；
3. 提取可供选题库调用的爆款表达。

不是每条素材都必须产生知识或选题。

## 2. 账号定位

默认服务对象：不懂技术、但需要用AI完成运营、市场、商务、内容和职场任务的人。

分析要讲清：这是什么、有什么用、怎么用、有什么限制，以及哪些表达值得复刻。

## 3. 主分类

每条素材只给一个主分类：

- `skill_tools`：Skill、工具、网站、平台、插件、GitHub项目、产品功能；
- `ai_knowledge`：模型更新、产品功能、额度、价格、规则、使用区别和AI知识；
- `operations`：小红书、内容运营、达人、投放、数据、选题和标题；
- `workplace_efficiency`：PPT、表格、会议、文案、资料整理和自动化；
- `personal_growth`：学习、职业成长和经验；
- `viral_reference`：主要价值是标题、封面、开头、结构或数据；
- `manual_pending`：无法可靠判断。

既有知识又是爆款时，按主要内容分类，并设置 `is_viral_reference=true`。

## 4. 原内容分析

必须包含：

- 原标题与封面表达；
- 前3—5秒原话或概括；
- 4—8步内容结构；
- 为什么会点击、收藏、评论、分享；
- 信任来自哪里；
- 表达成立的条件；
- 哪些地方不能照搬。

有互动数据时结合点赞、收藏、评论、分享和时长判断。

## 5. 沉淀技能 / 知识

只提取具体、可利用的内容：Skill、工具、网站、平台、插件、项目、产品功能、设置、规则、教程和可核验结论。

每条必须写清：

- 名称；
- 一句话用途；
- 解决的问题；
- 怎么使用；
- 使用条件和限制；
- 当前来源状态；
- 下一步动作。

以下内容不要独立沉淀：

- 只有“收集→分析→分类”这类抽象步骤；
- “这个工作流很好”“这个Skill很强”；
- 没有名称、入口、步骤或来源的推荐；
- 没有新增信息的重复知识。

知识分组：

- `skill_library`
- `ai_knowledge`
- `operations`
- `workplace_efficiency`
- `personal_growth`
- `manual_pending`

来源状态：

- `mentioned`：素材中提到；
- `source_confirmed`：找到原始来源；
- `tested`：用户已实际使用。

## 6. 爆款复刻

数据或表达值得参考时设置 `is_viral_reference=true`。

最多输出：

- 1—3个标题改写；
- 1—3个开头改写；
- 内容结构；
- 干货点；
- 价值锚点；
- 信任证据；
- 适用主题；
- 照搬风险。

标题不超过20字。不能只替换关键词，不能使用正文无法支撑的承诺。

## 7. 选题种子

只有存在真实知识、真实案例或强爆款表达时才生成。

每条包括：类别、选题名、用户问题、为什么值得做、状态。

状态：`needs_evidence` 或 `ready`。

## 8. Markdown结构

```md
# 分析结果

## 1. 素材分类
- 主分类
- 标签
- 一句话总结
- 是否可作爆款参考

## 2. 原内容分析
### 标题与封面
### 前3—5秒
### 内容结构
### 为什么会点、藏、评、转
### 成立条件与不可照搬

## 3. 沉淀技能 / 知识

## 4. 爆款复刻
### 可复刻标题
### 可复刻开头
### 结构
### 干货点与价值锚点
### 信任证据
### 适用主题
### 照搬风险

## 5. 可进入选题库的方向

## 6. JSON
```

## 9. JSON V3

```json
{
  "schema_version": "3.0",
  "card_value": "一句话价值",
  "summary": "内容总结",
  "rewrite_best_topic": "最推荐选题；没有则写暂不生成",
  "tags": ["标签"],
  "primary_category": "skill_tools|ai_knowledge|operations|workplace_efficiency|personal_growth|viral_reference|manual_pending",
  "category_label": "中文分类名",
  "material_summary": "列表页一句话总结",
  "is_viral_reference": true,
  "content_analysis": {
    "original_title": "原标题",
    "cover_expression": "封面表达",
    "title_cover": "标题与封面分析",
    "opening_quote": "前3—5秒",
    "opening_analysis": "开头分析",
    "structure": ["步骤1", "步骤2"],
    "click_reason": "点击原因",
    "save_reason": "收藏原因",
    "comment_reason": "评论原因",
    "share_reason": "分享原因",
    "trust_reason": "信任来源",
    "conditions": ["成立条件"],
    "copy_risks": ["不可照搬"]
  },
  "knowledge_assets": [
    {
      "canonical_name": "名称",
      "knowledge_group": "skill_library|ai_knowledge|operations|workplace_efficiency|personal_growth|manual_pending",
      "asset_type": "skill|tool|website|platform|plugin|github_project|platform_feature|fact|rule|decision|tutorial",
      "one_liner": "一句话用途",
      "what_it_solves": "解决的问题",
      "how_to_use": ["步骤"],
      "requirements_and_limits": "条件和限制",
      "source_status": "mentioned|source_confirmed|tested",
      "source_urls": ["来源"],
      "next_action": "下一步",
      "dedupe_key": "规范名称|类型"
    }
  ],
  "viral_replication": {
    "reference_title": "原标题",
    "reference_cover": "原封面",
    "reference_opening": "原开头",
    "title_rewrites": ["标题1", "标题2", "标题3"],
    "opening_rewrites": ["开头1", "开头2", "开头3"],
    "content_structure": ["结构"],
    "dry_points": ["干货点"],
    "value_anchors": ["价值锚点"],
    "trust_proofs": ["信任证据"],
    "suitable_topics": ["适用主题"],
    "copy_risks": ["照搬风险"]
  },
  "topic_seeds": [
    {
      "topic_category": "AI领域|Skill工具|运营|职场效率|个人成长",
      "topic_name": "20字以内",
      "user_problem": "用户问题",
      "why_now": "为什么值得做",
      "source": "material",
      "status": "needs_evidence|ready"
    }
  ]
}
```

## 10. 写回检查

- 主分类是否可靠；
- 一句话总结是否一眼能懂；
- 知识是否具体可利用；
- 来源状态是否诚实；
- 爆款改写是否只替换关键词；
- 标题是否不超过20字；
- 是否为了凑数硬生成知识或选题；
- JSON是否可解析。

处理结束只反馈数量、分类、知识数、爆款参考数、选题种子数、待分类数和最新commit。
