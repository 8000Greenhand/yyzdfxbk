# V4.1 历史素材分析迁移记录

## 完成范围

已由 ChatGPT 逐条读取 14 条历史素材的 `meta.json`、`transcript.md` 和旧 `analysis.md`，并将全部 `analysis.md` 重写为 `schema_version: "4.1"`。

本次只更新分析内容：

- 未修改任何 `transcript.md`；
- 未删除原素材；
- 未让 Codex 代替内容判断；
- 未调用完整深度拆解批量生成长报告；
- 未从单条素材直接生成完整逐字稿；
- Git 历史保留旧分析，可随时回滚。

## 迁移结果

- V4.1 素材分析：14 条
- 进入需求合并：3 条
- 进入知识核查：5 条
- 进入选题与学习：3 条
- 进入深度研究：2 条
- 仅保存包装参考：1 条
- 直接归档：0 条
- 具备正式选题机会：11 条，其中只有 1 条当前标记为 `ready`，其余需要学习、核查或实测

> 知识线索数量需要工作台去重后再统计，不能直接按每条素材中的条目相加。

## 当前最接近可制作的选题

来源：`items/抖音_recvoRjgc9OJmv`

用户问题：

> 为什么 Codex 能帮我做工作台，却不能替我决定账号该发什么？

该素材被标记为 `ready`，原因是用户已经有真实的 ChatGPT、Codex 和工作台协作经历。制作前只需补充一个 Codex 判断失败、明确规则后执行成功的真实对比。

## Codex 只需做的下一步

Codex 不再分析素材，只执行：

1. 拉取 GitHub 最新 main 分支；
2. 将最新 `items/**/analysis.md` 同步到本地 `transcript_repo`；
3. 修正下面两处 V4.1 解析兼容；
4. 重新运行本地工作台生成脚本；
5. 核对 14 条素材均识别为 V4.1，解析失败数为 0；
6. 提交更新后的工作台快照与验收结果。

## 必须修正的两个解析映射

### 1. 主分类枚举

`ANALYSIS_PROMPT.md` 的正式 V4.1 枚举是：

```text
skill_tools
ai_knowledge
operations_content
workplace_efficiency
personal_growth
packaging_only
manual_pending
```

当前 `workbench_app/build_local_workbench.py` 的 `CATEGORY_DEFAULTS` 仍使用部分旧缩写，例如：

```text
ops_content
work_efficiency
packaging_reference
uncategorized
```

必须让解析器原生识别正式 V4.1 枚举，同时保留旧缩写作为兼容别名。否则 `operations_content`、`workplace_efficiency`、`personal_growth` 等可能被错误放进“待分类”。

建议别名：

```text
operations_content -> ops_content / 运营与内容
workplace_efficiency -> work_efficiency / 职场效率
packaging_only -> packaging_reference / 包装参考
manual_pending -> uncategorized / 待分类
```

内部 key 可以继续沿用旧 key，但不能丢失 V4.1 分类含义。

### 2. 下一步动作枚举

`ANALYSIS_PROMPT.md` 的正式动作是：

```text
send_to_topic
```

当前工作台映射使用：

```text
enter_topic
```

解析器必须同时接受：

```text
send_to_topic
enter_topic
```

并统一显示为“进入选题”。新分析写入以 `send_to_topic` 为准，`enter_topic` 仅保留旧数据兼容。

## 验收要求

重新生成后至少确认：

- 总素材仍为 14 条；
- 14 条均读取到 `schema_version: "4.1"`；
- 旧的 4 条 JSON 解析失败归零；
- “运营与内容”“个人成长”等分类不再大量落入待分类；
- 知识库显示来源状态：仅提及 / 已找到来源 / 已实测；
- 选题与学习中能看到 11 条候选，但默认优先展示可执行度最高的少量内容；
- 今日行动优先显示 ready 项，不把大量待研究内容同时推给用户；
- AI 编辑部仍可为空，这与历史素材迁移无关；
- 不修改页面产品结构，不重新分析素材。
