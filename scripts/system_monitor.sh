#!/bin/bash
# 系统资源监控脚本
set -euo pipefail

LOG_FILE="/var/log/system_monitor.log"

# 获取系统指标
cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *$[0-9.]*$%* id.*/\1/" | awk '{print 100 - $1}')
mem_usage=$(free -m | awk '/Mem/{printf "%.2f", $3/$2 * 100}')
disk_usage=$(df -h / | awk '/\//{print $(NF-1)}')

# 记录日志
echo "$(date +"%Y-%m-%d %H:%M:%S") CPU: ${cpu_usage}% Mem: ${mem_usage}% Disk: ${disk_usage}" >> $LOG_FILE

# 触发告警
if (( $(echo "$cpu_usage > 90" | bc -l) )); then
    python3 /path/to/alert_analyzer.py "CPU过载警告" "当前CPU使用率: ${cpu_usage}%"
fi