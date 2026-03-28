#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆管理器 - 负责记忆的存储、检索和管理
"""

import asyncio
from datetime import datetime
from typing import Optional
import json
import os

class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, storage_path: str = "data/memories"):
        self.storage_path = storage_path
        self.max_memories = 1000  # 基础版限制
        os.makedirs(storage_path, exist_ok=True)
    
    async def add(self, content: str, source: str, metadata: Optional[dict] = None):
        """添加记忆"""
        memory = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "content": content,
            "source": source,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "tags": self._extract_tags(content)
        }
        
        # 检查是否超过限制
        current_count = await self.get_count()
        if current_count >= self.max_memories:
            raise Exception(f"已达到记忆数量限制 ({self.max_memories})")
        
        # 保存到文件
        filename = f"{self.storage_path}/{memory['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        
        return memory
    
    async def search(self, query: str, limit: int = 10):
        """搜索记忆"""
        memories = await self._load_all_memories()
        
        # 简单关键词匹配（专业版会用向量搜索）
        results = []
        for memory in memories:
            score = self._calculate_relevance(query, memory)
            if score > 0:
                results.append({
                    **memory,
                    "score": score
                })
        
        # 按相关性排序
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    async def get_stats(self):
        """获取统计信息"""
        count = await self.get_count()
        return {
            "total_memories": count,
            "max_memories": self.max_memories,
            "usage_percent": round(count / self.max_memories * 100, 2)
        }
    
    async def get_count(self):
        """获取记忆数量"""
        if not os.path.exists(self.storage_path):
            return 0
        return len([f for f in os.listdir(self.storage_path) if f.endswith('.json')])
    
    async def _load_all_memories(self):
        """加载所有记忆"""
        memories = []
        if not os.path.exists(self.storage_path):
            return memories
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                    memories.append(memory)
        
        return memories
    
    def _extract_tags(self, content: str):
        """提取标签"""
        # 简单实现，专业版会用 NLP 提取
        tags = []
        if "会议" in content:
            tags.append("会议")
        if "决策" in content:
            tags.append("决策")
        if "项目" in content:
            tags.append("项目")
        return tags
    
    def _calculate_relevance(self, query: str, memory: dict):
        """计算相关性分数"""
        score = 0
        query_words = query.lower().split()
        content = memory["content"].lower()
        
        for word in query_words:
            if word in content:
                score += 1
        
        return score
