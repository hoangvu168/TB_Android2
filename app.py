import json

from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = "192.168.0.104"  # Thay bằng broker của bạn
MQTT_TOPIC = "tb"

# Gửi MQTT dưới dạng JSON
def send_mqtt(title, content):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)

    # Tạo chuỗi JSON
    message = json.dumps({"title": title, "content": content}, ensure_ascii=False)
    print(f"Gửi: {message}")  # Log ra màn hình

    # Gửi MQTT
    client.publish(MQTT_TOPIC, message)
    print("Gửi thành công")
    client.disconnect()


# Route trỏ vào file index.html
@app.route("/")
def home():
    return render_template("index.html")

# Route API Gửi MQTT
@app.route("/send", methods=["POST"])
def send():
    title = request.args.get("title")
    content = request.args.get("content")
    if title and content:
        send_mqtt(title, content)
        return jsonify({"message": "Thông báo đã gửi thành công!"})
    return jsonify({"message": "Thiếu dữ liệu!"})

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port= 5000, debug=False)
