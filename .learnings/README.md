# Self-Improvement Hook 配置完成

## ✅ 已完成的配置

### 1. Hook 文件已安装
```
/Users/yy/.openclaw/hooks/self-improvement/
├── HOOK.md       # Hook 描述文件
├── handler.js    # JavaScript 处理器
└── handler.ts    # TypeScript 源码
```

### 2. 配置文件已更新
- `/Users/yy/.openclaw/openclaw.json` - 已启用 self-improvement hook

### 3. Hook 状态
```
✓ ready  🧠 self-improvement  Injects self-improvement reminder during agent bootstrap
```

---

## 🧠 Hook 工作原理

### 触发时机
- **Event**: `agent:bootstrap`
- **时机**: 每次会话启动时（在注入 workspace 文件之前）
- **范围**: 仅主会话，子会话自动跳过

### 注入内容
Hook 会自动注入一个虚拟文件 `SELF_IMPROVEMENT_REMINDER.md`，包含：

```markdown
## Self-Improvement Reminder

After completing tasks, evaluate if any learnings should be captured:

**Log when:**
- User corrects you → `.learnings/LEARNINGS.md`
- Command/operation fails → `.learnings/ERRORS.md`
- User wants missing capability → `.learnings/FEATURE_REQUESTS.md`
- You discover your knowledge was wrong → `.learnings/LEARNINGS.md`
- You find a better approach → `.learnings/LEARNINGS.md`

**Promote when pattern is proven:**
- Behavioral patterns → `SOUL.md`
- Workflow improvements → `AGENTS.md`
- Tool gotchas → `TOOLS.md`
```

---

## 📝 使用工作流

### 1. 自动触发
每次会话启动时，hook 会自动提醒你检查学习日志。

### 2. 记录学习
当遇到以下情况时：

**用户纠正你**
```markdown
## [LRN-20260324-001] correction

**Logged**: 2026-03-24T00:00:00-07:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
用户纠正了某个概念或方法

### Details
完整描述

### Suggested Action
如何改进

### Metadata
- Source: conversation
- Pattern-Key: example.pattern

---
```

**命令失败**
```markdown
## [ERR-20260324-001] command_name

**Logged**: 2026-03-24T00:00:00-07:00
**Priority**: high
**Status**: pending

### Summary
命令执行失败

### Error
```
错误信息
```

### Suggested Fix
可能的解决方案

---
```

### 3. 定期审查
```bash
# 查看待处理条目数量
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# 查找特定领域
grep -l "Area\*\*: backend" .learnings/*.md
```

### 4. 推广学习
当学习被证明具有广泛适用性时：
1. 提炼为简洁规则
2. 添加到 `SOUL.md`/`AGENTS.md`/`TOOLS.md`
3. 更新原条目状态为 `promoted`

---

## 🔧 管理命令

```bash
# 查看 hooks 列表
openclaw hooks list

# 禁用 hook（如需要）
# 编辑 openclaw.json，设置 "self-improvement": { "enabled": false }

# 重新启用
# 编辑 openclaw.json，设置 "self-improvement": { "enabled": true }
```

---

## 📊 完整系统概览

```
Self-Improvement 系统
├── Hook (自动触发)
│   └── 会话启动时注入提醒
│
├── 日志文件
│   ├── LEARNINGS.md        # 学习、纠正、最佳实践
│   ├── ERRORS.md           # 错误、失败
│   └── FEATURE_REQUESTS.md # 功能请求
│
├── 升级目标
│   ├── SOUL.md             # 行为模式
│   ├── AGENTS.md           # 工作流改进
│   └── TOOLS.md            # 工具注意事项
│
└── 审查节奏
    ├── 会话前：检查相关学习
    ├── 任务后：记录新发现
    └── 每周：推广适用学习
```

---

## 🎯 最佳实践

1. **立即记录** - 上下文最新鲜时记录
2. **具体明确** - 让未来的 AI 能快速理解
3. **包含重现步骤** - 特别是错误
4. **链接相关文件** - 便于修复
5. **建议具体方案** - 不只是"调查"
6. **积极推广** - 不确定时就添加到核心文件

---

配置完成！系统现在会自动提醒你记录学习和改进了。🧠✨
