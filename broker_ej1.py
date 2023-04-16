"""
Ejercicio número 1
"""

from paho.mqtt.client import Client

def on_message(client, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain) 
    
def on_publish(mqtcc,userdata,mid):
    print("Mensaje con el topic clients publicado")

def main(broker, topic): 
    client = Client()
    
    print(f'connecting {broker}')
    client.connect(broker)
    client.subscribe(topic)
    client.on_publish = on_publish
    client.on_message = on_message
    
    client.loop_start()
    while True:
        mensaje=input("Ingrese el mensaje a enviar")
        client.publish(topic, mensaje)
    client.loop_stop()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print(f"Usage: {sys.argv[0]} broker topic") 
        sys.exit(1)
    broker = sys.argv[1]
    topic = sys.argv[2]
    main(broker, topic)