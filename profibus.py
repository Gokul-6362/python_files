import socket
import threading
import time
import random
from opcua import Client, ua

# Simulated Profibus slave address
PROFIBUS_SLAVE_ADDR = ('localhost', 6000)

# Flag to control thread execution
running = True

# Function to simulate Profibus slave behavior
def profibus_slave_thread():
    global running
    
    # Simulated Profibus message format
    def generate_profibus_message():
        # Simulate data bytes in PROFIBUS message
        temperature = random.uniform(20.0, 30.0)
        pressure = random.uniform(1.0, 2.0)
        level = random.uniform(60.0, 80.0)
        
        message = f"Temperature={temperature:.2f}, Pressure={pressure:.2f}, Level={level:.2f}"
        return message
    
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(PROFIBUS_SLAVE_ADDR)
        sock.listen(1)
        
        print(f"Profibus slave is running on {PROFIBUS_SLAVE_ADDR[0]}:{PROFIBUS_SLAVE_ADDR[1]}")

        while running:
            try:
                conn, addr = sock.accept()
                print(f"Connected by {addr}")
                
                while running:
                    # Simulate Profibus message format
                    message = generate_profibus_message()
                    
                    # Send simulated Profibus message
                    conn.sendall(message.encode())
                    
                    time.sleep(1)  # Simulate delay between messages
            
            except KeyboardInterrupt:
                print("Profibus slave stopped by user")
                break
            
            except Exception as e:
                print(f"Error in Profibus slave: {e}")
            
            finally:
                conn.close()

# Function to send data to OPC UA server
def send_to_opcua_server():
    global running
    
    # OPC UA server connection parameters
    opcua_server_url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
    
    try:
        client = Client(opcua_server_url)
        client.connect()
        print(f"Connected to OPC UA server at {opcua_server_url}")
        
        # Example OPC UA variable node paths for variables in the server
        opc_variable_node_paths = [
            "ns=0;i=20003",  # Example OPC UA variable node path for variable 1
            "ns=0;i=20004",  # Example OPC UA variable node path for variable 2
            "ns=0;i=20005"   # Example OPC UA variable node path for variable 3
        ]
        
        while running:
            try:
                # Simulate data update
                temperature = random.uniform(20.0, 30.0)
                pressure = random.uniform(1.0, 2.0)
                level = random.uniform(60.0, 80.0)
                
                # Update OPC UA variables
                nodes = [client.get_node(node_path) for node_path in opc_variable_node_paths]
                values = [ua.Variant(value, ua.VariantType.Float) for value in [temperature, pressure, level]]
                for node, value in zip(nodes, values):
                    node.set_value(value)
                
                print(f"Updated OPC UA variables: Temperature={temperature:.2f}, Pressure={pressure:.2f}, Level={level:.2f}")
                
                time.sleep(1)  # Update interval
                
            except KeyboardInterrupt:
                break
            
            except Exception as e:
                print(f"Error updating OPC UA variables: {e}")
                break
    
    except KeyboardInterrupt:
        print("OPC UA data sender stopped by user")
        
    except Exception as e:
        print(f"Error in OPC UA data sender: {e}")
    
    finally:
        if client:
            client.disconnect()

if __name__ == "__main__":
    # Start Profibus slave thread
    slave_thread = threading.Thread(target=profibus_slave_thread)
    slave_thread.start()

    # Start OPC UA data sender thread
    opcua_thread = threading.Thread(target=send_to_opcua_server)
    opcua_thread.start()

    # Keep main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Main program stopped by user")
        running = False  # Set flag to stop threads gracefully
        slave_thread.join()  # Wait for Profibus slave thread to finish
        opcua_thread.join()  # Wait for OPC UA data sender thread to finish
