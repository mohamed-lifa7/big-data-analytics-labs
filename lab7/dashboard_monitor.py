# dashboard_monitor.py
import json
from kafka import KafkaConsumer

# Initialize Consumer
consumer = KafkaConsumer(
    'iot-sensors',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Monitoring System Active... Waiting for data.")
print("-" * 50)

for message in consumer:
    data = message.value
    
    # Logic: Detect Overheating
    if data['temperature'] > 100:
        print(f"⚠️  CRITICAL ALERT: {data['sensor_id']} is OVERHEATING! ({data['temperature']}°C)")
    else:
        print(f"✅ Normal: {data['sensor_id']} at {data['temperature']}°C") 
