#!/bin/bash

# * * * * * /bin/bash ~/auto_restart.sh > /dev/null 2>&1

service_name="pal-server.service"
mem_threshold=90
mem_usage_percent=$(free | awk '/Mem:/ {printf("%.0f", $3/$2 * 100.0)}')
echo "System Memory Usage: $mem_usage_percent%"
if [ "$mem_usage_percent" -ge "$mem_threshold" ]; then
    echo "Memory usage is above $mem_threshold%. Restarting service: $service_name..."
    sudo systemctl restart "$service_name"
else
    echo "Memory usage is within the threshold."
fi