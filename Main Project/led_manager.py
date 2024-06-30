import machine

class LEDManager:
    def __init__(self):
        self.led_green = machine.Pin(13, machine.Pin.OUT)
        self.led_yellow = machine.Pin(14, machine.Pin.OUT)
        self.led_red = machine.Pin(15, machine.Pin.OUT)
        self.manual_mode = False
        self.current_led_status = "Auto"

    def control_leds(self, temp, humid, light):
        if self.manual_mode:
            return self.current_led_status

        self.led_green.value(0)
        self.led_yellow.value(0)
        self.led_red.value(0)

        temp_ideal = (20, 25)
        humid_ideal = (40, 60)
        light_ideal = (20000, 40000)

        if (temp_ideal[0] <= temp <= temp_ideal[1] and
            humid_ideal[0] <= humid <= humid_ideal[1] and
            light_ideal[0] <= light <= light_ideal[1]):
            self.led_green.value(1)
            self.current_led_status = "Green"
        elif (18 <= temp <= 27 and
              35 <= humid <= 65 and
              10000 <= light <= 50000):
            self.led_yellow.value(1)
            self.current_led_status = "Yellow"
        else:
            self.led_red.value(1)
            self.current_led_status = "Red"

        return self.current_led_status


    def set_led(self, color, state):
        led_map = {"green": self.led_green, "yellow": self.led_yellow, "red": self.led_red}

        if color in led_map:
            self.led_green.value(0)
            self.led_yellow.value(0)
            self.led_red.value(0)

            led_map[color].value(state)

            self.current_led_status = color.upper() if state else "Off"

            return f"{color.upper()} LED turned {'on' if state else 'off'}"
        return "Invalid LED color"

    def toggle_mode(self):
        self.manual_mode = not self.manual_mode
        return "Manual" if self.manual_mode else "Auto"
