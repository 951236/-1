## 部署指南

### 快速开始
```bash
# 初始化配置
chmod +x scripts/*.sh
mkdir config && cp config_example/smtp_settings.ini config/smtp.ini
vim config/smtp.ini

# 定时任务配置
(crontab -l 2>/dev/null; echo "*/5 * * * /path/to/system_monitor.sh") | crontab -

## 快速使用
```bash
git clone https://github.com/yourname/server-inspection-tools
cp config_example/ config/ -r