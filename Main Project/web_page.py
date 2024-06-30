def web_page(temp, humid, light, led_status, mode):
    led_color = {"Green": "#28a745", "Yellow": "#ffc107", "Red": "#dc3545", "Off": "#6c757d"}.get(led_status, "#6c757d")

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sensor Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .dashboard {{
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                padding: 20px;
                width: 100%;
                max-width: 500px;
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 20px;
            }}
            .sensor-data {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }}
            .sensor-item {{
                background-color: #e9ecef;
                border-radius: 5px;
                padding: 15px;
                text-align: center;
            }}
            .sensor-value {{
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
            }}
            .led-status {{
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 20px;
            }}
            .led-indicator {{
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background-color: {led_color};
                margin-right: 10px;
            }}
            .led-controls {{
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
            }}
            .led-button {{
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .led-button.green {{ background-color: #28a745; color: white; }}
            .led-button.yellow {{ background-color: #ffc107; color: black; }}
            .led-button.red {{ background-color: #dc3545; color: white; }}
            .led-button.off {{ background-color: #6c757d; color: white; }}
            .mode-toggle {{
                display: flex;
                justify-content: center;
                margin-top: 20px;
            }}
            .mode-button {{
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                background-color: #007bff;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>Sensor Dashboard</h1>
            <div class="sensor-data">
                <div class="sensor-item">
                    <div>Temperature</div>
                    <div class="sensor-value">{temp:.1f}°C</div>
                </div>
                <div class="sensor-item">
                    <div>Humidity</div>
                    <div class="sensor-value">{humid:.1f}%</div>
                </div>
                <div class="sensor-item">
                    <div>Light</div>
                    <div class="sensor-value">{light}</div>
                </div>
            </div>
            <div class="led-status">
                <div class="led-indicator"></div>
                <div>Status: {led_status}</div>
            </div>
            <div class="mode-toggle">
                <button class="mode-button" onclick="toggleMode()">{mode} Mode</button>
            </div>
            <div class="led-controls">
                <button class="led-button green" onclick="controlLED('green')">Green LED</button>
                <button class="led-button yellow" onclick="controlLED('yellow')">Yellow LED</button>
                <button class="led-button red" onclick="controlLED('red')">Red LED</button>
                <button class="led-button off" onclick="controlLED('off')">All Off</button>
            </div>
        </div>
        <script>
            function controlLED(color) {{
                let state = color === 'off' ? 0 : 1;
                let ledColor = color === 'off' ? 'green' : color;
                fetch(`/led?color=${{ledColor}}&state=${{state}}`, {{method: 'POST'}})
                    .then(response => response.text())
                    .then(data => {{
                        alert(data);
                        location.reload();
                    }});
            }}

            function toggleMode() {{
                fetch('/toggle_mode', {{method: 'POST'}})
                    .then(response => response.text())
                    .then(data => {{
                        alert("Switched to " + data + " mode");
                        location.reload();
                    }});
            }}

            setTimeout(function(){{
                window.location.reload(1);
            }}, 5000);
        </script>
    </body>
    </html>
    """
    return html
