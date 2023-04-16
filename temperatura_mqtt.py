from paho.mqtt.client import Client
import sys
import time


def calculo_estadisticas(userdata):
    temp = userdata["temperatures"]
    t_min = min(temp)
    t_max = max(temp)
    mean = sum(temp) // len(temp) #media
    
    t1 = userdata["t1"]
    t1_min = min(t1)
    t1_max = max(t1)
    mean1 = sum(t1) // len(t1)
    
    t2 = userdata["t2"]
    t2_min = min(t2)
    t2_max = max(t2)
    mean2 = sum(t2) // len(t2)
    
    print(f'Total- Max: {t_max}, Min: {t_min}, Media: {mean}')
    print(f'Sensor 1- Max: {t1_max}, Min: {t1_min}, Media: {mean1}')
    print(f'Sensor 2- Max: {t2_max}, Min: {t2_min}, Media: {mean2}')

    
    
def on_message(client, userdata, msg):

    try:
        print(msg.topic, msg.payload)
        n =  float(msg.payload)
        userdata["temperatures"].append(n)
        
        if msg.topic == 'temperature/t1':
            userdata["t1"].append(n)
        else:
            userdata["t2"].append(n)
            
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(hostname):
    userdata = {'temperatures':[], 't1':[],'t2':[]}
    client = Client(userdata=userdata)
    client.on_message = on_message
    print(f'Connecting on channels temperature on {hostname}')
    client.connect(hostname)
    client.subscribe('temperature/#') #escuchar todas las temperaturas
    client.loop_start()
    
    while True:
        time.sleep(5) #Esperamos 5 segundos
        calculo_estadisticas(userdata)


if __name__ == "__main__":
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} hostname")
    hostname = sys.argv[1]
    main(hostname)