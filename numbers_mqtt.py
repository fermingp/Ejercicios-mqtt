
from paho.mqtt.client import Client
import traceback
import sys
from sympy import isprime


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n =  float(msg.payload)
        if n%1 == 0:
            n =  int(msg.payload)
            userdata['frec_enteros'] += 1
            client.publish('/clients/frec_enteros', f'{userdata["frec_enteros"]}')
            client.publish('/clients/enteros', n)
            if n%2==0:
                client.publish('/clients/par', n)
            else:
                client.publish('clients/impar',n)
            if isprime(n):
                client.publish('/clients/primo', n)
            else:
                client.publish('/clients/compuesto', n)

        else:
            userdata['frec_reales'] += 1
            client.publish('/clients/frec_reales', f'{userdata["frec_reales"]}')
            client.publish('/clients/reales', n)
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(broker):
    userdata = {
        'frec_enteros': 0,
        'frec_reales':0
    }
    client = Client(userdata=userdata)
    client.on_message = on_message
    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)
    
    client.subscribe('numbers')
    client.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)