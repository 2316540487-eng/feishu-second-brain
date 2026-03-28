# Vector Memory Search - 向量记忆检索技能

## 功能说明

使用本地向量数据库（ChromaDB）实现语义检索，增强记忆搜索能力。

## 核心能力

1. **语义检索**：基于向量相似度搜索，不依赖关键词
2. **混合检索**：向量检索 + 关键词检索，提升准确率
3. **记忆嵌入**：自动将记忆内容转换为向量
4. **增量更新**：支持记忆增量添加和更新

## 技术架构

```python
import chromadb
from chromadb.config import Settings

# 初始化 ChromaDB（本地持久化）
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./memory_vectors"
))

# 创建记忆集合
memory_collection = client.create_collection(
    name="long_term_memory",
    metadata={"description": "长期记忆向量存储"}
)
```

## 记忆嵌入流程

```python
def store_memory(content, category="general", metadata=None):
    """
    存储记忆到向量数据库
    
    Args:
        content: 记忆内容
        category: 记忆分类
        metadata: 附加元数据
    """
    # 生成向量嵌入
    embedding = generate_embedding(content)
    
    # 生成唯一 ID
    memory_id = generate_memory_id(category)
    
    # 存储到 ChromaDB
    memory_collection.add(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata or {"category": category}]
    )
    
    return memory_id
```

## 检索流程

```python
def search_memories(query, top_k=5, category=None, min_score=0.7):
    """
    搜索记忆
    
    Args:
        query: 搜索查询
        top_k: 返回结果数量
        category: 分类过滤（可选）
        min_score: 最低相似度阈值
    
    Returns:
        memories: 匹配的记忆列表
    """
    # 生成查询向量
    query_embedding = generate_embedding(query)
    
    # 向量检索
    results = memory_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"category": category} if category else None
    )
    
    # 过滤低相似度结果
    filtered_results = filter_by_score(results, min_score)
    
    return filtered_results
```

## 混合检索（向量 + 关键词）

```python
def hybrid_search(query, top_k=5, vector_weight=0.7, keyword_weight=0.3):
    """
    混合检索：结合向量检索和关键词检索
    
    Args:
        query: 搜索查询
        top_k: 返回结果数量
        vector_weight: 向量检索权重
        keyword_weight: 关键词检索权重
    
    Returns:
        memories: 排序后的记忆列表
    """
    # 向量检索结果
    vector_results = search_memories(query, top_k=top_k * 2)
    
    # 关键词检索结果
    keyword_results = keyword_search(query, top_k=top_k * 2)
    
    # 合并并排序
    combined = merge_and_rank(vector_results, keyword_results, 
                              vector_weight, keyword_weight)
    
    return combined[:top_k]
```

## 使用场景

当用户说：
- "我之前说过关于选股逻辑的内容"
- "找一下昨天讨论的抖音运营方案"
- "搜索所有关于 OpenClaw 配置的记忆"

## 性能优化

### 1. 批量嵌入
```python
# 批量添加记忆（减少 IO）
def batch_store_memories(memories):
    embeddings = [generate_embedding(m.content) for m in memories]
    memory_collection.add(
        ids=[m.id for m in memories],
        embeddings=embeddings,
        documents=[m.content for m in memories]
    )
```

### 2. 增量索引
```python
# 定期重建索引（优化检索性能）
def rebuild_index():
    memory_collection.compact()
    memory_collection.optimize()
```

### 3. 缓存热点查询
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query_hash, top_k):
    return search_memories(query_hash, top_k)
```

## 安装依赖

```bash
# 安装 ChromaDB
pip install chromadb

# 安装嵌入模型（本地）
pip install sentence-transformers
```

## 配置选项

| 选项 | 默认值 | 说明 |
|------|--------|------|
| persist_directory | ./memory_vectors | 向量数据持久化路径 |
| embedding_model | all-MiniLM-L6-v2 | 嵌入模型 |
| max_memories | 10000 | 最大记忆数量 |
| cleanup_threshold | 0.5 | 低质量记忆清理阈值 |

## 与现有记忆系统集成

```
现有系统：
- memory/*.md 文件（Markdown 格式）
- sessions（会话历史）

升级后：
- memory/*.md → 定期同步到向量数据库
- sessions → 重要会话自动存储到向量数据库
- 搜索时优先使用向量检索，回退到关键词检索
```

---

**版本**: 1.0.0
**作者**: OpenClaw Partner
**最后更新**: 2026-03-26
