#!/usr/bin/env python3
"""
系统健康检查脚本
监控 CPU、内存、磁盘、进程等
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path


def run_command(cmd):
    """运行 Shell 命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def check_disk():
    """检查磁盘使用"""
    output = run_command("df -h / | tail -1")
    parts = output.split()
    if len(parts) >= 5:
        return {
            'total': parts[1],
            'used': parts[2],
            'available': parts[3],
            'usage_percent': parts[4].replace('%', '')
        }
    return {}


def check_memory():
    """检查内存状态"""
    output = run_command("vm_stat")
    stats = {}
    for line in output.split('\n'):
        if ':' in line and 'page size' not in line.lower():
            try:
                key, value = line.split(':')
                stats[key.strip()] = int(value.strip().rstrip('.'))
            except ValueError:
                pass
    
    page_size = 16384  # macOS ARM64
    return {
        'free_mb': stats.get('Pages free', 0) * page_size / 1024 / 1024,
        'active_mb': stats.get('Pages active', 0) * page_size / 1024 / 1024,
        'wired_mb': stats.get('Pages wired down', 0) * page_size / 1024 / 1024,
        'compressed_mb': stats.get('Pages stored in compressor', 0) * page_size / 1024 / 1024
    }


def check_load():
    """检查系统负载"""
    output = run_command("uptime")
    if 'load averages:' in output:
        load_part = output.split('load averages:')[1].strip()
        loads = [float(x.strip().rstrip(',')) for x in load_part.split()[:3]]
        return {
            '1min': loads[0],
            '5min': loads[1],
            '15min': loads[2]
        }
    return {}


def check_process_count():
    """检查进程数"""
    output = run_command("ps aux | wc -l")
    try:
        return int(output)
    except:
        return 0


def check_cache_stats():
    """检查缓存统计"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from openclaw_cache import get_cache_proxy
        cache = get_cache_proxy()
        stats = cache.get_stats()
        return {
            'hit_rate': stats.get('hit_rate', '0%'),
            'total_requests': stats.get('total_requests', 0),
            'cache_hits': stats.get('cache_hits', 0)
        }
    except Exception as e:
        return {'error': str(e)}


def health_check():
    """执行完整健康检查"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'hostname': run_command("hostname"),
        'disk': check_disk(),
        'memory': check_memory(),
        'load': check_load(),
        'processes': check_process_count(),
        'cache': check_cache_stats()
    }
    
    # 健康评估
    issues = []
    
    # 磁盘检查
    disk_usage = int(report['disk'].get('usage_percent', 0))
    if disk_usage > 90:
        issues.append(f"🔴 磁盘使用过高：{disk_usage}%")
    elif disk_usage > 70:
        issues.append(f"🟡 磁盘使用警告：{disk_usage}%")
    
    # 负载检查
    load_1min = report['load'].get('1min', 0)
    if load_1min > 4:
        issues.append(f"🔴 系统负载过高：{load_1min}")
    elif load_1min > 2:
        issues.append(f"🟡 系统负载警告：{load_1min}")
    
    # 内存检查
    free_mb = report['memory'].get('free_mb', 0)
    if free_mb < 500:
        issues.append(f"🔴 内存不足：{free_mb:.0f}MB")
    elif free_mb < 1000:
        issues.append(f"🟡 内存警告：{free_mb:.0f}MB")
    
    report['issues'] = issues
    report['status'] = 'healthy' if not issues else 'warning' if len(issues) == 1 else 'critical'
    
    return report


def print_report(report):
    """打印报告"""
    print("\n" + "=" * 60)
    print("🏥 系统健康检查报告")
    print("=" * 60)
    print(f"时间：{report['timestamp']}")
    print(f"主机：{report['hostname']}")
    print(f"状态：{'✅ 健康' if report['status'] == 'healthy' else '⚠️ 警告' if report['status'] == 'warning' else '🔴 严重'}")
    
    print("\n📊 磁盘使用:")
    disk = report['disk']
    print(f"  总计：{disk.get('total', 'N/A')}")
    print(f"  已用：{disk.get('used', 'N/A')} ({disk.get('usage_percent', 'N/A')}%)")
    print(f"  可用：{disk.get('available', 'N/A')}")
    
    print("\n💾 内存状态:")
    mem = report['memory']
    print(f"  空闲：{mem.get('free_mb', 0):.0f}MB")
    print(f"  活跃：{mem.get('active_mb', 0):.0f}MB")
    print(f"  压缩：{mem.get('compressed_mb', 0):.0f}MB")
    
    print("\n⚡ 系统负载:")
    load = report['load']
    print(f"  1 分钟：{load.get('1min', 0):.2f}")
    print(f"  5 分钟：{load.get('5min', 0):.2f}")
    print(f"  15 分钟：{load.get('15min', 0):.2f}")
    
    print("\n🔄 进程数:")
    print(f"  {report['processes']}")
    
    print("\n⚡ 缓存性能:")
    cache = report.get('cache', {})
    if 'error' not in cache:
        print(f"  命中率：{cache.get('hit_rate', 'N/A')}")
        print(f"  总请求：{cache.get('total_requests', 0)}")
        print(f"  命中：{cache.get('cache_hits', 0)}")
    else:
        print(f"  无法获取：{cache.get('error')}")
    
    if report['issues']:
        print("\n⚠️ 问题:")
        for issue in report['issues']:
            print(f"  {issue}")
    
    print("\n" + "=" * 60)


def main():
    """主函数"""
    import sys
    
    report = health_check()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        print(json.dumps(report, indent=2, default=str))
    else:
        print_report(report)
    
    # 保存到日志
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"health-{datetime.now().strftime('%Y-%m-%d')}.json"
    
    with open(log_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📁 日志已保存：{log_file}")


if __name__ == '__main__':
    main()
