# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## 🛠️ 工具路由配置

### 飞书日历工具 (feishu_calendar_event)

**触发关键词**:
- 会议、日程、日历、event、calendar
- "明天有什么会"、"下周安排"、"预定会议室"
- 时间相关查询 + 会议/日程上下文

**使用场景**:
1. 查询日程：`feishu_calendar_event action=list`
2. 创建会议：`feishu_calendar_event action=create`
3. 修改日程：`feishu_calendar_event action=patch`
4. 忙闲查询：`feishu_calendar_freebusy action=list`

**示例**:
```
用户："明天上午有什么会议？"
→ 调用：feishu_calendar_event (action=list, time_range=明天上午)

用户："帮我预定明天下午 3 点的会议室"
→ 调用：feishu_calendar_event (action=create, time=明天 15:00)
```

---

### 飞书任务工具 (feishu_task_task)

**触发关键词**:
- 任务、待办、todo、task
- "创建任务"、"分配任务"、"任务进度"

**使用场景**:
1. 创建任务：`feishu_task_task action=create`
2. 查询任务：`feishu_task_task action=list`
3. 更新任务：`feishu_task_task action=patch`

---

### 飞书多维表格 (feishu_bitable_app_table_record)

**触发关键词**:
- 数据表、记录、查询数据
- "查看销售数据"、"添加记录"、"更新表格"

---

### 搜索工具 (tavily_search / web_search)

**触发关键词**:
- 搜索、查找、新闻、最新动态
- "今天有什么新闻"、"查一下 XXX"、"最新进展"

---

### 记忆工具 (memory_search / memory_get)

**触发关键词**:
- "我之前说过"、"上次提到的"、"还记得吗"
- 历史上下文查询、个人偏好

**记忆管理命令**:
- `/compact` - 压缩当前会话上下文（保留关键信息）
- `/reset` - 重置会话（保留长期记忆，清空短期上下文）
- `/new` - 开启全新对话（类似新建标签页）
- `openclaw memory index` - 重建记忆索引（修改记忆文件后必行）
- `openclaw memory status` - 查看记忆状态
- `openclaw memory search "关键词"` - 语义搜索记忆

**最佳实践**:
1. 长对话后使用 `/compact` 降低 Token 消耗
2. 切换话题时使用 `/reset` 保持上下文清晰
3. 修改 MEMORY.md 或 memory/*.md 后立即重建索引
4. 定期使用 `memory_search` 回顾历史记忆

---

## 📝 其他本地配置

### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

---

**最后更新**: 2026-03-27  
**更新内容**: 添加工具路由配置（飞书日历/任务/搜索/记忆）
