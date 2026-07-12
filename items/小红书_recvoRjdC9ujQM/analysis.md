# 分析结果

## 1. 素材判断
- 主分类：运营与内容
- 利用方式：需求证据、知识线索、包装参考、表达参考、进入选题
- 一句话总结：把“AI味”拆成 10 个可检查的具体痕迹，帮助用户把模糊的不自然感变成发布前可执行的文案质检。
- 分析深度：轻分析

## 2. 用户需求
- 核心需求：已经用 AI 写文章或口播、却觉得成品不像自己的人，希望知道具体哪里有 AI 味，以及怎样快速修改而不是整篇重写。
- 需求证据：视频有评论 394、分享 1636；标题直接命中高频困扰，内容提供可转成提示词或 Skill 的明确清单。
- 答案缺口：破折号、三段式、转折等并不天然等于 AI 味；如果机械删除，可能损伤原本有效的表达，最终仍需要作者自己的经历、判断和语言习惯。
- 置信度：高

## 3. 可提取知识
- **AI 文案 10 项检查法**：检查破折号、不是A而是B、固定三项、句首连接词、句尾拔高、节奏固定、段落升华、全程确定、面面俱到和假精确。
- **真实表达补充规则**：不确定时承认不确定，用真实经历、具体细节和个人强观点替代假数据与平均化表达。
- 状态：来源内容完整，但仍需用用户自己的稿件做前后对比，确认哪些规则真正有效。

## 4. 包装与表达参考
- 标题只保留一个清晰问题，内容用“10个痕迹”提供明确收藏价值，并直接告诉用户可以转成提示词或 Skill。
- 可迁移的是模糊问题具体化；不能把所有常见句式都粗暴判定为 AI，也不能只靠删除句式制造“真人感”。

## 5. 对我的创作增量
- 新增能力：可以把用户自己的口播稿做成发布前检查清单，减少报告腔和模板腔。
- 当前准备状态：需要实测。
- 需要补充：选 3 篇用户真实稿件做修改前后对比，并补充“个人经历、真实犹豫、强判断”三项正向规则。
- 制作适配：适合低成本实测内容，也适合直接沉淀成工作台内部质检规则。

## 6. 下一步
进入知识库并安排一次用户真实稿件的前后对比测试。

## 7. JSON
```json
{
  "schema_version": "4.1",
  "card_value": "把模糊的AI味拆成可执行检查项，可直接用于用户自己的口播稿质检",
  "summary": "用10个具体痕迹识别和修改AI写作中的模板化表达",
  "primary_category": "operations_content",
  "category_label": "运营与内容",
  "tags": ["AI写作", "去AI味", "口播稿", "文案质检"],
  "analysis_depth": "light",
  "use_modes": ["demand_signal", "knowledge_lead", "packaging_reference", "expression_reference", "topic_support"],
  "demand_signal": {
    "statement": "已经用AI写内容但觉得成品不像自己的人，希望知道具体哪里有AI味，以及怎样快速修改而不是整篇重写",
    "evidence": ["评论394、分享1636", "标题直接命中问题，内容提供10项清单"],
    "answer_gap": "常见句式不天然等于AI味，机械删除可能损伤表达，仍需加入个人经历和判断",
    "confidence": "high"
  },
  "knowledge_leads": [
    {
      "canonical_name": "AI 文案 10 项检查法",
      "knowledge_group": "operations_content",
      "asset_type": "method",
      "one_liner": "把常见AI写作痕迹变成发布前可逐项检查的清单",
      "material_claim": "视频列出破折号、固定三项、连接词、段落升华、假精确等10类痕迹",
      "source_status": "source_confirmed",
      "source_urls": ["http://xhslink.com/o/8b3xOLRZUO8"],
      "verification_needed": ["用用户真实稿件做前后对比", "识别哪些规则不应机械使用"],
      "dedupe_key": "ai-writing-ten-signs|method"
    },
    {
      "canonical_name": "真人表达正向规则",
      "knowledge_group": "operations_content",
      "asset_type": "rule",
      "one_liner": "用真实经历、具体细节、不确定性和个人判断替代假精确与平均化表达",
      "material_claim": "作者建议不确定时承认不确定，并用真实经历替代虚构数字",
      "source_status": "source_confirmed",
      "source_urls": ["http://xhslink.com/o/8b3xOLRZUO8"],
      "verification_needed": ["补充用户自己的口语习惯"],
      "dedupe_key": "human-expression-positive-rules|rule"
    }
  ],
  "content_insight": {
    "original_title": "如何让AI写的东西没有AI味",
    "cover_expression": "一个明确问题与10项检查结果",
    "title_cover_roles": "标题负责痛点，内容用编号清单提供可收藏答案",
    "click_or_stop_reason": "用户知道成品不自然，却说不清问题在哪里",
    "strongest_transferable_points": ["把模糊感受拆成具体检查项", "告诉用户可以直接沉淀成提示词或Skill"],
    "non_transferable_points": ["把所有破折号和三段式都判定为AI", "只删句式而不加入个人经验"],
    "promise_delivered": "yes"
  },
  "creator_transfer": {
    "new_capability": "建立用户自己的口播稿发布前质检规则",
    "readiness": "needs_test",
    "missing_pieces": ["3篇真实稿件对比", "用户个人语言习惯", "正向表达规则"],
    "production_fit": "可在2小时内完成一篇稿件前后对比并录屏"
  },
  "topic_opportunity": {
    "should_enter_pool": true,
    "user_problem": "AI写得很完整，为什么一念出来就完全不像自己",
    "why_worth_testing": "高分享说明问题具有传播性，且用户可用自己的真实稿件验证",
    "current_status": "needs_test"
  },
  "next_action": {
    "action": "add_knowledge",
    "reason": "先沉淀为内部质检规则，并用真实稿件验证后再制作"
  }
}
```