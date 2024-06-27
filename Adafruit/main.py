import time
from mqtt import MQTTClient
import machine
import micropython
from machine import Pin, ADC
import dht
import keys
import wifiConnection

# LED setup
led_green = Pin(13, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
led_red = Pin(15, Pin.OUT)

# Ensure all LEDs are off at start
led_green.value(0)
led_yellow.value(0)
led_red.value(0)

# Turn off Pico's onboard LED
pico_led = Pin("LED", Pin.OUT)
pico_led.off()

# Sensor setup
dht_sensor = dht.DHT11(Pin(28))
photoresistor = ADC(26)

# Intervals and timeouts
SENSOR_INTERVAL = 30000  # 30 seconds
MANUAL_TIMEOUT = 15000  # 15 seconds
MODE_UPDATE_INTERVAL = 30000  # 30 seconds

# Tracking variables
last_sensor_sent_ticks = 0
last_manual_control = 0
last_mode_update = 0
manual_override = False

# Ideal ranges
temp_ideal = (20, 25)
humid_ideal = (40, 60)
light_ideal = (20000, 40000)

def sub_cb(topic, msg):
    print(f"Received message on topic {topic}: {msg}")
    if topic == bytes(keys.AIO_LED_CONTROL_FEED, 'utf-8'):
        manual_control_leds(msg.decode())

def manual_control_leds(command):
    global manual_override, last_manual_control
    print("Manual control: ON")

    if command in ["1", "GREEN"]:
        new_state = not led_green.value()
        led_green.value(new_state)
        print(f"Green LED {'ON' if new_state else 'OFF'}")
        update_green_led_indicator(new_state)
    elif command in ["2", "YELLOW"]:
        new_state = not led_yellow.value()
        led_yellow.value(new_state)
        print(f"Yellow LED {'ON' if new_state else 'OFF'}")
        update_yellow_led_indicator(new_state)
    elif command in ["3", "RED"]:
        new_state = not led_red.value()
        led_red.value(new_state)
        print(f"Red LED {'ON' if new_state else 'OFF'}")
        update_red_led_indicator(new_state)
    elif command == "OFF":
        led_green.value(0)
        led_yellow.value(0)
        led_red.value(0)
        update_all_led_indicators()
        print("All LEDs OFF")
    else:
        print(f"Unknown command: {command}")
        return

    manual_override = True
    last_manual_control = time.ticks_ms()
    update_mode_indicator()

def update_green_led_indicator(state):
    try:
        client.publish(topic=keys.AIO_GREEN_LED_INDICATOR_FEED, msg=str(int(state)))
        print(f"Green LED indicator updated: {'ON' if state else 'OFF'}")
    except Exception as e:
        print(f"Failed to update Green LED indicator: {e}")

def update_yellow_led_indicator(state):
    try:
        client.publish(topic=keys.AIO_YELLOW_LED_INDICATOR_FEED, msg=str(int(state)))
        print(f"Yellow LED indicator updated: {'ON' if state else 'OFF'}")
    except Exception as e:
        print(f"Failed to update Yellow LED indicator: {e}")

def update_red_led_indicator(state):
    try:
        client.publish(topic=keys.AIO_RED_LED_INDICATOR_FEED, msg=str(int(state)))
        print(f"Red LED indicator updated: {'ON' if state else 'OFF'}")
    except Exception as e:
        print(f"Failed to update Red LED indicator: {e}")

def update_all_led_indicators():
    update_green_led_indicator(led_green.value())
    update_yellow_led_indicator(led_yellow.value())
    update_red_led_indicator(led_red.value())

def auto_control_leds(temp, humid, light):
    if temp_ideal[0] <= temp <= temp_ideal[1] and \
       humid_ideal[0] <= humid <= humid_ideal[1] and \
       light_ideal[0] <= light <= light_ideal[1]:
        led_green.value(1)
        led_yellow.value(0)
        led_red.value(0)
        print("Auto control: Green LED ON, Yellow LED OFF, Red LED OFF")
    elif (temp_ideal[0] - 2 <= temp <= temp_ideal[1] + 2) and \
         (humid_ideal[0] - 5 <= humid <= humid_ideal[1] + 5) and \
         (light_ideal[0] - 5000 <= light <= light_ideal[1] + 5000):
        led_green.value(0)
        led_yellow.value(1)
        led_red.value(0)
        print("Auto control: Green LED OFF, Yellow LED ON, Red LED OFF")
    else:
        led_green.value(0)
        led_yellow.value(0)
        led_red.value(1)
        print("Auto control: Green LED OFF, Yellow LED OFF, Red LED ON")

    update_all_led_indicators()

def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humid = dht_sensor.humidity()
        light = photoresistor.read_u16()
        return temp, humid, light
    except Exception as e:
        print('Error reading sensors:', e)
        return None, None, None

def send_sensor_data():
    global last_sensor_sent_ticks, manual_override
    current_time = time.ticks_ms()
    if (current_time - last_sensor_sent_ticks) < SENSOR_INTERVAL:
        return

    temp, humid, light = read_sensors()
    if temp is not None:
        print(f"Temperature: {temp}°C, Humidity: {humid}%, Light: {light}")

        try:
            client.publish(topic=keys.AIO_TEMPERATURE_FEED, msg=str(temp))
            client.publish(topic=keys.AIO_HUMIDITY_FEED, msg=str(humid))
            client.publish(topic=keys.AIO_LIGHT_SENSOR_FEED, msg=str(light))
            print("Sensor data published successfully")

            if not manual_override or (current_time - last_manual_control) > MANUAL_TIMEOUT:
                if manual_override:
                    manual_override = False
                    update_mode_indicator()
                auto_control_leds(temp, humid, light)
                print("Auto LED control applied")
            else:
                update_all_led_indicators()

        except Exception as e:
            print(f"Failed to publish sensor data: {e}")
    else:
        print("Failed to read sensor data")

    last_sensor_sent_ticks = current_time

def update_mode_indicator():
    global last_mode_update
    current_time = time.ticks_ms()
    if (current_time - last_mode_update) >= MODE_UPDATE_INTERVAL:
        mode = "MANUAL" if manual_override else "AUTO"
        try:
            client.publish(topic=keys.AIO_MODE_INDICATOR_FEED, msg=mode)
            print(f"Mode indicator updated: {mode}")
        except Exception as e:
            print(f"Failed to update mode indicator: {e}")
        last_mode_update = current_time

# Connect to WiFi
try:
    ip = wifiConnection.connect()
    print(f"Connected to WiFi. IP: {ip}")
except Exception as e:
    print(f"Failed to connect to WiFi: {e}")
    machine.reset()

# Connect to Adafruit IO MQTT server
client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
client.set_callback(sub_cb)
try:
    client.connect()
    client.subscribe(keys.AIO_LED_CONTROL_FEED)
    print(f"Connected to {keys.AIO_SERVER}, subscribed to {keys.AIO_LED_CONTROL_FEED} topic")
except Exception as e:
    print(f"Failed to connect to Adafruit IO: {e}")
    machine.reset()

# Main loop
try:
    while True:
        client.check_msg()
        send_sensor_data()
        update_mode_indicator()
        time.sleep(1)  # Small delay to prevent tight looping
except Exception as e:
    print(f"An error occurred in the main loop: {e}")
finally:
    client.disconnect()
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO and WiFi.")
