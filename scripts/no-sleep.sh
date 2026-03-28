#!/bin/bash

# 禁止熄屏和休眠（7×24 运行）
# 使用方法：sudo /Users/yy/.openclaw/workspace/scripts/no-sleep.sh

echo "🔌 配置 7×24 不熄屏..."

# 禁止显示器休眠（电源适配器模式）
sudo pmset -c displaysleepnever 1

# 禁止系统休眠
sudo pmset -c sleep 0

# 禁止硬盘休眠
sudo pmset -c disksleep 0

# 禁止待机（deep sleep）
sudo pmset -c standby 0

# 禁止 Power Nap（后台刷新）
sudo pmset -c powernap 0

# 查看当前设置
echo ""
echo "✅ 当前电源设置："
pmset -g | grep -E "(sleep|displaysleep|disksleep|standby|powernap)"

echo ""
echo "🎯 配置完成！系统将保持 7×24 运行"
echo "💡 如需恢复默认设置，执行：sudo pmset -c displaysleepnever 0"
