#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书第二大脑 | Feishu Second Brain
让飞书文档自动记住一切，3 秒找到任何历史决策
"""

import asyncio
from core.memory import MemoryManager
from core.feishu_client import FeishuClient
from core.search import SemanticSearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="飞书第二大脑",
    description="智能知识管理系统",
    version="1.0.0"
)

class SearchQuery(BaseModel):
    query: str
    limit: int = 10

class MemoryResult(BaseModel):
    content: str
    source: str
    score: float
    created_at: str

@app.get("/")
async def root():
    return {
        "name": "飞书第二大脑",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/search", response_model=list[MemoryResult])
async def search(query: SearchQuery):
    """语义搜索"""
    try:
        search_engine = SemanticSearch()
        results = await search_engine.search(query.query, limit=query.limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/add")
async def add_memory(content: str, source: str):
    """添加记忆"""
    try:
        memory_manager = MemoryManager()
        await memory_manager.add(content, source)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/stats")
async def memory_stats():
    """记忆统计"""
    try:
        memory_manager = MemoryManager()
        stats = await memory_manager.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    """主函数"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
