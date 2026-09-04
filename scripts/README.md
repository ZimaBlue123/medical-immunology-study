# Scripts 目录规范

本目录统一收纳本项目所有的 Python (`.py`) 源码与脚本工具，**严禁在根目录或其他目录散落 Python 文件**。

## 目录结构

```text
scripts/
├─ app.py                    # Flask Web 应用服务
├─ convert_to_android.py     # 题库与知识库导出为 Android JS 资源脚本
├─ run_cli.py                # 命令行自测与复习 CLI 入口
└─ immuno_study/             # 免疫学学习系统核心 Python 包
   ├─ __init__.py
   ├─ __main__.py
   ├─ cli.py                 # CLI 参数解析与交互逻辑
   ├─ deck.py                # 题库加载与校验
   ├─ engine.py              # 判题与文本归一化算法
   ├─ knowledge.py           # 12 大模块知识库与考点
   └─ store.py               # SRS 间隔重复与做题历史存储
```

## 新建 Python 文件规范
后续如有任何新建的 `.py` 脚本、数据转换工具、后端扩展或维护脚本，**必须全部归类存放在本 `scripts/` 目录或其子目录中**。
