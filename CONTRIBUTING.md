# 贡献指南（Contributing）

感谢你为 `medical-immunology-study` 做贡献。本项目强调“可学习、可追踪、可复用”，请按以下规范提交内容。

## 1. 贡献范围

欢迎提交：
- 题库扩展（`decks/*.json`）
- 知识库优化（`immuno_study/knowledge.py`）
- 文档改进（`README.md`、`README.en.md`、`docs/*.md`）
- 功能增强与缺陷修复（`immuno_study/*.py`、`app.py`）

暂不建议：
- 提交教材原文或大段近似改写内容
- 提交含个人隐私/敏感信息的数据文件

## 2. 开发环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m unittest discover -v -s .\tests
```

## 3. 题库提交规范（重点）

题库文件：`decks/people9-core.json`

每张卡片至少包含：
- `id`：全局唯一，例如 `core-0051`
- `type`：`mcq` 或 `short`
- `tags`：至少 1 个模块标签（如 `module06`）
- `explain`：简要解析（建议说明“为什么对/错”）

`mcq` 题目字段：
- `stem`、`choices`（至少 2 项）、`answer_index`

`short` 题目字段：
- `prompt`、`answer`

提交前请确保：
- JSON 语法正确
- `id` 无重复
- 标签与模块语义一致

## 4. 标签规范（建议统一）

### 4.1 模块主标签（必选）
- `module01` 到 `module12`

### 4.2 主题标签（可选，建议）
- 机制标签：如 `innate`、`adaptive`、`complement`、`mhc`、`tcell`、`bcell`
- 应用标签：如 `vaccine`、`tumor`、`transplant`、`autoimmune`

### 4.3 命名建议
- 优先小写英文短词，必要时可补充中文标签
- 避免同义多写（例如同一概念只保留一套主标签）

## 5. 知识库内容规范

修改 `immuno_study/knowledge.py` 时：
- 优先补“定义 + 关键点 + 常见混淆 + 临床关联”
- 避免无来源的绝对化结论
- 不确定内容请在文档中明确“需按教材核对”

## 6. 文档规范

- 中文主文档：`README.md`
- 英文文档：`README.en.md`
- 若改动中文主文档中的结构性内容，建议同步更新英文版
- 外链优先引用权威机构（WHO、CDC、NIH、NCBI、AAI）

## 7. 提交流程建议

1. 新建分支：`feat/...`、`fix/...`、`docs/...`
2. 完成修改并本地运行测试
3. 自查是否引入与本任务无关的大改动
4. 发起 PR，描述：
   - 变更目的（Why）
   - 主要改动（What）
   - 验证方式（How tested）

## 8. Pull Request 检查清单

- [ ] 测试通过（`python -m unittest discover -v -s .\tests`）
- [ ] 新增题目含 `explain` 与合理 `tags`
- [ ] 未提交运行时产物（如 `immuno_study/data/`）
- [ ] README 与相关文档已同步
- [ ] 不包含教材版权原文

## 9. License 与合规

本仓库采用 `Apache-2.0`。提交代码即表示你同意以该协议授权你的贡献。
