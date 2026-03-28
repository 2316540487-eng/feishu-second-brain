# 📊 性能监控配置

**时间**: 2026-03-24 00:58 PDT

---

## ✅ 已配置监控

### 1. 健康检查脚本
**位置**: `/Users/yy/.openclaw/workspace/scripts/health_check.py`

**监控项目**:
- ✅ 磁盘使用
- ✅ 内存状态
- ✅ 系统负载
- ✅ 进程数
- ✅ 缓存性能

**使用方式**:
```bash
# 运行检查
python3 ~/workspace/scripts/health_check.py

# JSON 输出
python3 ~/workspace/scripts/health_check.py --json

# 日志位置
~/workspace/logs/health-YYYY-MM-DD.json
```

---

## 📊 当前系统状态

**检查结果**: ✅ 健康

| 指标 | 值 | 状态 |
|------|-----|------|
| 磁盘使用 | 7% (12GB/228GB) | ✅ 优秀 |
| 空闲内存 | 1044MB | ✅ 正常 |
| 系统负载 | 1.44 | ✅ 正常 |
| 进程数 | 583 | ✅ 正常 |

---

## 🔧 建议的监控频率

### 实时关注
- 系统负载 (持续>4 需关注)
- 内存使用 (空闲<500MB 需关注)

### 每日检查
- 磁盘使用 (超过 90% 需清理)
- 健康日志审查

### 每周回顾
- 性能趋势分析
- 缓存命中率统计

---

## ⚙️ 自动化配置 (可选)

### 添加到 Crontab
```bash
# 每天早上 8 点运行健康检查
0 8 * * * python3 ~/.openclaw/workspace/scripts/health_check.py >> ~/.openclaw/logs/health-cron.log 2>&1

# 每 4 小时记录缓存统计
0 */4 * * * source ~/.openclaw/memory/venv/bin/activate && python ~/.openclaw/memory/openclaw_cache.py stats >> ~/.openclaw/logs/cache-cron.log 2>&1
```

### 添加到 HEARTBEAT.md
```markdown
# 心跳检查清单
- [ ] 查看系统健康日志
- [ ] 检查缓存命中率
- [ ] 审查异常警告
```

---

## 📁 日志文件

**位置**: `/Users/yy/.openclaw/workspace/logs/`

**文件命名**: `health-YYYY-MM-DD.json`

**内容示例**:
```json
{
  "timestamp": "2026-03-24T00:58:07",
  "status": "healthy",
  "disk": {"usage_percent": "7"},
  "memory": {"free_mb": 1044},
  "load": {"1min": 1.44},
  "processes": 583
}
```

---

## ⚠️ 警告阈值

| 指标 | 警告 | 严重 |
|------|------|------|
| 磁盘使用 | >70% | >90% |
| 系统负载 (1min) | >2 | >4 |
| 空闲内存 | <1000MB | <500MB |
| 进程数 | >1000 | >2000 |

---

## 📞 快速命令

```bash
# 查看今日健康状态
python3 ~/workspace/scripts/health_check.py

# 查看历史日志
cat ~/workspace/logs/health-$(date +%Y-%m-%d).json

# 查看缓存统计
source ~/.openclaw/memory/venv/bin/activate
python ~/workspace/memory/openclaw_cache.py

# 监控系统负载 (实时)
watch -n 5 'uptime'
```

---

**监控状态**: ✅ 已配置并运行正常
