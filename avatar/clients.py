"""
Client UDP for Avatar
Author: Ganesh from https://github.com/ganeshsar/UnityPythonMediaPipeAvatar
Purpose: 

This class ClientUDP (clientUDP.py:35-82:30) is a subclass of threading.
Thread and is used for managing a UDP client connection.

run (clientUDP.py:37:5-38:23): Calls the connect (clientUDP.py:69:5-82:30) method.
init (clientUDP.py:40:5-46:13): Initializes the client with IP, port, and connection settings.
isConnected (clientUDP.py:48:5-49:30): Checks if the client is connected.
sendMessage (clientUDP.py:51:5-60:30): Sends a message to the server.
disconnect (clientUDP.py:62:5-67:27): Closes the socket and disconnects the client.
connect (clientUDP.py:69:5-82:30): Sets up the socket connection to the server.
"""

"""
MIT License

Copyright (c) 2023 Ganesh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import socket
import time
import threading

class ClientUDP(threading.Thread):

    def run(self):
        self.connect()

    def __init__(self,ip,port, autoReconnect = True) -> None:
        threading.Thread.__init__(self)
        self.IP = ip
        self.PORT = port
        self.AUTO_RECONNECT = autoReconnect
        self.connected = False
        pass

    def isConnected(self):
        return self.connected

    def sendMessage(self,message):
        try:
            message = str('%s<EOM>'%message).encode('utf-8')
            self.socket.send(message)
        except ConnectionRefusedError as ex:
            print("Connection refused. Is server running?")
            self.disconnect()
        except ConnectionResetError as ex:
            print("Server was disconnected...")
            self.disconnect()

    def disconnect(self):
        self.connected = False
        self.socket.close()
        if(self.autoReconnect):
            time.sleep(1)
            self.connect()

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, 
                                        socket.SOCK_DGRAM)     
            print("Attempting Connection...")
            self.socket.connect((self.IP, self.PORT))
            print("Will send messages to "+str(self.socket.getpeername()))
            self.connected = True
        except ConnectionRefusedError as ex:
            print("Connection refused. Is server running?")
            self.disconnect()
        except ConnectionResetError as ex:
            print("Server was disconnected...")
            self.disconnect()

"""
mqttClient for avatar
Author: Jayden Chen
Purpose: 

starts a mqtt thread that publishes to a topic
"""
import paho.mqtt.client as mqtt
import random
import threading

class MQTTClient(threading.Thread):

    def run(self):
        self.connect_mqtt()

    def __init__(self, broker,port,publishTopic,clientID = f'python-mqtt-{random.randint(0, 1000)}') -> None:

        threading.Thread.__init__(self)

        self.connected = False

        self.BROKER = broker
        self.PORT = port
        self.PUBLISH_TOPIC = publishTopic
        self.CLIENT_ID = clientID

        self.client = None

        pass

    # for debugging
    def isConnected(self):

        return self.connected

    def sendMessage(self,message):
        try:
            self.client.publish(self.PUBLISH_TOPIC, message)
        except:
            print("Error: publish failed")

    def disconnect(self):

        self.connected = False

        # disconnect gracefully
        self.client.disconnect()
        self.client.loop_stop()

    def connect_mqtt(self):

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt.Client(client_id=self.CLIENT_ID)
        self.client.on_connect = on_connect
        self.client.connect(self.BROKER, self.PORT)
        self.client.loop_start()

        self.connected = True

        return self.client
        