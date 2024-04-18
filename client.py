import requests
import random
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime

# Constants for API endpoint and MQTT broker (update these with your actual values)
API_ENDPOINT = 'localhost:3000/ddig/SDPR/'
MQTT_BROKER_HOST = 'localhost'
MQTT_BROKER_PORT = 1883  # MQTT broker port (usually 1883 or 8883 for TLS)
MQTT_TOPIC = None  # This will be obtained from the API response
serial_id = 123

def get_mqtt_topic(serial_id):
    # Make request to API to get MQTT topic
    response = requests.post(API_ENDPOINT, params={'Sid': serial_id})
    if response.status_code == 200:
        data = response.json()
        return data.get('topic')
    else:
        return None


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to the MQTT topic obtained from the API
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection to MQTT broker failed with error code {rc}")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")


def main():
    # Get Serial ID from user input or any other source
    global serial_id

    # Obtain MQTT topic from the API
    global MQTT_TOPIC
    MQTT_TOPIC = get_mqtt_topic(serial_id)
    if not MQTT_TOPIC:
        print("Failed to obtain MQTT topic from the API. Exiting.")
        return
    # Create MQTT client instance
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to MQTT broker
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    # Start the MQTT client loop
    client.loop_start()

    try:
        # Publish random integer values to the MQTT topic
        while True:
            random_value = random.randint(1, 50)
            beat = random_value.randint(1, 45)
            ir_Reading = random.randint(1, 30)
            redReading = random.randint(1,23)
            timestamptt = time.time()
            dt_obj = datetime.fromtimestamp(timestamptt)
            timestamp = dt_obj.strftime('%Y-%m-%d %H:%M:%S')    
            client.publish(MQTT_TOPIC, json.dumps({
                                                        'beat':beat,
                                                        'ir_Reading': ir_Reading,
                                                        'redReading': redReading,
                                                        'timestamp': timestamp }))
            print(f"Published value: {random_value} to topic: {MQTT_TOPIC}")
            # Sleep for a few seconds before publishing the next value
            # Adjust the interval based on your requirements
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping MQTT client...")
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()