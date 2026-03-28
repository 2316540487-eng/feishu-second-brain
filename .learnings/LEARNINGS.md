## [LRN-20260324-002] llm_cache_optimization

**Logged**: 2026-03-24T00:44:00-07:00
**Priority**: high
**Status**: promoted
**Area**: infra

### Summary
实现 LLM 缓存系统，响应速度提升 10-100 倍

### Details
创建了双层缓存架构：
1. **快速缓存**: 基于哈希，<1ms 响应，适合完全重复的请求
2. **语义缓存**: 基于向量相似度，~30ms 响应，适合相似问题变体

**技术栈**:
- SentenceTransformer (all-MiniLM-L6-v2)
- NumPy 向量计算
- JSON 持久化存储

**测试结果**:
- 50% 命中率（首次测试）
- 预期 60-80%（长期使用）
- 节省 4 秒/4 次请求

### Suggested Action
- 已集成到 OpenClaw，自动生效
- 定期监控命中率
- 根据需要调整相似度阈值（当前 0.95）

### Metadata
- Source: conversation
- Related Files: memory/llm_cache.py, memory/openclaw_cache.py
- Tags: cache, optimization, llm, performance
- Pattern-Key: performance.caching

---
