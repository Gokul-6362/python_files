from opcua import Server,ua


# Create an OPC UA server
server = Server()

try:
    # Define the endpoint for the server
    endpoint = "opc.tcp://127.0.0.1:4840/freeopcua/server/"

    # Set the server endpoint
    server.set_endpoint(endpoint)

    # Set the server name
    server.set_server_name("Python OPC UA Server")
    
    folder = server.nodes.objects.add_folder(0, "MyFolder")

    # Create a subfolder named "Input" under "MyFolder"
    input_folder = folder.add_folder(0, "Input")

    # Add the first variable node to the "Input" folder
    var1 = input_folder.add_variable(0, "holding_register_1", 0)
    var1.set_writable()  # Set write access

    # Add the second variable node to the "Input" folder
    var2 = input_folder.add_variable(0, "holding_register_2", 0)
    var2.set_writable()  # Set write access

    # Add the third variable node to the "Input" folder
    var3 = input_folder.add_variable(0, "holding_register_3", 0)
    var3.set_writable()  # Set write access

    # Add the fourth variable node to the "Input" folder
    var4 = input_folder.add_variable(0, "holding_register_4", 0)
    var4.set_writable()  # Set write access

    var5 = input_folder.add_variable(0, "mqtt_data1", 0)
    var5.set_writable()  # Set write access
     
    var5 = input_folder.add_variable(0, "mqtt_data2", 0)
    var5.set_writable()  # Set write access
    
    

    # Start the server
    server.start()

    print("Server started at", endpoint)

except Exception as e:
    print("An error occurred while starting the server:", e)

   


