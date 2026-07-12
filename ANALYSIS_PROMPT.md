# 素材分析标准 · 工作台 V4.1

## 0. 总原则

原视频只是学习输入，不是最终交付。

分析的目的，是把外部内容转化为用户自己的：

1. 用户需求判断；
2. 可核查知识；
3. 包装与表达参考；
4. 真实证据或案例；
5. 原创内容机会。

禁止把工作台做成高级收藏夹。分析结果必须回答：

> 这条素材能帮助我创作出什么原来创作不出来的东西？

回答不出来时，只保留链接和一句话总结，不继续加工。

## 1. 输入与红线

读取 `items/**/meta.json` 与 `items/**/transcript.md`，把结果写入同目录 `analysis.md`。

必须遵守：

- 不修改 `transcript.md`；
- 不删除原素材或旧分析；
- 不上传视频、音频；
- 不调用付费 API；
- 不自动发布；
- 不编造标题、封面、数据、评论、功能或来源；
- 没有证据时明确写“无法确认”或留空；
- 不从单条素材直接生成完整逐字稿；
- 不为凑字段强行生成知识、需求或选题。

## 2. 先分流，再分析

每条素材先判断利用方式，可多选：

- `demand_signal`：证明某个用户问题真实存在；
- `knowledge_lead`：出现工具、Skill、产品、方法、规则或事实线索；
- `packaging_reference`：标题、封面或首屏点击机制值得学习；
- `expression_reference`：开头、讲解顺序、案例表达值得学习；
- `evidence_asset`：含真实截图、操作、数据、结果或前后对比；
- `topic_support`：能补充已有需求或知识主题；
- `archive_only`：暂时没有进一步利用价值。

同一条素材可以有多个利用方式。

### 分析深度

- `light`：默认。只输出最有价值的部分；
- `deep`：仅在以下情况使用：
  - 用户手动要求深度分析；
  - 数据明显优秀且材料充分；
  - 同一需求已出现多条证据，需要做专题判断；
  - 即将进入正式内容制作。

不得因为有逐字稿就自动做长篇分析。

## 3. 默认输出预算

普通素材默认最多输出：

- 1 条一句话总结；
- 1 个核心需求；
- 最多 3 条知识线索；
- 最多 2 个包装或表达重点；
- 1 个创作增量判断；
- 1 个下一步动作。

没有对应价值的区块直接省略，不写空话。

## 4. 主分类

每条素材只设一个主分类，可附多个标签：

- `skill_tools`：Skill、工具、网站、软件、插件、GitHub 项目、产品功能；
- `ai_knowledge`：模型、产品更新、AI 原理、规则、区别、使用判断；
- `operations_content`：小红书、内容运营、达人、投放、选题、标题、数据；
- `workplace_efficiency`：PPT、表格、会议、文案、资料、自动化；
- `personal_growth`：学习、职业、经验、认知；
- `packaging_only`：主要价值是标题、封面、开头或视觉表达；
- `manual_pending`：无法可靠判断。

分类描述“它在讲什么”；`use_modes` 描述“它对我有什么用”。两者不能混为一谈。

## 5. 用户需求分析

只有设置了 `demand_signal` 才输出。

核心需求必须写成完整任务：

> 什么人，在什么情况下，因为遇到什么阻碍，希望得到什么结果。

不要写“用户想学 AI”“用户想提高效率”这类宽泛判断。

默认只回答三项：

1. **核心需求**：谁在什么场景下想解决什么问题；
2. **需求证据**：数据、评论、搜索、多个同类样本或明确表达；
3. **答案缺口**：原内容没有解决的最重要问题。

没有数据和评论时，需求只能标记为推断，不能写成已验证事实。

需求置信度：

- `high`：有完整内容，并有数据、评论或多个同类样本支持；
- `medium`：内容完整，但只有部分数据或较强表达证据；
- `low`：只有标题、封面或零散信息。

## 6. 知识线索

捕获门槛低，核查门槛高。

只要素材明确提到“名称 + 大致用途”，就可以登记为知识线索，不要求原视频提供完整入口、价格、API、安装和限制。

每条知识线索优先记录：

- 规范名称；
- 它大致解决什么问题；
- 素材中具体说了什么；
- 当前来源状态；
- 下一步需要核查什么。

来源状态：

- `mentioned`：仅素材提到；
- `source_confirmed`：找到官方、原作者或 GitHub 原始来源；
- `tested`：用户本人已实际使用。

规则：

- `mentioned` 不能直接升级为正式事实；
- 外部核查优先官方文档、官方博客、GitHub 原仓库和原作者内容；
- 费用、API、账号、电脑、版权、地区等，仅在会影响实际使用时补充；
- 同一知识只保留一个规范实体，通过来源列表合并；
- 抽象的“收集→分析→分类”不能单独沉淀成知识。

## 7. 包装与表达参考

只有设置了 `packaging_reference` 或 `expression_reference` 才输出。

素材分析阶段不生成改写标题和完整脚本，只保存市场参考价值。

最多提炼：

- 原标题与原封面各自承担什么；
- 用户为什么会停下或点击；
- 最值得迁移的 1—2 个机制；
- 哪些依赖作者人设、资源、数据或产品，不能照搬；
- 内容是否兑现标题承诺。

不要退化成“人群 + 痛点 + 结果 + 数字”的模板套用。

## 8. 创作者可用性判断

每条有进一步价值的素材都要回答：

- 它给创作增加了什么：新需求、新知识、新证据、新表达或新判断；
- 用户现在是否能讲清楚；
- 是否需要先学习、核查或实测；
- 是否能在日常 2—4 小时制作条件下完成。

制作准备状态：

- `ready`：已有理解、证据和可展示画面；
- `needs_learning`：需要先学懂关键知识；
- `needs_research`：需要补官方来源或事实；
- `needs_test`：需要亲自使用或验证；
- `not_fit`：不适合当前账号或制作成本明显过高；
- `archive`：没有足够创作增量。

## 9. 下一步动作

每条素材只给一个主要动作：

- `merge_demand`：合并到已有用户需求；
- `add_knowledge`：进入知识核查与沉淀；
- `save_packaging`：保存为标题封面参考；
- `save_evidence`：保存证据或案例；
- `send_to_topic`：进入选题与学习；
- `deep_research`：需要专题研究；
- `manual_review`：需要人工判断；
- `archive`：仅保留原素材。

## 10. Markdown 结构

按实际价值选择区块，没有价值的区块不显示。

```md
# 分析结果

## 1. 素材判断
- 主分类
- 利用方式
- 一句话总结
- 分析深度

## 2. 用户需求
- 核心需求
- 需求证据
- 答案缺口

## 3. 可提取知识

## 4. 包装与表达参考

## 5. 对我的创作增量
- 能帮助我新增什么
- 当前准备状态
- 需要补什么

## 6. 下一步

## 7. JSON
```

## 11. JSON V4.1

`analysis.md` 必须包含一个可解析 JSON 代码块。

```json
{
  "schema_version": "4.1",
  "card_value": "这条素材对创作最直接的价值",
  "summary": "一句话说明原内容讲了什么",
  "primary_category": "skill_tools|ai_knowledge|operations_content|workplace_efficiency|personal_growth|packaging_only|manual_pending",
  "category_label": "中文分类名",
  "tags": ["标签"],
  "analysis_depth": "light|deep",
  "use_modes": [
    "demand_signal",
    "knowledge_lead",
    "packaging_reference"
  ],
  "demand_signal": {
    "statement": "什么人在什么场景下，因为何种阻碍，希望获得什么结果",
    "evidence": ["可见证据"],
    "answer_gap": "原内容未解决的最重要问题",
    "confidence": "high|medium|low"
  },
  "knowledge_leads": [
    {
      "canonical_name": "名称",
      "knowledge_group": "skill_library|ai_knowledge|operations_content|workplace_efficiency|personal_growth|manual_pending",
      "asset_type": "skill|tool|website|platform|plugin|github_project|product_feature|fact|rule|method|tutorial",
      "one_liner": "它大致解决什么问题",
      "material_claim": "素材中具体提到了什么",
      "source_status": "mentioned|source_confirmed|tested",
      "source_urls": ["已找到的原始来源"],
      "verification_needed": ["下一步需要核查什么"],
      "dedupe_key": "规范名称|类型"
    }
  ],
  "content_insight": {
    "original_title": "原标题",
    "cover_expression": "原封面表达",
    "title_cover_roles": "标题与封面如何分工",
    "click_or_stop_reason": "为什么会停下或点击",
    "strongest_transferable_points": ["最多2条"],
    "non_transferable_points": ["不能照搬的部分"],
    "promise_delivered": "yes|partial|no|unknown"
  },
  "creator_transfer": {
    "new_capability": "它让我能创作出什么原来创作不出来的内容",
    "readiness": "ready|needs_learning|needs_research|needs_test|not_fit|archive",
    "missing_pieces": ["需要补的知识、证据或实测"],
    "production_fit": "适合什么形式，是否能在2—4小时完成"
  },
  "topic_opportunity": {
    "should_enter_pool": true,
    "user_problem": "准备覆盖的完整用户问题",
    "why_worth_testing": "为什么值得测试",
    "current_status": "ready|needs_learning|needs_research|needs_test|not_fit"
  },
  "next_action": {
    "action": "merge_demand|add_knowledge|save_packaging|save_evidence|send_to_topic|deep_research|manual_review|archive",
    "reason": "只写一个主要原因"
  }
}
```

不适用的对象使用 `null`，数组使用 `[]`，不要为了结构完整编造内容。

## 12. 技能调用

具体技能安装、触发条件和禁用规则以 `SKILL_ROUTING.md` 为唯一依据。

关键原则：

- 普通素材默认不调用完整爆款拆解 Skill；
- 只有高价值素材或人工点击“深度分析”时才调用；
- AI 新闻与产品更新先用实时信息 Skill 发现，再回原始来源核查；
- 标题、封面 Skill 只在正式内容项目阶段调用，不在素材阶段提前批量生成；
- 不使用模仿其他创作者个人文风的 Skill 代替用户自己的表达。

## 13. 写回检查

- 是否先分流，再分析；
- 是否把分类和利用价值分开；
- 是否只输出真正有用的部分；
- 核心需求是否具体到“谁、场景、阻碍、结果”；
- 需求证据是否诚实；
- 知识线索是否允许低门槛捕获、高门槛确认；
- 是否误把二手说法当事实；
- 是否在素材阶段生成了不必要的标题或完整脚本；
- 是否回答了“它对我的创作增加了什么”；
- 是否只给一个主要下一步；
- JSON 是否可解析；
- 是否避免把系统做成高级收藏夹。

处理结束只反馈：处理数量、各利用方式数量、进入知识核查数、保存包装数、进入选题池数、归档数、失败数和最新 commit。