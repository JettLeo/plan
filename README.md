# Excel Agent · AI 多智能体协同系统

> 基于 LangGraph 构建的 Supervisor + Workers 多智能体架构，支持 Excel 解析/校验/生成 + RAG 知识库检索 + Checkpoint 状态持久化

---

## 📌 项目背景

本项目是一个 **AI Agent 应用开发实战项目**，从 Java 后端转型 AI Agent 开发的完整实践产物。核心展示：

- **Supervisor + Workers 多智能体协同架构**
- **Excel 数据解析、校验、JSON 生成**
- **RAG 检索增强生成（ChromaDB + FAQ 知识库）**
- **Checkpoint 状态持久化（断点续传）**
- **企业级 Python 工程规范（类型注解、日志、配置管理）**

---

## 🛠️ 技术栈

| 类别       | 技术                             |
| :--------- | :------------------------------- |
| 语言       | Python 3.10+                     |
| Agent 框架 | LangGraph                        |
| Web 框架   | FastAPI                          |
| 向量数据库 | ChromaDB                         |
| 状态持久化 | SQLite (Checkpoint)              |
| 数据处理   | Pandas, OpenPyXL                 |
| 配置管理   | Pydantic Settings, python-dotenv |
| 日志       | logging                          |
| 包管理     | pyproject.toml                   |

---

## 📁 项目结构

```text
excel-agent/
├── app/                         # 主应用模块
│   ├── agents/                  # Agent 定义
│   │   └── multi_agent.py       # 主 Agent（Supervisor + 5 Workers）
│   ├── core/                    # 核心配置
│   │   └── config.py            # 统一配置管理
│   └── rag/                     # RAG 模块
│       ├── __init__.py
│       └── vector_store.py      # ChromaDB 向量存储封装
├── data/                        # 数据目录
│   └── faq.xlsx                 # FAQ 知识库样例
├── scripts/                     # 工具脚本
│   ├── generate_faq.py          # 生成 FAQ 样例数据
│   ├── load_faq_data.py         # 加载 FAQ 到向量库
│   └── create_sample_excel.py   # 生成样例 Excel
├── tests/                       # 测试脚本
│   └── test_retrieve.py         # 检索功能测试
├── .env                         # 环境变量（不上传）
├── .gitignore
├── pyproject.toml               # 项目依赖
└── README.md
```
