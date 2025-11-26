# sensor_simulation.py
import time
import json
import random
from kafka import KafkaProducer

# Initialize Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8') # Format as JSON
)

# Simulate 3 different machines
machine_ids = ["Excavator-01", "Crane-04", "Bulldozer-02"]

print("IoT Sensors started... Press Ctrl+C to stop.")

try:
    while True:
        # Create fake data
        data = {
            "sensor_id": random.choice(machine_ids),
            "temperature": round(random.uniform(60, 110), 1), # Temp between 60 and 110
            "engine_rpm": random.randint(2000, 4500),
            "timestamp": time.time()
        }
        
        # Send to Kafka topic 'iot-sensors'
        producer.send('iot-sensors', value=data)
        
        print(f"Sent: {data}")
        time.sleep(1) # Wait 1 second
        
except KeyboardInterrupt:
    print("Sensors stopped.")
    producer.close()
