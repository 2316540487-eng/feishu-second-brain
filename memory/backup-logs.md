# 备份日志

## 备份记录

### 2026-03-26 00:49

**首次备份（系统配置完成）**

- 备份名称：backup_2026-03-26_00-49-36.tar.gz
- 备份大小：7.7 MB
- 文件数量：885
- 备份位置：/Users/yy/.openclaw/backups/

**备份内容**：
- ✅ 配置文件 (openclaw.json, credentials/)
- ✅ 记忆文件 (memory/, MEMORY.md, SOUL.md, USER.md, AGENTS.md)
- ✅ 技能文件 (skills/)
- ✅ 学习记录 (.learnings/)

**状态**：✅ 成功

---

## 备份策略

| 配置项 | 值 |
|--------|-----|
| 备份频率 | 每天 23:00 |
| 保留天数 | 7 天 |
| 备份位置 | ~/.openclaw/backups/ |
| 自动清理 | 是 |

---

## 恢复方法

```bash
# 1. 查看备份列表
ls -lh ~/.openclaw/backups/

# 2. 恢复指定备份
cd ~/.openclaw/
tar -xzf ~/.openclaw/backups/backup_YYYY-MM-DD_HH-mm-ss.tar.gz -C ~/

# 3. 重启网关
openclaw gateway restart
```

---

## 手动备份

```bash
# 执行手动备份
/Users/yy/.openclaw/workspace/skills/auto-backup/backup.sh
```

---

**最后更新**: 2026-03-26 00:49

## 备份报告 - 2026-03-26 23:00

### 备份信息
- 备份名称：backup_2026-03-26_23-00-01.tar.gz
- 备份大小：7.7M
- 文件数量：     110
- 备份位置：/Users/yy/.openclaw/backups

### 备份内容
✅ 配置文件
✅ 记忆文件
✅ 技能文件
✅ 学习记录

### 状态
✅ 备份成功
✅ 旧备份已清理（保留 7 天）

---

## 备份报告 - 2026-03-26 23:00

### 备份信息
- 备份名称：backup_2026-03-26_23-00-01.tar.gz
- 备份大小：7.7M
- 文件数量：     110
- 备份位置：/Users/yy/.openclaw/backups

### 备份内容
✅ 配置文件
✅ 记忆文件
✅ 技能文件
✅ 学习记录

### 状态
✅ 备份成功
✅ 旧备份已清理（保留 7 天）

---

## 备份报告 - 2026-03-27 23:00

### 备份信息
- 备份名称：backup_2026-03-27_23-00-01.tar.gz
- 备份大小：7.8M
- 文件数量：      62
- 备份位置：/Users/yy/.openclaw/backups

### 备份内容
✅ 配置文件
✅ 记忆文件
✅ 技能文件
✅ 学习记录

### 状态
✅ 备份成功
✅ 旧备份已清理（保留 7 天）

---

## 备份报告 - 2026-03-27 23:00

### 备份信息
- 备份名称：backup_2026-03-27_23-00-01.tar.gz
- 备份大小：7.8M
- 文件数量：      62
- 备份位置：/Users/yy/.openclaw/backups

### 备份内容
✅ 配置文件
✅ 记忆文件
✅ 技能文件
✅ 学习记录

### 状态
✅ 备份成功
✅ 旧备份已清理（保留 7 天）

---
