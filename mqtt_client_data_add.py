import paho.mqtt.client as mqtt

# Define callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Publish a message to a topic
        topic = "topic/test"
        message = "gdgdgd to board"
        client.publish(topic, message,retain=True)
        topic="topic/test2"
        message = "564"
        client.publish(topic, message,retain=True)
        print ("published")
        topic = "topic/test3"
        message = "485"
        client.publish(topic, message,retain=True)
        # Disconnect from the MQTT broker after publishing the message
        client.disconnect()
    else:
        print("Failed to connect, return code=", rc)

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect

# Connect to MQTT broker (replace "broker.example.com" with your broker's address)
client.connect("192.168.122.33", 1883)  # MQTT default port is 1883

# Start the MQTT client loop to handle incoming messages
client.loop_forever()


















