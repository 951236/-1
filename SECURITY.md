````markdown
# 安全操作规范

## 敏感信息加密
```bash
# 加密配置文件（首次执行）
ansible-vault create config/smtp.ini

# 编辑加密文件
ansible-vault edit config/smtp.ini

# 运行加密配置环境
ansible-playbook --ask-vault-pass deploy.yml

# 建议的vault密码策略：
# - 长度至少16字符
# - 包含大小写字母、数字和特殊符号
# - 每90天轮换
```

## 权限控制策略
```bash
# 创建专用系统账户
sudo useradd -r -s /bin/false -d /opt/monitor -M monitoruser

# 设置目录所有权
sudo chown -R monitoruser:monitoruser \
  /opt/monitor \
  /var/log/system_monitor.log

# 配置sudo权限（/etc/sudoers）
monitoruser ALL=(root) NOPASSWD: /usr/bin/systemctl restart monitor.service
```

## 网络安全加固
```bash
# 限制SMTP访问IP
iptables -A OUTPUT -p tcp --dport 587 -d smtp.example.com -j ACCEPT
iptables -A OUTPUT -p tcp --dport 587 -j DROP

# 启用SSL证书验证
openssl s_client -connect smtp.example.com:587 -starttls smtp -verify 2
```

---

### 最佳实践补充

#### 1. 监控脚本完整性校验
```bash
# 生成校验和文件
sha256sum scripts/* > checksum.txt

# 验证脚本完整性
verify_script() {
    local file=$1
    grep "$file" checksum.txt | sha256sum -c -
}
verify_script scripts/system_monitor.sh
```

#### 2. 告警信息脱敏处理
```python
# 在alert_analyzer.py中添加
def sanitize_message(msg):
    patterns = [
        r'(password\s*=\s*["\'])(.*?)(["\'])',
        r'(api_key\s*:\s*)\w+'
    ]
    for pattern in patterns:
        msg = re.sub(pattern, r'\1***REDACTED***\3', msg)
    return msg
```

#### 3. 进程监控守护
```bash
# 创建systemd服务（/etc/systemd/system/monitor.service）
[Unit]
Description=System Monitor Service
After=network.target

[Service]
User=monitoruser
ExecStart=/opt/monitor/scripts/system_monitor.sh
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```