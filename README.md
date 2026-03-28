# 🧠 飞书第二大脑 | Feishu Second Brain

> **让飞书文档自动记住一切，3 秒找到任何历史决策**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Feishu](https://img.shields.io/badge/Feishu-Lark-00D0B0?logo=feishu)](https://open.feishu.cn/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

---

## 🚀 快速开始

### 什么是飞书第二大脑？

飞书第二大脑是一个智能知识管理系统，自动将你的飞书文档、聊天记录、会议纪要进行**向量化存储**和**智能分类**，让你**3 秒内找到任何历史决策和讨论**。

**核心能力**:
- 📝 **自动记忆**: 飞书文档/聊天/会议自动归档
- 🔍 **语义搜索**: 不用记关键词，用自然语言搜索
- 🧠 **智能关联**: 自动关联相关文档和讨论
- 📊 **知识图谱**: 可视化展示知识结构

---

## ✨ 核心功能

### 1. 飞书文档自动记忆

```python
# 自动监控飞书文档变化
- 新建文档 → 自动提取关键信息
- 文档更新 → 自动记录变更历史
- 文档删除 → 自动备份到记忆库
```

### 2. 聊天记录智能归档

```python
# 从飞书群聊中提取关键信息
- 重要决策 → 自动标记并存储
- 任务分配 → 自动创建待办
- 文件分享 → 自动关联到相关项目
```

### 3. 会议纪要自动生成

```python
# 飞书日历会议结束后
- 自动提取会议要点
- 自动关联相关文档
- 自动生成待办事项
```

### 4. 语义搜索（核心亮点）

```python
# 不用记关键词，用自然语言搜索
搜索："上次讨论预算是什么时候？"
→ 自动找到相关会议记录和文档

搜索："张三负责的项目有哪些？"
→ 自动汇总所有相关项目和文档
```

---

## 💻 安装

### 方式一：一键安装（推荐）

```bash
# 克隆仓库
git clone git@github.com:<你的用户名>/feishu-second-brain.git

# 安装依赖
cd feishu-second-brain
pip install -r requirements.txt

# 配置
cp .env.example .env
# 编辑 .env 填入你的飞书 App ID 和 Secret

# 运行
python main.py
```

### 方式二：Docker（推荐企业用户）

```bash
docker-compose up -d
```

---

## 📖 使用文档

### 第一步：配置飞书应用

1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置权限（文档、消息、日历）
5. 填入 `.env` 文件

### 第二步：启动服务

```bash
python main.py
```

### 第三步：使用语义搜索

访问：http://localhost:8000/search

输入自然语言问题，例如：
- "上个月的销售数据在哪里？"
- "谁负责客服系统项目？"
- "上次关于预算的会议结论是什么？"

---

## 💰 版本与定价

### 基础版（免费）

✅ 飞书文档自动记忆  
✅ 基础语义搜索  
✅ 最多 1000 条记忆  
✅ 社区支持  

**适合**: 个人用户、小团队试用

---

### 专业版（¥299/月）

✅ 所有基础版功能  
✅ 聊天记录智能归档  
✅ 会议纪要自动生成  
✅ 无限记忆存储  
✅ 知识图谱可视化  
✅ 优先支持  

**适合**: 中小团队、知识密集型团队

[立即升级](https://github.com/sponsors/<你的用户名>)

---

### 企业版（¥4,999/月）

✅ 所有专业版功能  
✅ 私有部署  
✅ 定制开发  
✅ 专属技术支持  
✅ SLA 保障  
✅ 培训服务  

**适合**: 中大型企业、对数据安全要求高的团队

[联系销售](mailto:your-email@example.com)

---

## 🔧 技术架构

```
┌─────────────┐
│  飞书 API   │
│ (文档/消息) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  数据提取   │
│  & 清洗     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  向量化     │
│  (Embedding)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  向量数据库 │
│  (FAISS)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  语义搜索   │
│  & 推荐     │
└─────────────┘
```

---

## 📝 常见问题

### Q: 数据安全吗？

A: 非常安全！
- 所有数据存储在本地
- 不会上传到任何第三方服务器
- 支持私有部署
- 符合企业安全标准

### Q: 需要编程能力吗？

A: 不需要！
- 一键安装，开箱即用
- 提供 Web 界面
- 详细文档和视频教程

### Q: 可以定制吗？

A: 可以！
- 开源代码可自由修改
- 企业版提供定制开发
- 支持插件扩展

### Q: 支持其他平台吗？

A: 目前仅支持飞书，计划支持：
- 钉钉（2026 Q2）
- 企业微信（2026 Q3）
- Slack（2026 Q4）

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone git@github.com:<你的用户名>/feishu-second-brain.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📬 联系方式

- 📧 Email: your-email@example.com
- 💬 微信群：扫码加入（见下图）
- 🐛 Issue: [GitHub Issues](https://github.com/<你的用户名>/feishu-second-brain/issues)

---

## 🌟 致谢

感谢以下开源项目：
- [Feishu Open API](https://open.feishu.cn/)
- [LangChain](https://github.com/langchain-ai/langchain)
- [FAISS](https://github.com/facebookresearch/faiss)

---

**Made with ❤️ by OpenClaw Developer**

[![Star this repo](https://img.shields.io/github/stars/<你的用户名>/feishu-second-brain?style=social)](https://github.com/<你的用户名>/feishu-second-brain)
