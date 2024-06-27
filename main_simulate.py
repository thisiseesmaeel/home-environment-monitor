import machine
import dht
import time
import random

# DHT11 sensor setup
dht_sensor = dht.DHT11(machine.Pin(28))

# Photoresistor setup
photoresistor = machine.ADC(26)  # Photoresistor connected to GPIO 26

# LED setup
led_green = machine.Pin(13, machine.Pin.OUT)  # Green LED on GPIO 13
led_yellow = machine.Pin(14, machine.Pin.OUT)  # Yellow LED on GPIO 14
led_red = machine.Pin(15, machine.Pin.OUT)  # Red LED on GPIO 15

# Define threshold values
temp_ideal_range = (20, 25)  # Ideal temperature range in celsius
humid_ideal_range = (40, 60)  # Ideal humidity range in percentage
light_ideal_range = (20000, 40000)  # Ideal light level range

# Define warning ranges (slightly outside ideal ranges)
temp_warning_range = (18, 27)  # Warning temperature range in celsius
humid_warning_range = (35, 65)  # Warning humidity range in percentage
light_warning_range = (10000, 50000)  # Warning light level range

# Simulation flag
simulate = False


# Time-based light thresholds
daytime_light_range = (20000, 40000)  # Ideal light range during the day
nighttime_light_range = (0, 5000)     # Ideal light range at night

def is_daytime():
    # Get current hour (0-23)
    current_hour = time.localtime()[3]
    # Consider daytime as 6 AM to 8 PM
    return 6 <= current_hour < 20

def get_light_thresholds():
    if is_daytime():
        return daytime_light_range
    else:
        return nighttime_light_range

def control_leds(temp, humid, light):
    led_green.value(0)
    led_yellow.value(0)
    led_red.value(0)

    light_range = get_light_thresholds()

    if (temp_ideal_range[0] <= temp <= temp_ideal_range[1] and
        humid_ideal_range[0] <= humid <= humid_ideal_range[1] and
        light_range[0] <= light <= light_range[1]):
        led_green.value(1)  # Green LED on
        return "Green"
    elif (temp_warning_range[0] <= temp <= temp_warning_range[1] and
          humid_warning_range[0] <= humid <= humid_warning_range[1] and
          (light_range[0] - 5000 <= light <= light_range[1] + 5000)):  # Wider range for yellow
        led_yellow.value(1)  # Yellow LED on
        return "Yellow"
    else:
        led_red.value(1)  # Red LED on
        return "Red"

# Function to simulate sensor values
def simulate_values():
    scenario = random.choice(["ideal", "warning", "critical"])
    if scenario == "ideal":
        temp = random.uniform(temp_ideal_range[0], temp_ideal_range[1])
        humid = random.uniform(humid_ideal_range[0], humid_ideal_range[1])
        light = random.uniform(light_ideal_range[0], light_ideal_range[1])
    elif scenario == "warning":
        temp = random.uniform(temp_warning_range[0], temp_warning_range[1])
        humid = random.uniform(humid_warning_range[0], humid_warning_range[1])
        light = random.uniform(light_warning_range[0], light_warning_range[1])
        # Ensure at least one value is outside ideal range
        if (temp_ideal_range[0] <= temp <= temp_ideal_range[1] and
            humid_ideal_range[0] <= humid <= humid_ideal_range[1] and
            light_ideal_range[0] <= light <= light_ideal_range[1]):
            choice = random.choice(["temp", "humid", "light"])
            if choice == "temp":
                temp = random.choice([temp_warning_range[0], temp_warning_range[1]])
            elif choice == "humid":
                humid = random.choice([humid_warning_range[0], humid_warning_range[1]])
            else:
                light = random.choice([light_warning_range[0], light_warning_range[1]])
    else:  # critical
        temp = random.uniform(15, 30)
        humid = random.uniform(30, 70)
        light = random.uniform(0, 65535)
        # Ensure at least one value is outside warning range
        if (temp_warning_range[0] <= temp <= temp_warning_range[1] and
            humid_warning_range[0] <= humid <= humid_warning_range[1] and
            light_warning_range[0] <= light <= light_warning_range[1]):
            choice = random.choice(["temp", "humid", "light"])
            if choice == "temp":
                temp = random.choice([14, 31])
            elif choice == "humid":
                humid = random.choice([29, 71])
            else:
                light = random.choice([0, 65535])
    return temp, humid, light

while True:
    try:
        if simulate:
            temp, humid, light = simulate_values()
        else:
            # Read temperature and humidity from DHT22
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            humid = dht_sensor.humidity()

            # Read light level from photoresistor
            light = photoresistor.read_u16()

        print(f"Temperature: {temp:.1f}°C, Humidity: {humid:.1f}%, Light: {light}")
        print(f"Current period: {'Daytime' if is_daytime() else 'Nighttime'}")

        # Control LEDs based on conditions
        led_status = control_leds(temp, humid, light)
        print(f"LED Status: {led_status}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)  # Wait for 2 seconds before reading again
