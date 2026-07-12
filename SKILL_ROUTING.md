# 工作台 Skill 路由 · V4.1

## 0. 目的

本文件是工作台调用外部 Skill 的唯一路由表。

Skill 用来提高某一个环节的质量，不是用来让流程显得复杂。每次调用前先问：

> 不调用这个 Skill，当前任务会明显变差吗？

不会明显变差，就不要调用。

## 1. 总规则

1. 静态 `workbench.html` 不能直接假装调用 Agent Skill；
2. V1 由工作台组装任务包，用户复制给 ChatGPT / Codex / Claude Code 等 Agent；
3. Agent 执行 Skill 后，把结构化结果导回工作台；
4. 已有本地辅助服务时，才允许实现真实一键调用；
5. 不为每条普通素材调用完整 Skill；
6. 重要事实仍需回原始来源核查，Skill 输出不是事实豁免；
7. 不复制其他创作者的个人文风作为用户默认表达；
8. Skill 更新可能改变行为，Codex 实施前应重新读取最新版 `SKILL.md`；
9. 外部 Skill 不复制进本仓库，默认通过官方仓库或安装入口引用；
10. 每次 Skill 运行建议记录：Skill 名称、来源、时间、输入素材 ID、输出文件和核查来源。

## 2. 路由总表

| 阶段 | Skill | 使用级别 | 什么时候调用 | 什么时候禁止调用 |
|---|---|---:|---|---|
| AI编辑部发现新信息 | `aihot` | 推荐 | 查询最近 AI 精选、产品/模型/技巧、关键词或公司动态 | 不把摘要直接当正式事实；不作为工作台唯一信息源 |
| 高价值素材深拆 | `cosmos-xiaohongshuvideo-breakdown` | 按需 | 用户点“深度分析”、素材数据好且材料充分、准备进入内容项目 | 普通素材轻分析、只有一个标题且无数据时不调用完整流程 |
| 深度研究产品/公司/概念 | `hv-analysis` | 重型可选 | 用户明确选择深度研究，且需要历史演进、竞品与系统判断 | 日常资讯、简单工具说明、两小时内短内容不自动调用 |
| 正式内容标题 | `xhs-title` | 按需 | 目标用户、核心承诺、知识证据和内容结构已经确定 | 素材入库阶段、内容尚未学懂、没有可兑现价值时禁止调用 |
| 正式封面或旧封面诊断 | `cover-anchor-system` | 按需 | 标题已定，需要封面信息层级、视觉锚点或改版方案 | 不强制套固定视觉风格；不替代账号自己的视觉一致性 |
| 开发完成后的项目收尾 | `neat-freak` | 开发必做 | Codex 完成本阶段代码、文档和规则变更后 | 不用于日常素材分析或内容写作 |
| 卡兹克公众号文风 | `khazix-writer` | 禁用为默认 | 仅用户明确要求研究其写作方法时可阅读 | 不用于小红书短内容，不以卡兹克个人口吻代写用户内容 |
| 半自动视频剪辑 | 暂无指定 Skill | 暂缓 | V4.1 只生成剪辑标注 | 不声称已经有可靠自动剪辑 Skill，不与本次改版绑定 |

# 3. AI HOT：AI编辑部信息入口

## 3.1 来源

- 网站：`https://aihot.virxact.com/`
- Skill 安装入口：`https://aihot.virxact.com/aihot-skill/`
- GitHub：`https://github.com/KKKKhazix/khazix-skills/tree/main/aihot`

安装提示：

```text
帮我安装这个 skill：https://aihot.virxact.com/aihot-skill/
```

## 3.2 适合做什么

- 获取最近 24 小时或最近几天的 AI 精选；
- 按模型、产品、行业、论文、技巧分类查询；
- 查询 OpenAI、Anthropic、Google、Codex、Sora 等关键词；
- 获取当前多信源热点；
- 为 AI编辑部提供“今天有什么值得进一步研究”的候选。

## 3.3 工作台中的正确位置

只用于 **AI编辑部 → 信息发现**。

推荐流程：

```text
AI HOT 拉取候选
→ 按账号承诺和用户任务筛噪
→ 打开原始链接核查
→ 判断是短期信息、长期知识还是需求机会
→ 再进入知识库或选题与学习
```

## 3.4 查询规则

- 宽泛问题如“今天 AI 圈有什么”默认取精选和语义时间窗；
- 用户明确说“日报”才取日报；
- 用户明确说“全部、完整、全量”才取全部；
- 主题、公司和产品优先用服务端关键词搜索；
- 不一次拉大量内容回来再本地粗暴过滤；
- 日常只保留少量真正与账号和用户有关的条目。

## 3.5 事实核查规则

AI HOT 是聚合摘要和发现入口，进入正式知识或内容前必须：

1. 保留 AI HOT 条目链接；
2. 保留第三方原文 URL；
3. 优先打开官方博客、官方文档、GitHub Release 或论文；
4. 区分“原文事实、AI HOT 摘要、工作台判断”；
5. 没有核实的内容不得写成确定结论；
6. 服务不可用时允许编辑部为空，不阻塞工作台。

## 3.6 编辑部导入建议

Agent 结果写入：

```text
editorial/daily/YYYY-MM-DD.json
```

每条建议包含：

```json
{
  "id": "稳定ID",
  "title": "标题",
  "category": "model|product|industry|paper|tips",
  "published_at": "ISO datetime",
  "aihot_url": "AI HOT详情链接",
  "original_url": "原文链接",
  "summary": "发生了什么",
  "user_task": "它影响什么用户任务",
  "account_value": "为什么与账号有关",
  "verification_status": "discovered|source_checked|tested",
  "recommended_action": "ignore|knowledge|demand|research|topic"
}
```

前台不展示大批未核实内容；默认只显示已筛选的少量候选。

# 4. Cosmos：高价值素材深度拆解

## 4.1 来源

- GitHub：`https://github.com/Cosmoslmj/cosmos-xiaohongshuvideo-breakdown`

安装提示：

```text
帮我安装这个 skill：https://github.com/Cosmoslmj/cosmos-xiaohongshuvideo-breakdown
```

## 4.2 使用位置

- 素材总览 → 用户手动点击“深度分析”；
- 同一需求已有多条高数据内容，需要比较；
- 选题与学习 → 准备正式制作前，分析 1—3 条真实参考。

## 4.3 只取有用能力

重点调用：

- 目标用户；
- 前 3 秒；
- 内容推进；
- 标题与封面点击理由；
- 收藏、评论、分享原因；
- 可迁移与不可迁移部分；
- 已确认事实与推断区分。

## 4.4 项目覆盖规则

本项目的 `ANALYSIS_PROMPT.md` 优先级高于外部 Skill。

因此必须覆盖外部 Skill 中以下不适合本项目的默认行为：

- 不强制从一条素材延展 5—10 条系列；
- 不在素材阶段直接生成大量迁移标题或完整稿；
- 不强制每条输出评分表；
- 不把“爆款”自动等同于适合用户账号；
- 先判断需求与创作增量，再决定是否进入选题。

# 5. HV Analysis：重型深度研究

## 5.1 来源

- GitHub：`https://github.com/KKKKhazix/khazix-skills/tree/main/hv-analysis`

安装提示：

```text
帮我安装这个 skill：https://github.com/KKKKhazix/khazix-skills/tree/main/hv-analysis
```

## 5.2 适合场景

- 想系统搞懂一个产品、公司、技术或概念；
- 需要追踪历史演进并与竞品横向比较；
- 准备做重要专题，而不是追一条即时新闻；
- 结论会影响账号长期内容方向或重要实测投入。

## 5.3 禁止过度调用

它是重型研究 Skill，默认产出很长，不能用于：

- 每日 AI编辑部；
- 普通 Skill 介绍；
- 60 秒工具分享；
- 只需要查一个官方事实的问题；
- 用户只能投入 2—4 小时的日常选题。

选题卡必须明确显示“重型研究”，由用户主动选择后才调用。

# 6. XHS Title：正式标题候选

## 6.1 来源

- GitHub：`https://github.com/ren644/xhs-title-skill`

安装提示：

```text
帮我安装这个 skill：https://github.com/ren644/xhs-title-skill
```

## 6.2 调用前置条件

必须先确定：

- 本次给谁看；
- 用户正在解决什么任务；
- 内容的真实结果或价值；
- 有哪些证据；
- 完整逐字稿或内容结构。

缺少上述信息时，不调用标题 Skill 掩盖内容空缺。

## 6.3 项目标题规则覆盖

外部 Skill 只提供候选方法，最终必须符合：

- 20 个汉字是上限，不是越短越好；
- 标题必须语义完整；
- 允许适度夸张、情绪、冲突和悬念；
- 不得编造结果、功能和数据；
- 标题与封面互补；
- 不生成没对象、没场景、没结果的半句话；
- 最终只保留 1 个主标题和最多 2 个备用，不把 8 个候选全部塞给用户。

# 7. Cover Anchor：封面设计与诊断

## 7.1 来源

- GitHub：`https://github.com/ponyodong2026/ponyo-cover-anchor-system`
- Skill 路径：`cover-anchor-system/SKILL.md`

安装提示：

```text
帮我安装这个 skill：https://github.com/ponyodong2026/ponyo-cover-anchor-system/tree/main/cover-anchor-system
```

## 7.2 使用位置

- 选题与学习 → 标题确定后生成封面方案；
- 复盘库 → 点击率低时诊断旧封面；
- 真实工具、工作台和结果类内容优先使用截图型视觉锚点。

## 7.3 项目覆盖规则

- 使用“信息密度 × 视觉锚点”的判断逻辑；
- 不强制采用 Skill 的固定配色和视觉风格；
- 用户现有账号视觉一致性优先；
- 封面大字应比笔记标题更短；
- 优先真实截图、成品和结果证据；
- 需要生图时输出完整提示词，但 V4.1 工作台不直接生成图片；
- 不添加他人水印、Logo 或虚假数据。

# 8. Neat Freak：Codex 开发收尾

## 8.1 来源

- GitHub：`https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak`

安装提示：

```text
帮我安装这个 skill：https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak
```

## 8.2 调用时间

Codex 完成 V4.1 代码、测试和文档后，最后执行一次：

```text
/neat
```

目标：

- 检查代码与 `WORKBENCH_SPEC.md` 是否一致；
- 检查 `CODEX_HANDOFF.md` 是否过期；
- 检查 README、规则和真实实现是否冲突；
- 清理死引用和重复文档；
- 输出最终变更摘要。

它不能代替功能测试，也不能自行改变用户确认的产品逻辑。

# 9. 为什么不使用 Khazix Writer 作为默认写作 Skill

`khazix-writer` 是卡兹克个人公众号长文文风 Skill，目标是以其个人口吻写长文。

本项目不把它用于默认创作，原因：

- 用户要形成自己的声音；
- 当前主要是小红书短视频和录屏内容；
- 模仿其他创作者个人口吻会削弱原创性；
- 它可以作为研究“真人感、个人经历和观点边界”的材料，但不能直接代写。

正式逐字稿由本项目内容任务包生成，必须以用户本人理解、真实经验、自己的声音和可展示证据为核心。

# 10. 工作台任务包格式

当网页不能直接调用 Skill 时，生成如下任务包：

```text
任务阶段：素材深拆 / AI资讯发现 / 深度研究 / 标题 / 封面
建议 Skill：<skill-name>
Skill 来源：<url>
用户目标：<这一步要解决什么>
输入材料：<素材ID、需求ID、知识ID、内容项目ID>
必须遵守：<本项目覆盖规则>
期望输出：<结构化字段>
保存位置：<文件或工作台对象>
```

用户复制给 Agent 后，返回结果必须能绑定原对象 ID，不能产生无法追溯的孤立文本。

# 11. Codex 实施检查

- 已读取本文件和每个将安装 Skill 的最新版 `SKILL.md`；
- 已在 UI 中区分“生成任务包”和“真实调用”；
- 没有用前端字符串替换伪装 Skill；
- AI HOT 只作为发现入口，保留原文核查；
- 普通素材不会自动调用 Cosmos 深拆；
- 标题和封面 Skill 只在正式内容阶段调用；
- HV Analysis 标记为重型可选；
- 没有启用 Khazix Writer 代替用户表达；
- V4.1 未声称实现自动剪辑 Skill；
- 开发完成后已执行 Neat Freak 收尾。
