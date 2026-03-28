# 飞书第二大脑 - 快速开始指南

## 🚀 5 分钟快速安装

### 方式一：本地安装（推荐新手）

```bash
# 1. 克隆仓库
git clone https://github.com/2316540487-eng/feishu-second-brain.git
cd feishu-second-brain

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的飞书 App ID 和 Secret

# 5. 启动服务
python main.py

# 6. 访问 Web 界面
打开浏览器：http://localhost:8000
```

### 方式二：Docker 安装（推荐企业用户）

```bash
# 1. 构建镜像
docker build -t feishu-second-brain .

# 2. 启动容器
docker run -d \
  -p 8000:8000 \
  -e FEISHU_APP_ID=your_app_id \
  -e FEISHU_APP_SECRET=your_app_secret \
  -v ./data:/app/data \
  --name feishu-second-brain \
  feishu-second-brain

# 3. 访问服务
打开浏览器：http://localhost:8000
```

---

## 📋 飞书应用配置

### 第一步：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 点击"创建应用"
3. 选择"企业自建应用"
4. 填写应用名称和描述

### 第二步：配置权限

在"权限管理"页面添加以下权限：
- ✅ 文档只读权限
- ✅ 消息只读权限
- ✅ 日历只读权限

### 第三步：获取凭证

在"凭证与基础信息"页面获取：
- App ID
- App Secret
- Verification Token

### 第四步：填入配置文件

编辑 `.env` 文件：
```
FEISHU_APP_ID=cli_xxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxx
FEISHU_VERIFICATION_TOKEN=xxxxxxxxxxxxx
```

---

## 🎯 使用示例

### API 调用示例

#### 1. 语义搜索

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "上个月的销售数据", "limit": 10}'
```

#### 2. 添加记忆

```bash
curl -X POST "http://localhost:8000/memory/add" \
  -H "Content-Type: application/json" \
  -d '{"content": "会议内容", "source": "feishu_doc"}'
```

#### 3. 查看统计

```bash
curl "http://localhost:8000/memory/stats"
```

### Python 调用示例

```python
from core import MemoryManager, SemanticSearch

# 添加记忆
memory = MemoryManager()
await memory.add(
    content="讨论了 Q2 销售目标",
    source="meeting_20260328"
)

# 搜索记忆
results = await memory.search("销售目标", limit=5)
for result in results:
    print(f"相关性：{result['score']}")
    print(f"内容：{result['content']}")
```

---

## 📊 版本对比

| 功能 | 基础版 | 专业版 | 企业版 |
|------|--------|--------|--------|
| 记忆数量 | 1000 条 | 无限 | 无限 |
| 搜索方式 | 关键词 | 向量搜索 | 向量搜索 |
| 聊天归档 | ❌ | ✅ | ✅ |
| 会议纪要 | ❌ | ✅ | ✅ |
| 知识图谱 | ❌ | ✅ | ✅ |
| 部署方式 | 本地 | 本地 | 私有部署 |
| 技术支持 | 社区 | 优先 | 专属 |
| 价格 | 免费 | ¥299/月 | ¥4,999/月 |

---

## ❓ 常见问题

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

---

## 🆘 获取帮助

- 📧 Email: 2316540487@qq.com
- 🐛 Issue: [GitHub Issues](https://github.com/2316540487-eng/feishu-second-brain/issues)
- 💬 微信群：扫码加入（见 README.md）

---

**祝你使用愉快！** 🎉
