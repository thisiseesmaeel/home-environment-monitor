import socket
from web_page import web_page
import time

def start_server(sensor_manager, led_manager, port=80):
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
            s = socket.socket()
            s.bind(addr)
            s.listen(1)
            print(f'Listening on http://{addr[0]}:{addr[1]}/')

            while True:
                try:
                    cl, addr = s.accept()
                    print('Client connected from', addr)
                    request = cl.recv(1024)
                    method, path = parse_request(request)

                    if method == 'GET' and path == '/':
                        temp, humid, light = sensor_manager.read_sensors()
                        if temp is not None:
                            led_status = led_manager.control_leds(temp, humid, light)
                            mode = "Manual" if led_manager.manual_mode else "Auto"
                            response = web_page(temp, humid, light, led_status, mode)
                        else:
                            response = "Error reading sensors"
                    elif method == 'POST' and path.startswith('/led'):
                        response = handle_led_request(path, led_manager)
                    elif method == 'POST' and path == '/toggle_mode':
                        response = led_manager.toggle_mode()
                    else:
                        response = "404 Not Found"

                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()
                except Exception as e:
                    print('Client handling error:', e)
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f'Port {port} is busy, trying again in 10 seconds...')
                time.sleep(10)
            else:
                print('Unexpected error:', e)
                break
        except Exception as e:
            print('Unexpected error:', e)
            break
    else:
        print(f'Failed to start server after {max_attempts} attempts')

def parse_request(request):
    try:
        request = request.decode('utf-8')
        request_line = request.split('\r\n')[0]
        parts = request_line.split()
        if len(parts) < 2:
            return None, None
        method, path = parts[0], parts[1]
        return method, path
    except Exception as e:
        print('Error parsing request:', e)
        return None, None

def handle_led_request(path, led_manager):
    try:
        params = path.split('?')[1].split('&')
        color = None
        state = None
        for param in params:
            key, value = param.split('=')
            if key == 'color':
                color = value.lower()
            elif key == 'state':
                state = int(value)
        if color and state is not None:
            return led_manager.set_led(color, state)
        return "Invalid request"
    except Exception as e:
        print('Error handling LED request:', e)
        return "Error processing request"
