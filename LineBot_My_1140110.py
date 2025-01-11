# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 00:45:16 2025

@author: super
"""
# 資料來源：https://www.wang-sy.com/courses/python-linebot/lessons/20241127-003/

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 定義LINE Messaging API的回應端點和金鑰
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
# LINE_CHANNEL_ACCESS_TOKEN = "你的LINE_CHANNEL_ACCESS_TOKEN"
# LINE_CHANNEL_ACCESS_TOKEN = "lQwjfwzHsCgy9CMTwGhYzRtAeGoin8/rpevfc7Cd1vlR7ZNJatZNogAENKtmQqrScaNps7U3ABG8qYkZ5cPWCgsUAoCRCrgdSP5SuWusj4RaHkn0+TnJMmGLrkMvfwY/Se7NvRQn30L6C85OweiPsAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 設定請求的標頭
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}

@app.route('/')
def hello():
    return "LINE Webhook is active!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received webhook event:", data)
    
    # 迭代處理每個事件
    for event in data.get('events', []):
        event_type = event.get('type')
        
        if event_type == 'message':
            message = event.get('message', {})
            text = message.get('text', '')  # 取得文字內容
            emojis = message.get('emojis', [])
            mentions = message.get('mention', {}).get('mentionees', [])
            reply_token = event.get('replyToken')  # 取得回應用的token
            
            # 印出訊息詳細內容
            print(f"Message Text: {text}")
            if emojis:
                for emoji in emojis:
                    emoji_id = emoji.get('emojiId')
                    print(f"Emoji used: {emoji_id}")
            
            if mentions:
                for mention in mentions:
                    mention_type = mention.get('type')
                    if mention_type == 'all':
                        print("The message mentioned everyone in the group.")
                    elif mention_type == 'user':
                        mentioned_user_id = mention.get('userId')
                        is_self = mention.get('isSelf')
                        print(f"User {mentioned_user_id} was mentioned (self: {is_self}).")
            
            # 根據接收到的訊息生成回應
            if text.lower() == "hello":
                reply_text = "Hi there! How can I help you?"
            elif text.lower() == "bye":
                reply_text = "Goodbye! Have a great day!"
            else:
                reply_text = f"You said: {text}"
            
            # 準備回應訊息的內容
            reply_payload = {
                "replyToken": reply_token,
                "messages": [
                    {"type": "text", "text": reply_text}
                ]
            }
            
            # 發送回應
            response = requests.post(LINE_REPLY_URL, headers=HEADERS, json=reply_payload)
            print("Reply response:", response.status_code, response.text)
        
        else:
            print(f"Unhandled event type: {event_type}")
    
    return jsonify(status='ok'), 200

if __name__ == '__main__':
    app.run(debug=True)