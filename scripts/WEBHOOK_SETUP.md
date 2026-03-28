# 🪝 飞书 Webhook 配置指南

**目标**：实现群里@消息实时触发 AI 审核

---

## 📋 配置步骤

### 步骤 1: 飞书开放平台创建应用

1. 访问 https://open.feishu.cn/app
2. 点击"创建企业自建应用"
3. 填写应用信息：
   - **名称**: OpenClaw 审核机器人
   - **图标**: 选择一个合适的图标
   - **描述**: 股票分析审核助手

---

### 步骤 2: 配置机器人

1. 在应用管理页面，点击"添加机器人"
2. 填写机器人信息：
   - **名称**: ClawA 审核助手
   - **头像**: 选择一个专业头像
3. 启用机器人

---

### 步骤 3: 配置事件订阅

1. 在应用管理页面，点击"事件订阅"
2. 启用事件订阅功能
3. 配置订阅地址：
   ```
   URL: http://你的服务器 IP:8080/feishu/webhook
   或
   URL: https://你的域名/feishu/webhook
   ```

4. 订阅以下事件：
   - ✅ `im.message.receive_v1` - 接收消息
   - ✅ `im.message.group_at_msg_v1` - 群聊@消息

5. 获取验证 Token 和 Encrypt Key

---

### 步骤 4: 配置权限

1. 在"权限管理"中添加以下权限：
   - ✅ `im:message` - 发送和读取消息
   - ✅ `im:chat` - 获取群聊信息
   - ✅ `contact:user:readonly` - 读取用户信息

2. 发布应用并获取：
   - **App ID**: `cli_xxxxxxxxx`
   - **App Secret**: `xxxxxxxxxxxxxxxx`

---

### 步骤 5: 将机器人添加到群里

1. 在飞书群聊中，点击右上角设置
2. 选择"添加机器人"
3. 选择"OpenClaw 审核机器人"
4. 确认添加

---

### 步骤 6: 启动 Webhook 服务器

```bash
# 启动服务器
python3 /Users/yy/.openclaw/workspace/scripts/feishu_webhook_server.py

# 后台运行
nohup python3 /Users/yy/.openclaw/workspace/scripts/feishu_webhook_server.py > /Users/yy/.openclaw/logs/webhook.log 2>&1 &

# 查看日志
tail -f /Users/yy/.openclaw/logs/webhook.log
```

---

### 步骤 7: 测试配置

在群里发送：
```
@OpenClaw 审核机器人 测试
```

检查日志：
```bash
tail -f /Users/yy/.openclaw/logs/webhook.log
```

应该看到：
```
[2026-03-24 01:45:00] 收到消息：{...}
检测到@消息，触发审核...
```

---

## 🔧 需要填写的配置

编辑 `/Users/yy/.openclaw/workspace/scripts/feishu_webhook_server.py`:

```python
WEBHOOK_SECRET = "从飞书开放平台获取的签名密钥"
APP_ID = "cli_xxxxxxxxx"
APP_SECRET = "xxxxxxxxxxxxxxxx"
```

---

## 📊 工作流程

```
1. 用户在群里@机器人
       ↓
2. 飞书推送消息到 Webhook
       ↓
3. Webhook 服务器接收并解析
       ↓
4. 触发 AI 审核脚本
       ↓
5. AI 审核并生成意见
       ↓
6. 发送审核结果到群里
```

---

## ⚠️ 注意事项

1. **公网访问**: Webhook 需要公网 IP 或内网穿透
2. **HTTPS**: 生产环境建议使用 HTTPS
3. **签名验证**: 必须验证飞书签名，防止伪造请求
4. **超时处理**: 设置合理的超时时间，避免阻塞

---

## 🚀 快速测试

### 本地测试（ngrok 内网穿透）

```bash
# 安装 ngrok
brew install ngrok

# 启动内网穿透
ngrok http 8080

# 复制生成的 https 地址到飞书开放平台
```

### 发送测试消息

在群里发送：
```
@OpenClaw 审核机器人 股票：AAPL 建议：买入
```

---

**配置完成后，@消息会实时触发审核，无需人工提醒。** ✅
