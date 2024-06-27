# Home Environment Monitoring System

By Ismail Safwat (ss226ru)

## Project Overview

This project guides you through building a Home Environment Monitoring System using a Raspberry Pi Pico WH. The system measures and displays temperature, humidity, and light levels in a room or multiple rooms. It provides real-time data through a web interface and uses LEDs for visual status indication.

I've developed two variants of this system:
1. The main project version for real-world deployment
2. A simulation-capable version for testing and demonstration purposes

**Estimated Time:** 20 mins for basic setup, additional time for exploring both variants

## Objective

The Home Environment Monitoring System was developed for the following reasons:

1. **Comfort Optimization:** Monitor temperature and humidity to ensure optimal living conditions.
2. **Energy Efficiency:** Understand light levels to optimize artificial lighting usage.
3. **Data-Driven Decisions:** Collect data for insights into environmental patterns.
4. **Learning Experience:** Gain hands-on experience with IoT and home automation.
5. **Testing and Demonstration:** The simulation variant allows for comprehensive testing and showcasing of system behavior under various conditions.

## Materials

- Raspberry Pi Pico WH
- DHT11 Digital Temperature and Humidity Sensor
- Photoresistor (CdS)
- LEDs (1 red, 1 yellow, 1 green)
- Resistors (3 x 500Ω for LEDs, 1 x 4.7kΩ for photoresistor)
- Breadboard
- Jumper Wires

![Components](images/x.png)

## Computer Setup

1. Download and install [Thonny IDE](https://thonny.org/).
2. Connect Raspberry Pi Pico WH to your computer via USB.
3. In Thonny, go to "Run" > "Configure Interpreter" > "Interpreter" and select "MicroPython (Raspberry Pi Pico)".
4. Click on "Install or update firmware" to ensure you have the latest MicroPython firmware.

## Hardware Assembly

Connect the components as follows:

1. DHT11 Sensor:
   - VCC to 3.3V
   - GND to GND
   - DATA to GPIO 28
2. Photoresistor:
   - One leg to 3.3V
   - Other leg to GPIO 26 and to GND through a 4.7kΩ resistor
3. LEDs (each with a 500Ω resistor):
   - Green LED to GPIO 13
   - Yellow LED to GPIO 14
   - Red LED to GPIO 15

![Circuit Diagram](images/circuit_diagram.png)

## Platform

This project uses a local web server hosted on the Raspberry Pi Pico WH, offering:

- Simplicity
- Privacy
- Low Latency
- Cost-Effectiveness

## Code Overview

These are two variants of the code:

### Main Project Version

```python
import machine
import dht
import network
import socket
import time

# Sensor setup
dht_sensor = dht.DHT11(machine.Pin(28))
photoresistor = machine.ADC(26)

# LED setup
led_green = machine.Pin(13, machine.Pin.OUT)
led_yellow = machine.Pin(14, machine.Pin.OUT)
led_red = machine.Pin(15, machine.Pin.OUT)

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

def control_leds(temp, humid, light):
    # LED control logic here
    pass

# Web server setup and main loop here
```

### Key Features of the Main Project Version:

1. **Real-time Sensor Reading:** This version reads actual data from the DHT11 sensor and photoresistor in real-time.
2. **Web Server Integration:** Implements a local web server to display sensor data and control LEDs remotely.
3. **LED Status Indication:** Uses LEDs to provide a visual representation of the current environmental conditions.
4. **Wi-Fi Connectivity:** Connects to a local Wi-Fi network to make the dashboard accessible from other devices.

### Key Functions in the Main Project Version:

`connect_to_wifi()`
Establishes a connection to the specified Wi-Fi network, enabling remote access to the dashboard.

`read_sensors()`
Reads and returns the current temperature, humidity, and light levels from the physical sensors.

`control_leds(temp, humid, light)`
Sets the LED status based on the current sensor readings, indicating whether conditions are ideal, acceptable, or outside the desired range.

`web_page(temp, humid, light, led_status, mode)`
Generates the HTML for the web dashboard, displaying current sensor readings and LED status.

`parse_request(request)`
Parses incoming HTTP requests to handle user interactions with the web dashboard.

`handle_led_request(path)`
Processes requests to manually control the LEDs through the web interface.

`toggle_mode()`
Switches between automatic and manual LED control modes.

`start_server(port=80)`
Initializes and runs the web server, handling incoming connections and serving the dashboard.

### Simulation-Capable Version

This version includes additional features for testing and demonstration:

```python
import machine
import dht
import time
import random

# [Sensor and LED setup remains the same]

# Define threshold values
temp_ideal_range = (20, 25)
humid_ideal_range = (40, 60)
light_ideal_range = (20000, 40000)

# Define warning ranges
temp_warning_range = (18, 27)
humid_warning_range = (35, 65)
light_warning_range = (10000, 50000)

# Simulation flag
simulate = False

# Time-based light thresholds
daytime_light_range = (20000, 40000)
nighttime_light_range = (0, 5000)

def is_daytime():
    current_hour = time.localtime()[3]
    return 6 <= current_hour < 20

def get_light_thresholds():
    return daytime_light_range if is_daytime() else nighttime_light_range

def control_leds(temp, humid, light):
    # Enhanced LED control logic here
    pass

def simulate_values():
    # Simulation logic here
    pass

# Main loop with simulation option
```


### Key Features of the Simulation-Capable Version:

1. **Time-based Light Thresholds:**
This version adjusts light level expectations based on the time of day.
2. **Simulation Mode:**
A simulate flag allows the system to generate mock sensor data for testing purposes.
3. **Enhanced LED Control:** 
The LED status is determined by more nuanced conditions, including time-of-day considerations for light levels.
4. **Error Handling:**
The main loop includes exception handling to manage potential errors gracefully.

## Key Functions in the Simulation Version
`is_daytime()` 
Determines if it's currently daytime (6 AM to 8 PM) based on the system's current hour.

`get_light_thresholds()`
Returns appropriate light level thresholds based on whether it's daytime or nighttime.

`control_leds(temp, humid, light)`
Sets the LED status based on how closely the current conditions match the ideal ranges, considering the time of day for light levels.

`simulate_values()`
When simulation mode is active, this function generates realistic mock data for temperature, humidity, and light levels.

## Choosing Between Versions

1. Use the main project version for actual deployment and real-world monitoring.
2. Use the simulation-capable version for testing, demonstrations, and understanding system behavior under various conditions.

To use the simulation version, replace the main code with this variant and set the `simulate` flag to `True` when you want to run in simulation mode.

## Data Transmission

- **Wireless Protocol:** Wi-Fi (client mode)
- **Transport Protocol:** HTTP
- **Frequency:** Auto-refresh every 5 seconds

In the simulation version, mock data is generated and processed similarly to real sensor data.

## Data Presentation

- Responsive web dashboard
- Auto-refreshes every 5 seconds
- Displays temperature, humidity, and light levels
- Manual LED control option
- In the simulation version, indicates whether it's "Daytime" or "Nighttime"

![Dashboard](images/dashboard.png)

## Future Improvements

1. Implement long-term data storage and trend analysis using cloud servers (e.g., Adafruit, ThingSpeak)
2. Merge simulation capabilities into the main version for a more versatile single system
3. Develop a user interface to easily switch between real and simulated data


![Final Setup](images/x.png)

This project demonstrates the potential of DIY IoT solutions for home monitoring and automation, providing valuable insights into your living environment while offering a great learning experience in hardware and software integration. The addition of a simulation-capable version enhances its utility for testing, demonstration, and educational purposes.
