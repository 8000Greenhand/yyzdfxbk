# 分析结果

## 1. 素材判断
- 主分类：Skill / 工具
- 利用方式：需求证据、知识线索、包装参考、进入选题
- 一句话总结：介绍一个包含约 1.4 万条图片提示词的 Skill，覆盖头像、电商、海报、封面、漫画和游戏等场景，主打按需求快速找到现成参考。
- 分析深度：轻分析

## 2. 用户需求
- 核心需求：经常需要生成图片、却不会写提示词也不知道该参考什么风格的人，希望按具体场景快速获得可用提示词，而不是每次从空白开始。
- 需求证据：点赞 7592、收藏 9187、评论 530、分享 1458；收藏高于点赞，说明“可查询的大型提示词库”具有明显工具和资源价值。
- 答案缺口：数量多不代表质量稳定；原内容没有说明具体仓库、提示词版权和来源、跨模型适配、中文效果以及真实检索效率。
- 置信度：高

## 3. 可提取知识
- **AI Image Prompt Skill（具体仓库需核查）**：作者称包含约 14500 条图片提示词，可按头像、电商、封面等分类查询。
- **按任务检索提示词**：用户先描述场景，再由 Agent 从库中返回候选，而不是人工浏览全部提示词。
- 状态：仅素材提及；必须找到原仓库并测试 3—5 个用户真实场景。

## 4. 包装与表达参考
- “14000+提示词”和“这一个就够了”用极大数量和替代性承诺制造点击，再用大量结果图迅速证明覆盖面。
- 可迁移的是数字规模和多场景结果展示；不能照搬“一个解决全部”或把库中提示词直接视为原创、可商用资产。

## 5. 对我的创作增量
- 新增能力：提供一个不需要开发完整工作台的低成本实测选题，也可能补充用户做封面和图文时的提示词检索能力。
- 当前准备状态：需要研究。
- 需要补充：准确仓库、安装方式、许可协议、中文检索、不同模型下的 5 组结果对比。
- 制作适配：完成安装后可在 2—3 小时内做“数量很多是否真的更好用”的实测。

## 6. 下一步
进入知识核查，找到原 Skill 并用用户的封面、电商图和插画需求做实测。

## 7. JSON
```json
{
  "schema_version": "4.1",
  "card_value": "高收藏证明用户需要按场景检索提示词，但必须验证数量、质量和授权是否真的有用",
  "summary": "介绍一个包含约1.4万条图片提示词、覆盖多类生图场景的Skill",
  "primary_category": "skill_tools",
  "category_label": "Skill / 工具",
  "tags": ["AI生图", "提示词库", "Skill", "封面"],
  "analysis_depth": "light",
  "use_modes": ["demand_signal", "knowledge_lead", "packaging_reference", "topic_support"],
  "demand_signal": {
    "statement": "经常需要生成图片但不会写提示词的人，希望按具体场景快速获得可用参考，而不是每次从空白开始",
    "evidence": ["点赞7592、收藏9187、评论530、分享1458", "收藏高于点赞，资源复用价值明显"],
    "answer_gap": "缺少准确仓库、许可协议、中文效果、跨模型适配和真实检索效率",
    "confidence": "high"
  },
  "knowledge_leads": [
    {
      "canonical_name": "AI Image Prompt Skill（具体仓库需核查）",
      "knowledge_group": "skill_library",
      "asset_type": "skill",
      "one_liner": "按头像、电商、封面、漫画等场景检索图片提示词",
      "material_claim": "作者称库中约有14500条提示词",
      "source_status": "mentioned",
      "source_urls": ["https://v.douyin.com/i0vNfHttbBo/"],
      "verification_needed": ["找到原仓库", "检查许可协议", "测试中文检索和跨模型效果"],
      "dedupe_key": "ai-image-prompt-skill-unspecified|skill"
    },
    {
      "canonical_name": "按任务检索提示词",
      "knowledge_group": "skill_library",
      "asset_type": "method",
      "one_liner": "先描述真实图像任务，再从提示词库检索少量候选",
      "material_claim": "作者建议直接告诉Agent场景并让它返回对应提示词",
      "source_status": "mentioned",
      "source_urls": ["https://v.douyin.com/i0vNfHttbBo/"],
      "verification_needed": ["比较检索与直接让模型写提示词的差异"],
      "dedupe_key": "task-based-prompt-retrieval|method"
    }
  ],
  "content_insight": {
    "original_title": "一个skill里面14000+提示词！查AI生图提示词，这一个就够了！",
    "cover_expression": "超大数字、一个就够和多场景结果图",
    "title_cover_roles": "标题强调规模和替代性，画面快速展示不同类型结果",
    "click_or_stop_reason": "用户既缺提示词，也担心自己漏掉更好的风格参考",
    "strongest_transferable_points": ["用数字表达资源规模", "连续展示不同场景结果"],
    "non_transferable_points": ["未经实测宣称一个解决全部", "忽略提示词来源和授权"],
    "promise_delivered": "unknown"
  },
  "creator_transfer": {
    "new_capability": "增加一个可以快速实测并服务封面、图文制作的工具候选",
    "readiness": "needs_research",
    "missing_pieces": ["准确仓库", "许可协议", "5个真实场景测试", "与直接生成提示词对比"],
    "production_fit": "安装后2—3小时可完成实测内容"
  },
  "topic_opportunity": {
    "should_enter_pool": true,
    "user_problem": "提示词库有一万多条，普通人真的会更容易做出好图吗",
    "why_worth_testing": "高收藏证明资源需求强，用户又有大量真实做图任务",
    "current_status": "needs_test"
  },
  "next_action": {
    "action": "add_knowledge",
    "reason": "先找到并实测原Skill，确认质量和授权后再制作"
  }
}
```