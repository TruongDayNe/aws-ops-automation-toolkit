#!/bin/bash

echo "--- Bắt đầu cài đặt CloudWatch Agent ---"

# 1. Tải và cài đặt file RPM
echo "Downloading Agent..."
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm

echo "Installing RPM..."
sudo rpm -U ./amazon-cloudwatch-agent.rpm

# 2. Copy file config vào đúng chỗ (Giả sử file json nằm cùng thư mục script)
echo "Applying Config..."
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -c file:cw_config_basic.json \
    -s 

# 3. Kiểm tra trạng thái
echo "Checking Status..."
systemctl status amazon-cloudwatch-agent