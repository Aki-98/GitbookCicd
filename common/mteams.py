import requests
import json

# 复制生成的 Webhook URL
url = "https://teams.microsoft.com/l/channel/19%3A9f51405c12e24123a12e6a522d79cc69%40thread.tacv2/ChinaUX-Test?groupId=6afd2930-6ab2-4cca-8fbe-5a9f29f82520&ngc=true"

# 定义发送的消息内容
message = {
    "title": "New Event Notification",
    "text": "A new task has been assigned to you.",
    "themeColor": "0076D7",  # 设置消息的主题颜色（可选）
}

# 发送 POST 请求
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(message), headers=headers)

# 检查发送结果
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")
