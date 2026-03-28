#!/bin/bash

# OpenClaw 智能备份脚本
# 功能：自动备份配置、记忆、技能数据

set -e

# 配置
BACKUP_DIR="$HOME/.openclaw/backups"
CONFIG_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
RETENTION_DAYS=7
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="backup_${TIMESTAMP}.tar.gz"
LOG_FILE="$WORKSPACE_DIR/memory/backup-logs.md"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 开始备份
echo "🔄 开始备份 - $(date)"

# 创建临时备份目录
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/config"
mkdir -p "$TEMP_DIR/memory"
mkdir -p "$TEMP_DIR/skills"
mkdir -p "$TEMP_DIR/learnings"

# 复制配置文件
echo "📁 备份配置文件..."
cp "$CONFIG_DIR/openclaw.json" "$TEMP_DIR/config/" 2>/dev/null || true
cp -r "$CONFIG_DIR/credentials" "$TEMP_DIR/config/" 2>/dev/null || true

# 复制记忆文件
echo "📁 备份记忆文件..."
cp -r "$WORKSPACE_DIR/memory" "$TEMP_DIR/memory/" 2>/dev/null || true
cp "$WORKSPACE_DIR/MEMORY.md" "$TEMP_DIR/memory/" 2>/dev/null || true
cp "$WORKSPACE_DIR/SOUL.md" "$TEMP_DIR/memory/" 2>/dev/null || true
cp "$WORKSPACE_DIR/USER.md" "$TEMP_DIR/memory/" 2>/dev/null || true
cp "$WORKSPACE_DIR/AGENTS.md" "$TEMP_DIR/memory/" 2>/dev/null || true

# 复制技能文件
echo "📁 备份技能文件..."
cp -r "$WORKSPACE_DIR/skills" "$TEMP_DIR/skills/" 2>/dev/null || true

# 复制学习记录
echo "📁 备份学习记录..."
cp -r "$WORKSPACE_DIR/.learnings" "$TEMP_DIR/learnings/" 2>/dev/null || true

# 压缩备份
echo "📦 压缩备份..."
cd "$TEMP_DIR"
tar -czf "$BACKUP_DIR/$BACKUP_FILE" .
cd - > /dev/null

# 计算备份大小
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
FILE_COUNT=$(tar -tzf "$BACKUP_DIR/$BACKUP_FILE" | wc -l)

# 清理临时文件
rm -rf "$TEMP_DIR"

# 清理旧备份（保留最近 7 天）
echo "🧹 清理旧备份（保留最近 ${RETENTION_DAYS} 天）..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +${RETENTION_DAYS} -delete

# 记录备份日志
cat >> "$LOG_FILE" << EOF

## 备份报告 - $(date +"%Y-%m-%d %H:%M")

### 备份信息
- 备份名称：$BACKUP_FILE
- 备份大小：$BACKUP_SIZE
- 文件数量：$FILE_COUNT
- 备份位置：$BACKUP_DIR

### 备份内容
✅ 配置文件
✅ 记忆文件
✅ 技能文件
✅ 学习记录

### 状态
✅ 备份成功
✅ 旧备份已清理（保留 ${RETENTION_DAYS} 天）

---
EOF

echo "✅ 备份完成！"
echo "📦 备份文件：$BACKUP_DIR/$BACKUP_FILE"
echo "📊 备份大小：$BACKUP_SIZE"
echo "📁 文件数量：$FILE_COUNT"

# 返回备份信息（供 OpenClaw 读取）
cat << EOF

**备份成功！**
- 文件：\`$BACKUP_FILE\`
- 大小：$BACKUP_SIZE
- 位置：\`$BACKUP_DIR\`
EOF
