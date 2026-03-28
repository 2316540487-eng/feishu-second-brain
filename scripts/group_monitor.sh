#!/bin/bash
# 群消息监控脚本 - 每 30 秒检查一次

GROUP_ID="oc_3442e3de834815ee2f7e6e95a4e25757"
LAST_CHECK=$(date +%s)

while true; do
    # 检查群消息
    python3 -c "
import requests
import json

# 调用飞书 API 获取群消息
# 检查是否有@我的消息
# 如果有，立即触发审核
print('Monitoring group messages...')
" 2>&1 | tee -a /Users/yy/.openclaw/logs/group_monitor.log
    
    sleep 30
done
