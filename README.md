# 医学免疫学学习系统

[中文](README.md) | [English](README.en.md)

一个面向《医学免疫学》（人卫第9版）学习场景的离线系统：提供 Web 学习界面 + CLI 自测工具 + 题库/SRS/错题追踪 + 会话与进度文档沉淀。

> 合规说明：本项目不包含教材原文，内容以自写总结、概念化表达、题目与学习提示为主。

## 项目深度分析（架构与能力）

### 1) 产品定位
- 面向医学生/考研/住培早期学习者，强调“概念框架 + 高频自测 + 错题复盘 + 间隔复习”。
- 既支持浏览式学习（知识卡片、模块导航），也支持任务式学习（刷题、复习、统计）。

### 2) 技术架构
- **后端服务**：`app.py`（Flask），提供 REST API（题库、练习、知识库、学习教练、进度）。
- **核心引擎**：`immuno_study/` 下的 `deck.py`（题库校验）、`engine.py`（判题）、`store.py`（SRS/错题/做题日志）。
- **数据层**：本地 JSON/JSONL，无数据库依赖，易备份、可离线。
- **前端层**：`templates/index.html` + `static`（原生 JS/CSS 交互）。
- **多端扩展**：含 `android/` 目录与构建文档，支持 Android 交付链路。

### 3) 学习模型设计
- **知识模型**：`immuno_study/knowledge.py` 维护 12 个模块（总论、固有免疫、补体、MHC、抗体、T/B 细胞、细胞因子、超敏、自免、免疫缺陷、肿瘤与移植等）。
- **练习模型**：`decks/people9-core.json` 定义 MCQ + 简答题，含答案、解析、标签。
- **记忆模型**：轻量 SRS（间隔、难度因子、到期日、连续答对）驱动复习。
- **教练模型**：Socratic 流程（先探测理解，再聚焦讲解，再做核验）。

### 4) 当前优势与可提升点
- **优势**：结构完整、离线可用、可追踪、文档化学习流程明确。
- **可提升**：短答判题目前为归一化精确匹配；后续可升级同义词/关键词评分或语义评分。

## 快速开始（Windows / PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Web 模式
python app.py
# 浏览器打开 http://127.0.0.1:5000
```

```powershell
# CLI 模式
python -m immuno_study --help
python -m immuno_study quiz --deck .\decks\people9-core.json --n 10
python -m immuno_study review --deck .\decks\people9-core.json --n 10
python -m immuno_study stats
```

## 目录结构

```text
medical-immunology-study/
├─ app.py
├─ immuno_study/
│  ├─ cli.py
│  ├─ deck.py
│  ├─ engine.py
│  ├─ knowledge.py
│  └─ store.py
├─ decks/
│  └─ people9-core.json
├─ docs/
├─ sessions/
├─ progress/
├─ android/
└─ tests/
```

## 文档导航

- 使用说明：`docs/USER_GUIDE.md`
- 功能清单：`docs/FEATURES.md`
- 贡献指南：`CONTRIBUTING.md`
- 学习进度总表：`progress/immunology-study-tracker.md`
- 会话模板：`sessions/SESSION-TEMPLATE.md`
- Android 说明：`docs/android/ANDROID_README.md`、`android/README.md`

## 推荐教材与学习资源（全网补充）

以下资源优先选择权威机构与可长期访问页面：

### 核心教材/参考
- NCBI Bookshelf（Janeway《Immunobiology》入口，受版权限制仅支持检索）：  
  <https://www.ncbi.nlm.nih.gov/books/NBK10757/>

### 免疫与疫苗公共卫生权威资料
- WHO 免疫培训总入口：  
  <https://www.who.int/teams/immunization-vaccines-and-biologicals/essential-programme-on-immunization/training>
- WHO 通用培训资料（Immunization in practice、AEFI 等）：  
  <https://www.who.int/teams/immunization-vaccines-and-biologicals/essential-programme-on-immunization/training/general>
- CDC Pink Book（疫苗可预防疾病流行病学与预防，课程教材）：  
  <https://www.cdc.gov/pinkbook/hcp/table-of-contents/index.html>

### 教学法与课程设计资源
- AAI 教学资源（本科免疫课程建议、教学工具与活动案例）：  
  <https://www.aai.org/Education/Teaching-Resources>
- NIH 免疫系统概览（基础回顾入口）：  
  <https://www.niaid.nih.gov/research/immune-system-overview>

### 免费视频/公开课入口
- Khan Academy 免疫学入口（适合打基础与快速回顾）：  
  <https://www.khanacademy.org/science/biology/immunology>

## 教材融合建议（第9版联动）

- 在 `syllabus/outline.md` 为每个模块补充“教材章/页码”映射。
- 扩展 `decks/people9-core.json` 时保持字段一致：`id`、`type`、`tags`、`explain`。
- 每次学习后同步更新：
  - `sessions/YYYY-MM-DD/session-notes.md`
  - `progress/immunology-study-tracker.md`

## 模块-教材-外部资源对照（建议版）

> 说明：本节不替代你的纸质教材；“教材章节/页码”请按你手头版本自行回填。

- **module01（总论与基本概念）**
  - 教材联动：总论、免疫系统组成、抗原基础
  - 外部补充：NIH 免疫系统概览（建立大框架）
- **module02（固有免疫）**
  - 教材联动：PAMP/DAMP、PRR、炎症细胞与过程
  - 外部补充：Khan Academy 免疫学基础视频（快速建立先天/适应性差异）
- **module03（补体系统）**
  - 教材联动：三条激活途径、关键片段与调节机制
  - 外部补充：AAI 教学资源中的概念图/教学工具（适合对比记忆）
- **module04（MHC 与抗原呈递）**
  - 教材联动：MHC I/II、内外源通路、交叉呈递
  - 外部补充：Janeway 相关条目（用于英文术语对照）
- **module05（抗体/免疫球蛋白）**
  - 教材联动：Ig 分类、结构与效应功能
  - 外部补充：Khan Academy（抗体与体液免疫入门）
- **module06（T 细胞免疫）**
  - 教材联动：双信号/三信号、Th 分化、CTL、检查点
  - 外部补充：AAI 教学案例（主动学习、概念图工具）
- **module07（B 细胞与体液免疫）**
  - 教材联动：TD/TI 抗原、生发中心、类别转换与亲和力成熟
  - 外部补充：Khan Academy + NIH（基础回顾）
- **module08（细胞因子）**
  - 教材联动：IL/IFN/TNF/TGF 核心网络
  - 外部补充：AAI 教学资源（概念关联与课堂活动）
- **module09（超敏反应）**
  - 教材联动：I-IV 型机制与代表性疾病
  - 外部补充：NIH 免疫综述（联系免疫病理）
- **module10（免疫耐受与自身免疫）**
  - 教材联动：中枢/外周耐受、Treg、自免机制
  - 外部补充：Janeway 条目与 NIH 概览（机制复盘）
- **module11（免疫缺陷病）**
  - 教材联动：原发/继发免疫缺陷、病原易感谱
  - 外部补充：WHO 培训资料中的免疫实践章节（临床公共卫生视角）
- **module12（肿瘤免疫与移植免疫）**
  - 教材联动：免疫逃逸、检查点抑制剂、移植排斥
  - 外部补充：CDC Pink Book（疫苗学与免疫实践扩展）、WHO EPI 资源

## 测试

```powershell
python -m unittest discover -v -s .\tests
```

## License

本项目采用 [Apache License 2.0](LICENSE)。

