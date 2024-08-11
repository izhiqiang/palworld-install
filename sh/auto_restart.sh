#!/bin/bash

# 操作系统：Ubuntu 22.04 LTS
# wget https://raw.githubusercontent.com/izhiqiang/palworld-install/main/sh/auto_restart.sh
# * * * * * /bin/bash ~/auto_restart.sh > /dev/null 2>&1

systemd_unit=pal-server
mem_threshold=90
mem_usage_percent=$(free | awk '/Mem:/ {printf("%.0f", $3/$2 * 100.0)}')
echo "System Memory Usage: $mem_usage_percent%"
if [ "$mem_usage_percent" -ge "$mem_threshold" ]; then
    echo "Memory usage is above $mem_threshold%. Restarting service: $systemd_unit..."
    sudo systemctl restart "$systemd_unit"
else
    echo "Memory usage is within the threshold."
fi