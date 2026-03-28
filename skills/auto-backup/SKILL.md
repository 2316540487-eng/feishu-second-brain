# Auto Backup - 智能备份技能

## 功能说明

自动备份 OpenClaw 配置文件、记忆数据、技能状态，支持：
- 定时备份（每天 23:00）
- 增量备份（只备份变更文件）
- 自动清理（保留最近 7 天）
- 备份报告（生成备份日志）

## 使用场景

当用户说：
- "备份配置"
- "备份数据"
- "创建备份"
- "恢复备份"
- "查看备份"

## 备份内容

| 类型 | 路径 | 说明 |
|------|------|------|
| 配置 | `~/.openclaw/openclaw.json` | 主配置文件 |
| 配置 | `~/.openclaw/credentials/` | 认证信息 |
| 记忆 | `workspace/memory/` | 记忆文件 |
| 记忆 | `workspace/MEMORY.md` | 长期记忆 |
| 技能 | `workspace/skills/` | 自定义技能 |
| 日志 | `workspace/.learnings/` | 学习记录 |

## 备份策略

```
每天 23:00 → 自动备份
备份命名 → backup_YYYY-MM-DD_HH-mm-ss.tar.gz
保留策略 → 最近 7 天（自动清理旧备份）
备份位置 → ~/.openclaw/backups/
```

## 命令示例

```bash
# 手动备份
openclaw backup create

# 查看备份列表
openclaw backup list

# 恢复备份
openclaw backup restore --name backup_2026-03-26

# 验证备份
openclaw backup verify --name backup_2026-03-26
```

## 备份报告格式

```markdown
## 备份报告 - 2026-03-26 23:00

### 备份信息
- 备份名称：backup_2026-03-26_23-00-00.tar.gz
- 备份大小：1.2 MB
- 文件数量：45
- 备份耗时：3.2 秒

### 备份内容
✅ 配置文件 (25 KB)
✅ 记忆文件 (850 KB)
✅ 技能文件 (320 KB)
✅ 学习记录 (15 KB)

### 状态
✅ 备份成功
✅ 已验证完整性
✅ 旧备份已清理（保留 7 天）
```

## 注意事项

1. 备份前检查磁盘空间
2. 敏感信息（credentials）加密存储
3. 备份失败时通知用户
4. 恢复前提示用户确认

---

**版本**: 1.0.0
**作者**: OpenClaw Partner
**最后更新**: 2026-03-26
