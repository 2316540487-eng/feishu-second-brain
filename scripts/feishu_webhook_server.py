#!/usr/bin/env python3
"""
飞书 Webhook 服务器
接收群@消息，触发 AI 审核
"""

import json
import hashlib
import hmac
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import subprocess
import sys

# 飞书 webhook 配置
WEBHOOK_PORT = 8080
APP_ID = "cli_a9489e86be385bd7"
APP_SECRET = "YrM7aPnGyBaCCGOARkbjLdwVPNn8WGez"
VERIFICATION_TOKEN = "A3wfIglHW6NATmBktUd2MhzbgAYeeOR2"
WEBHOOK_SECRET = ""  # 需要从飞书开放平台获取

class FeishuWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 验证签名
        signature = self.headers.get('X-Lark-Signature', '')
        timestamp = self.headers.get('X-Lark-Request-Timestamp', '')
        
        # 解析消息
        try:
            data = json.loads(post_data.decode('utf-8'))
            print(f"[{datetime.now()}] 收到消息：{json.dumps(data, indent=2)}")
            
            # 检查是否是@消息
            if self.is_mention_message(data):
                print("检测到@消息，触发审核...")
                self.trigger_review(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        except Exception as e:
            print(f"错误：{e}")
            self.send_response(500)
            self.end_headers()
    
    def is_mention_message(self, data):
        """检查是否是@机器人的消息"""
        try:
            # 检查消息类型
            msg_type = data.get('message', {}).get('message_type', '')
            content = data.get('message', {}).get('content', {})
            
            # 检查是否有@机器人
            if isinstance(content, str):
                content = json.loads(content)
            
            mentions = content.get('mentions', [])
            for mention in mentions:
                if 'bot' in mention.get('name', '').lower() or 'claw' in mention.get('name', '').lower():
                    return True
            
            return False
        except:
            return False
    
    def trigger_review(self, data):
        """触发审核流程"""
        try:
            # 调用 AI 审核脚本
            subprocess.run([
                'python3',
                '/Users/yy/.openclaw/workspace/scripts/trigger_review.py',
                json.dumps(data)
            ], timeout=30)
        except Exception as e:
            print(f"触发审核失败：{e}")
    
    def log_message(self, format, *args):
        pass  # 禁用默认日志

def run_server():
    server = HTTPServer(('0.0.0.0', WEBHOOK_PORT), FeishuWebhookHandler)
    print(f"🚀 Webhook 服务器启动在端口 {WEBHOOK_PORT}")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
