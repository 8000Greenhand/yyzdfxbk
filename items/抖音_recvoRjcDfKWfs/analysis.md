# 分析结果

## 1. 素材判断
- 主分类：Skill / 工具
- 利用方式：需求证据、知识线索、包装参考、补充已有主题
- 一句话总结：按选题调研、文案、配音字幕、剪辑、发布复盘五个阶段盘点 AI 视频 Skill，帮助创作者理解完整生产流程。
- 分析深度：轻分析

## 2. 用户需求
- 核心需求：想用 AI 做视频、却被大量工具和 Skill 搞乱的创作者，希望按实际任务阶段知道先用什么、后用什么，以及哪些暂时不必安装。
- 需求证据：点赞 18175、收藏 21725、评论 1043、分享 4389，收藏高于点赞，说明“流程地图和工具清单”具有明显复用价值。
- 答案缺口：工具数量过多，多个名称来自转写且可能不准确；缺少针对普通新手的优先级、安装成本、实测效果和淘汰结论。
- 置信度：高

## 3. 可提取知识
- **MediaCrawler（名称需核查）**：作者称可抓取多个内容平台及评论，适合爆款和评论研究；需确认原仓库、平台限制和合规边界。
- **Humanizer（具体仓库需核查）**：作者称用于减少文案 AI 味；需确认项目来源，并与用户自己的真人表达检查规则区分。
- **第三方 Skill 安全审查**：安装 Skill 前检查文件读取、命令执行和网络权限；属于长期使用 Agent 的必要规则，需补可靠审查流程。

## 4. 包装与表达参考
- “整理一周、从调研到复盘、这一条全讲透、附文档”把时间投入、完整度和资源领取叠加，天然促进收藏。
- 可迁移的是按任务阶段组织信息；不能照搬超长工具清单和未经实测的 GitHub 星数、功能结论。

## 5. 对我的创作增量
- 新增能力：为工作台 Skill 路由提供“按任务调用，而不是按数量囤积”的市场证据。
- 当前准备状态：需要研究。
- 需要补充：逐个确认名称和仓库，筛成普通创作者真正需要的 3—5 个，而不是继续扩充清单。
- 制作适配：适合研究后做“新手先解决哪三步”的内容，不适合直接复述全工具库。

## 6. 下一步
进入知识核查，先从工具清单中确认最有价值且能实测的 3 个。

## 7. JSON
```json
{
  "schema_version": "4.1",
  "card_value": "用高收藏数据证明创作者需要按任务阶段理解Skill，而不是继续囤工具",
  "summary": "按调研、文案、配音字幕、剪辑和复盘盘点AI视频生产Skill",
  "primary_category": "skill_tools",
  "category_label": "Skill / 工具",
  "tags": ["AI视频", "Skill地图", "内容流程", "安全审查"],
  "analysis_depth": "light",
  "use_modes": ["demand_signal", "knowledge_lead", "packaging_reference", "topic_support"],
  "demand_signal": {
    "statement": "想用AI做视频但被大量工具搞乱的创作者，希望按任务阶段知道先用什么、后用什么以及哪些暂时不必安装",
    "evidence": ["点赞18175、收藏21725、评论1043、分享4389", "收藏高于点赞，流程地图具有强复用价值"],
    "answer_gap": "缺少新手优先级、准确仓库、安装成本、实测效果和淘汰结论",
    "confidence": "high"
  },
  "knowledge_leads": [
    {
      "canonical_name": "MediaCrawler（名称需核查）",
      "knowledge_group": "skill_library",
      "asset_type": "github_project",
      "one_liner": "抓取内容平台公开内容与评论，用于选题和评论研究",
      "material_claim": "作者称其覆盖抖音、小红书、快手等平台",
      "source_status": "mentioned",
      "source_urls": ["https://v.douyin.com/WEiCZ6u3Vw8/"],
      "verification_needed": ["确认原仓库", "检查平台支持与合规边界"],
      "dedupe_key": "mediacrawler|github_project"
    },
    {
      "canonical_name": "Humanizer（具体仓库需核查）",
      "knowledge_group": "skill_library",
      "asset_type": "skill",
      "one_liner": "检查并减少文案中僵硬、模板化的AI表达",
      "material_claim": "作者建议放在文案完成后的处理阶段",
      "source_status": "mentioned",
      "source_urls": ["https://v.douyin.com/WEiCZ6u3Vw8/"],
      "verification_needed": ["确认具体项目", "与用户自己的文案规则对比"],
      "dedupe_key": "humanizer-unspecified|skill"
    },
    {
      "canonical_name": "第三方 Skill 安全审查",
      "knowledge_group": "ai_knowledge",
      "asset_type": "rule",
      "one_liner": "安装第三方Skill前检查其文件、命令和网络权限",
      "material_claim": "作者认为长期使用第三方Skill时安全审查是必需环节",
      "source_status": "mentioned",
      "source_urls": ["https://v.douyin.com/WEiCZ6u3Vw8/"],
      "verification_needed": ["形成可执行的安全检查清单"],
      "dedupe_key": "third-party-skill-security-review|rule"
    }
  ],
  "content_insight": {
    "original_title": "自媒体人的skill盘点",
    "cover_expression": "整理一周、从调研到复盘、全讲透、附文档",
    "title_cover_roles": "标题承诺完整路线和资源，内容按五阶段展开",
    "click_or_stop_reason": "用户害怕漏工具，也缺少一张能看懂的流程地图",
    "strongest_transferable_points": ["按任务阶段组织", "明确新手与进阶工具层级"],
    "non_transferable_points": ["未经核查的项目名称和星数", "把大量工具都描述成必装"],
    "promise_delivered": "partial"
  },
  "creator_transfer": {
    "new_capability": "为工作台建立按阶段调用Skill而非囤积Skill的路由原则",
    "readiness": "needs_research",
    "missing_pieces": ["准确项目来源", "3—5个工具实测", "新手优先级"],
    "production_fit": "适合筛选后做少量工具决策内容，不适合复述完整清单"
  },
  "topic_opportunity": {
    "should_enter_pool": true,
    "user_problem": "AI视频Skill太多，普通创作者第一批到底应该先装什么",
    "why_worth_testing": "高收藏证明流程型工具筛选需求强",
    "current_status": "needs_research"
  },
  "next_action": {
    "action": "add_knowledge",
    "reason": "先核查项目并筛出少量真正值得实测的Skill"
  }
}
```