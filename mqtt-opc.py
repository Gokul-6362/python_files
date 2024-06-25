
import paho.mqtt.client as mqtt
from opcua import Client
from opcua import ua


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        
        client.subscribe("topic/test", qos=1)
        print("Subscribed to topic 'topic/test' with QoS 1")
        client.subscribe("topic/test2", qos=1)
        print("Subscribed to topic 'topic/test2' with QoS 1")
        client.subscribe("topic/test3", qos=1)
        print("Subscribed to topic 'topic/test2' with QoS 1")
    else:
        print("Failed to connect, return code=", rc)

def on_message(client, userdata, message):
    try:
        print("Received message on topic:", message.topic)
        print("Message payload:", str(message.payload.decode("utf-8")))
        
        topic_to_node_mapping = {
            "topic/test": "ns=0;i=20007",
            "topic/test2": "ns=0;i=20008", 
              # Add more mappings as needed
        }
        
        # Check if the message topic has a corresponding node
        if message.topic in topic_to_node_mapping:
            node_id = topic_to_node_mapping[message.topic]
        else:
            # Create a new node and add it to the mapping
            node_id = create_new_node(message.topic)
            topic_to_node_mapping[message.topic] = node_id
            
        store_to_opcua(node_id, message.payload.decode("utf-8"))
            
    except Exception as e:
        print("Error in on_message callback:", e)

def create_new_node(topic):
    try:
        client_opcua = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
        client_opcua.connect()
        
        root_node = client_opcua.get_root_node()
        
        # Create a new object node under the root node
        new_node = root_node.add_object(ua.NodeId.from_string("ns=0;s=" + topic), topic)
        
        client_opcua.disconnect()
        print("New node created for topic:", topic)
        
        return new_node.nodeid.to_string()
    except Exception as e:
        print("Error creating new node for topic:", topic, e)

def store_to_opcua(node_id, data):
    try:
        client_opcua = Client("opc.tcp://127.0.0.1:4840/freeopcua/server/")
        client_opcua.connect()
        
        node = client_opcua.get_node(node_id)
        node.set_value(data)
        
        client_opcua.disconnect()
        print("Data stored to OPC UA server successfully")
    except Exception as e:
        print("Error storing data to OPC UA server:", e)


client_mqtt = mqtt.Client()

client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message


try:
    client_mqtt.connect("192.168.122.33", 1883)
    print("Connecting to MQTT broker...")
except Exception as e:
    print("Error connecting to MQTT broker:", e)


try:
    client_mqtt.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print("Error in MQTT client loop:", e)
finally:
    client_mqtt.disconnect()
