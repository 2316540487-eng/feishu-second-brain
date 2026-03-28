# API 文档

## 基础信息

**Base URL**: `http://localhost:8000`

---

## 接口列表

### 1. 健康检查

**GET** `/`

检查服务状态

**响应示例**:
```json
{
  "name": "飞书第二大脑",
  "version": "1.0.0",
  "status": "running"
}
```

---

### 2. 语义搜索

**POST** `/search`

搜索记忆

**请求参数**:
```json
{
  "query": "搜索内容",
  "limit": 10
}
```

**响应示例**:
```json
[
  {
    "id": "20260328010000000001",
    "content": "会议讨论了 Q2 销售目标",
    "source": "meeting_20260328",
    "score": 0.95,
    "created_at": "2026-03-28T01:00:00"
  }
]
```

---

### 3. 添加记忆

**POST** `/memory/add`

添加新的记忆

**请求参数**:
```json
{
  "content": "记忆内容",
  "source": "feishu_doc",
  "metadata": {
    "doc_id": "xxx",
    "author": "张三"
  }
}
```

**响应示例**:
```json
{
  "status": "success",
  "memory_id": "20260328010000000001"
}
```

---

### 4. 记忆统计

**GET** `/memory/stats`

获取记忆统计信息

**响应示例**:
```json
{
  "total_memories": 500,
  "max_memories": 1000,
  "usage_percent": 50.0
}
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

**错误响应示例**:
```json
{
  "detail": "已达到记忆数量限制 (1000)"
}
```

---

## 使用示例

### Python

```python
import requests

# 搜索
response = requests.post(
    "http://localhost:8000/search",
    json={"query": "销售数据", "limit": 10}
)
results = response.json()

# 添加记忆
response = requests.post(
    "http://localhost:8000/memory/add",
    json={"content": "会议内容", "source": "meeting"}
)
```

### cURL

```bash
# 搜索
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "销售数据", "limit": 10}'

# 添加记忆
curl -X POST "http://localhost:8000/memory/add" \
  -H "Content-Type: application/json" \
  -d '{"content": "会议内容", "source": "meeting"}'
```

---

## 更新日志

### v1.0.0 (2026-03-28)
- ✅ 初始版本发布
- ✅ 基础记忆管理
- ✅ 关键词搜索
- ✅ RESTful API

### v1.1.0 (计划中)
- 🔜 向量搜索
- 🔜 聊天归档
- 🔜 会议纪要

---

**API 版本**: v1.0.0  
**最后更新**: 2026-03-28
