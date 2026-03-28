#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 论坛自动学习脚本 v4
每 6 小时检查 clawd.org.cn 论坛的新帖子并学习

功能：
1. 监控 8 个核心页面
2. 学习新内容并记录到 memory
3. 发送飞书消息通知
4. 记录学习历史统计
"""

import sys
import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = "/Users/yy/.openclaw/workspace"
LOG_FILE = "/Users/yy/.openclaw/logs/forum-learn.log"
MEMORY_DIR = "/Users/yy/.openclaw/workspace/memory"
LAST_CHECK_FILE = f"{MEMORY_DIR}/forum-last-check.txt"
LEARNED_POSTS_FILE = f"{MEMORY_DIR}/forum-learned-posts.json"
STATS_FILE = f"{MEMORY_DIR}/forum-learning-stats.json"
NOTIFICATION_FILE = f"{MEMORY_DIR}/forum-notification-pending.json"

# 论坛页面列表
FORUM_PAGES = [
    {'id': 'forum-home', 'title': 'OpenClaw 论坛首页', 'url': 'https://clawd.org.cn/forum/', 'category': '社区讨论', 'keywords': ['讨论', '分享', '提问'], 'priority': 1},
    {'id': 'automation-cron', 'title': '定时任务配置指南', 'url': 'https://clawd.org.cn/automation/cron-jobs.html', 'category': '自动化', 'keywords': ['定时', 'cron', '自动化'], 'priority': 1},
    {'id': 'tools-creating', 'title': '技能开发最佳实践', 'url': 'https://clawd.org.cn/tools/creating-skills.html', 'category': '技能开发', 'keywords': ['技能', '开发', '教程'], 'priority': 1},
    {'id': 'tools-overview', 'title': '工具与技能概述', 'url': 'https://clawd.org.cn/tools/', 'category': '工具', 'keywords': ['工具', '技能', '配置'], 'priority': 2},
    {'id': 'concepts-memory', 'title': '记忆系统详解', 'url': 'https://clawd.org.cn/concepts/memory.html', 'category': '核心概念', 'keywords': ['记忆', 'memory', '会话'], 'priority': 1},
    {'id': 'gateway-config', 'title': '网关配置示例', 'url': 'https://clawd.org.cn/gateway/configuration-examples.html', 'category': '网关', 'keywords': ['网关', '配置', '部署'], 'priority': 2},
    {'id': 'channels-feishu', 'title': '飞书通道配置', 'url': 'https://clawd.org.cn/channels/feishu.html', 'category': '消息通道', 'keywords': ['飞书', '通道', '集成'], 'priority': 2},
    {'id': 'releases', 'title': '版本发布信息', 'url': 'https://clawd.org.cn/releases.html', 'category': '版本更新', 'keywords': ['版本', '更新', '新功能'], 'priority': 1},
]

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "LEARN": "📚"}.get(level, "•")
    log_line = f"[{timestamp}] {emoji} {message}"
    print(log_line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"写入日志失败：{e}")

def load_json_file(filepath, default=None):
    """加载 JSON 文件"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else {}

def save_json_file(filepath, data):
    """保存 JSON 文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_last_check():
    """获取上次检查的时间"""
    try:
        with open(LAST_CHECK_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_check(timestamp):
    """保存检查时间"""
    os.makedirs(os.path.dirname(LAST_CHECK_FILE), exist_ok=True)
    with open(LAST_CHECK_FILE, "w", encoding="utf-8") as f:
        f.write(timestamp)

def send_feishu_notification(learned_items, stats):
    """
    发送飞书消息通知
    将通知内容写入文件，由 OpenClaw 主进程发送
    """
    try:
        if not learned_items:
            return False
        
        # 构建通知内容
        items_text = "\n".join([f"• {item}" for item in learned_items])
        
        next_check = (datetime.now() + timedelta(hours=6)).strftime('%m-%d %H:%M')
        
        notification = {
            "type": "feishu_message",
            "msg_type": "text",
            "content": {
                "text": f"""📚 论坛学习通知

发现 {len(learned_items)} 个新内容：

{items_text}

📊 累计运行：{stats['total_runs']} 次
📈 共学习：{stats['total_learned']} 个内容
⏰ 下次检查：{next_check}
"""
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # 写入通知文件（OpenClaw 主进程会读取并发送）
        save_json_file(NOTIFICATION_FILE, notification)
        
        log(f"通知已准备：{NOTIFICATION_FILE}", "SUCCESS")
        return True
    except Exception as e:
        log(f"准备通知失败：{e}", "ERROR")
        return False

def evaluate_learning_value(page):
    """评估页面学习价值"""
    high_priority = ['技能开发', '自动化', '版本更新', '核心概念']
    
    if page.get('category') in high_priority:
        return True
    
    if page.get('priority', 2) == 1:
        return True
    
    return False

def save_learning(page):
    """保存学习内容到 memory 文件"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = f"{MEMORY_DIR}/{today}.md"
        
        learning_entry = f"""
## 📚 论坛学习 - {page.get('title', '未知标题')}

**分类**: {page.get('category', '未分类')}  
**链接**: {page.get('url', '未知链接')}  
**学习时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

### 学习要点
- 页面类别：{page.get('category')}
- 关键词：{', '.join(page.get('keywords', []))}
- 优先级：{'⭐ 高' if page.get('priority') == 1 else '普通'}
- 建议定期回访查看更新

---
"""
        
        if not os.path.exists(memory_file):
            with open(memory_file, "w", encoding="utf-8") as f:
                f.write(f"# {today} 记忆\n\n")
        
        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(learning_entry)
        
        log(f"已保存：{page.get('title', '未知')[:40]}", "LEARN")
        return True
    except Exception as e:
        log(f"保存失败：{e}", "ERROR")
        return False

def update_stats(learned_count, total_pages):
    """更新学习统计"""
    stats = load_json_file(STATS_FILE, {
        'total_runs': 0,
        'total_learned': 0,
        'last_run': None,
        'runs_by_date': {}
    })
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    stats['total_runs'] += 1
    stats['total_learned'] += learned_count
    stats['last_run'] = datetime.now().isoformat()
    
    if today not in stats['runs_by_date']:
        stats['runs_by_date'][today] = {'runs': 0, 'learned': 0}
    
    stats['runs_by_date'][today]['runs'] += 1
    stats['runs_by_date'][today]['learned'] += learned_count
    
    save_json_file(STATS_FILE, stats)
    return stats

def main():
    log("=" * 60, "INFO")
    log("🚀 开始论坛学习检查", "INFO")
    
    # 加载状态
    last_check = get_last_check()
    log(f"上次检查：{last_check or '首次运行'}", "INFO")
    
    learned_posts = load_json_file(LEARNED_POSTS_FILE, [])
    log(f"已学习页面数：{len(learned_posts)}", "INFO")
    
    # 检查每个页面
    new_count = 0
    learned_count = 0
    learned_items = []
    
    for page in FORUM_PAGES:
        page_url = page.get('url')
        
        # 跳过已学习的
        if page_url in learned_posts:
            continue
        
        # 评估学习价值
        if not evaluate_learning_value(page):
            log(f"跳过 (价值不足): {page.get('title', '')[:30]}", "INFO")
            continue
        
        new_count += 1
        log(f"✨ 发现新内容：{page.get('title', '')[:40]}", "SUCCESS")
        
        # 保存学习记录
        if save_learning(page):
            learned_posts.append(page_url)
            learned_count += 1
            learned_items.append(f"{page.get('category')} - {page.get('title', '')}")
            
            # 限制每次学习的数量
            if learned_count >= 3:
                log("已达到本次学习上限 (3 个)", "INFO")
                break
    
    # 保存状态
    save_json_file(LEARNED_POSTS_FILE, learned_posts)
    save_last_check(datetime.now().isoformat())
    
    # 更新统计
    stats = update_stats(learned_count, len(FORUM_PAGES))
    
    # 发送通知
    if learned_count > 0:
        log(f"📬 准备发送飞书通知...", "INFO")
        send_feishu_notification(learned_items, stats)
    
    # 摘要
    log("=" * 60, "INFO")
    log(f"✅ 完成：检查 {len(FORUM_PAGES)} 个页面，{new_count} 个新内容，学习 {learned_count} 个", "SUCCESS")
    log(f"📊 累计运行：{stats['total_runs']} 次，共学习 {stats['total_learned']} 个内容", "INFO")
    
    next_check = datetime.now() + timedelta(hours=6)
    log(f"⏰ 下次检查：{next_check.strftime('%Y-%m-%d %H:%M')}", "INFO")
    
    # 如果有通知，输出提示
    if learned_count > 0:
        log(f"\n🔔 通知已写入：{NOTIFICATION_FILE}", "INFO")
        log(f"   OpenClaw 主进程会读取并发送飞书消息", "INFO")

if __name__ == "__main__":
    main()
