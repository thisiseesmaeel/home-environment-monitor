from wifi_manager import connect_to_wifi
from sensor_manager import SensorManager
from led_manager import LEDManager
from web_server import start_server

def main():
    connect_to_wifi()
    sensor_manager = SensorManager()
    led_manager = LEDManager()
    start_server(sensor_manager, led_manager)

if __name__ == "__main__":
    main()
