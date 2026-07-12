# 分析结果

## 1. 素材判断
- 主分类：Skill / 工具
- 利用方式：需求证据、知识线索、包装参考、进入选题
- 一句话总结：介绍一个上传图片、圈选原文字并输入新内容，就能自动匹配字体、颜色和排版的图片文字替换工具。
- 分析深度：轻分析

## 2. 用户需求
- 核心需求：经常需要修改电商海报、笔记截图、横幅和表情包文字、但不会 PS 或没有时间重做的人，希望几秒完成看起来接近原图的文字替换。
- 需求证据：评论 210、分享 3842；高分享说明这是很容易转给电商、设计和运营同事的具体实用问题。
- 答案缺口：逐字稿没有提供工具名称和入口，也没有证明复杂背景、中文字体、长短文字变化和商用图片下都能“放大10倍看不出”。
- 置信度：高

## 3. 可提取知识
- **无痕图片文字替换工具（名称缺失）**：上传图片、圈选文字并输入新内容，尝试自动匹配字体、颜色和排版。
- **图片改字测试标准**：至少检查字体相似度、背景修复、文字长度变化、中文标点、放大细节和导出清晰度。
- 状态：工具名称缺失，必须先从原视频画面或评论区确认，再做实测。

## 4. 包装与表达参考
- “求做电商的姐妹看”先精准圈人，“再也不用PS”直接给出替代结果，开头第一句继续展示“任意图片、放大10倍”的强效果。
- 可迁移的是人群 + 高频任务 + 可见结果；不能照搬“任意、无痕、放大10倍”这种未经过多场景验证的绝对承诺。

## 5. 对我的创作增量
- 新增能力：这是与用户图片处理和运营工作高度相关的低成本工具实测方向，不需要开发新工作台。
- 当前准备状态：需要研究。
- 需要补充：准确工具、入口和费用；用电商海报、聊天截图、手写笔记、复杂背景至少测试 4 张图。
- 制作适配：找到工具后可在 2—3 小时完成对比测试，适合短录屏内容。

## 6. 下一步
进入知识核查，先确认工具名称，再按 4 类图片做真实改字测试。

## 7. JSON
```json
{
  "schema_version": "4.1",
  "card_value": "高分享证明图片改字是强实用需求，适合做低成本真实工具测试",
  "summary": "用AI圈选并替换图片文字，自动尝试匹配原字体、颜色和排版",
  "primary_category": "skill_tools",
  "category_label": "Skill / 工具",
  "tags": ["图片改字", "电商", "AI修图", "PS替代"],
  "analysis_depth": "light",
  "use_modes": ["demand_signal", "knowledge_lead", "packaging_reference", "topic_support"],
  "demand_signal": {
    "statement": "需要修改电商海报、截图和横幅文字但不会PS或没有时间重做的人，希望几秒完成接近原图的文字替换",
    "evidence": ["评论210、分享3842", "高分享说明任务具体且适合转给同事"],
    "answer_gap": "缺少工具名称、复杂背景和中文字体测试，也没有证据支持任意图片都无痕",
    "confidence": "high"
  },
  "knowledge_leads": [
    {
      "canonical_name": "无痕图片文字替换工具（名称缺失）",
      "knowledge_group": "skill_library",
      "asset_type": "tool",
      "one_liner": "圈选图片原文字并输入新内容，自动匹配字体、颜色和排版",
      "material_claim": "作者称可用于电商海报、手写笔记、横幅和表情包",
      "source_status": "mentioned",
      "source_urls": ["https://www.xiaohongshu.com/discovery/item/6a3a79c3000000001700b9af"],
      "verification_needed": ["确认工具名称和入口", "核查费用与隐私", "测试4类图片"],
      "dedupe_key": "ai-image-text-replacement-unspecified|tool"
    },
    {
      "canonical_name": "图片改字六项测试",
      "knowledge_group": "operations_content",
      "asset_type": "method",
      "one_liner": "检查字体、背景、字数变化、中文标点、放大细节和导出清晰度",
      "material_claim": "原内容重点承诺匹配字体颜色排版和放大细节",
      "source_status": "mentioned",
      "source_urls": ["https://www.xiaohongshu.com/discovery/item/6a3a79c3000000001700b9af"],
      "verification_needed": ["形成真实前后对比"],
      "dedupe_key": "image-text-edit-six-tests|method"
    }
  ],
  "content_insight": {
    "original_title": "求做电商的姐妹看！图片改字再也不用PS了！",
    "cover_expression": "精准人群、图片改字和PS替代",
    "title_cover_roles": "标题圈定电商人群和替代结果，开头继续用无痕效果强化",
    "click_or_stop_reason": "用户一眼能联想到自己反复修改海报文字的场景",
    "strongest_transferable_points": ["精准圈定使用人群", "第一秒展示改前改后结果"],
    "non_transferable_points": ["任意图片和放大10倍等绝对承诺", "不展示失败样本"],
    "promise_delivered": "unknown"
  },
  "creator_transfer": {
    "new_capability": "增加一个与运营真实任务相关、无需开发新系统的工具实测选题",
    "readiness": "needs_research",
    "missing_pieces": ["准确工具", "入口费用", "4类图片实测", "失败边界"],
    "production_fit": "找到工具后2—3小时可完成短录屏测试"
  },
  "topic_opportunity": {
    "should_enter_pool": true,
    "user_problem": "不会PS的人，AI图片改字到底能不能保住原字体和背景",
    "why_worth_testing": "高分享证明需求强，且结果非常适合屏幕录制展示",
    "current_status": "needs_test"
  },
  "next_action": {
    "action": "add_knowledge",
    "reason": "先确认具体工具并做多场景实测，不能仅凭演示下结论"
  }
}
```