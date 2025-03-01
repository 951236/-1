# 系统监控部署指南

## 核心组件说明
- `system_monitor.sh` (1KB)：系统资源监控主程序
- `alert_analyzer.py` (2KB)：告警通知处理模块

## 高级配置

### 日志管理方案
```bash
# 创建日志轮转配置
sudo tee /etc/logrotate.d/system_monitor <<'EOF'
/var/log/system_monitor.log {
    daily               # 每日轮转
    rotate 7           # 保留7天日志
    compress            # 启用gzip压缩
    delaycompress       # 延迟压缩前一个日志
    missingok           # 文件缺失不报错
    notifempty          # 空文件不轮转
    create 0644 root adm  # 设置新建日志权限
    postrotate
        systemctl restart cron.service >/dev/null 2>&1  # 重启关联服务
    endscript
}
EOF

# 手动触发轮转测试
logrotate -vf /etc/logrotate.d/system_monitor
```

### 多节点部署
```bash
# 使用Ansible批量部署
ansible all -m copy -a "src=scripts/ dest=/opt/monitor mode=0755"
ansible all -m file -a "path=/var/log/system_monitor.log state=touch"
```