import machine
import dht

class SensorManager:
    def __init__(self):
        self.dht_sensor = dht.DHT11(machine.Pin(28))
        self.photoresistor = machine.ADC(26)

    def read_sensors(self):
        try:
            self.dht_sensor.measure()
            temp = self.dht_sensor.temperature()
            humid = self.dht_sensor.humidity()
            light = self.photoresistor.read_u16()
            return temp, humid, light
        except Exception as e:
            print('Error reading sensors:', e)
            return None, None, None
