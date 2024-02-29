import configparser
import os
import pygame
import subprocess
import platform
import time

CONFIG_FILE = 'config.ini'
CONFIG_SECTION = 'Settings'

def get_server_ip(server_name):
    servers = {
        "US West": "137.221.105.2",
        "US Central": "24.105.62.129",
        "Europe": "185.60.112.157",
        "Korea": "211.115.104.1",
        "Taiwan": "5.42.162.1",
        "Oceania": "103.4.115.248"
    }
    return servers.get(server_name, "24.105.62.129")  # Default to US Central if not found

def prompt_for_settings(config):
    high_ping_threshold = input("Enter the high ping threshold (ms): ")
    server_name = input("Choose a server (US West, US Central, Europe, Korea, Taiwan, Oceania): ")
    server_ip = get_server_ip(server_name)

    # Ensure high_ping_threshold is stored as a float
    config[CONFIG_SECTION] = {
        'HighPingThreshold': str(float(high_ping_threshold)),  # Convert and store as string
        'Server': server_name
    }

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

    return float(high_ping_threshold), server_ip  # Return as float

def load_or_prompt_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if CONFIG_SECTION not in config or 'HighPingThreshold' not in config[CONFIG_SECTION] or 'Server' not in config[CONFIG_SECTION]:
            return prompt_for_settings(config)
        else:
            high_ping_threshold = config.getfloat(CONFIG_SECTION, 'HighPingThreshold')  # Use getfloat to ensure it's a float
            server_name = config.get(CONFIG_SECTION, 'Server')
            server_ip = get_server_ip(server_name)
            return high_ping_threshold, server_ip
    else:
        return prompt_for_settings(config)


def parse_ping_output(output):
    if "time=" not in output:
        return None
    try:
        if platform.system().lower() == "windows":
            time_index = output.find('time=') + 5
            time_end_index = output.find('ms', time_index)
        else:
            time_index = output.find('time=') + 5
            time_end_index = output.find(' ms', time_index)
        
        ping_time = float(output[time_index:time_end_index])
        return ping_time
    except ValueError:
        print("Error parsing ping output: ", output)
        return None

def ping(host, simulate_timeout=False):
    if simulate_timeout:
        print(f"Simulating timeout for {host}")
        return None  # Simulate a timeout response
    
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        output = subprocess.check_output(command).decode()
        return parse_ping_output(output)
    except subprocess.CalledProcessError:
        print(f"Failed to ping {host}")
        return None


def alert():
    pygame.mixer.init()
    pygame.mixer.music.load('alert.mp3')
    pygame.mixer.music.play()
    time.sleep(2)  # Play for 2 seconds
    pygame.mixer.music.stop()

def monitor_ping(host, threshold, server_name):
    try:
        while True:
            # Force a simulated timeout for testing
            ping_time = ping(host, simulate_timeout=False)
            if ping_time is None:
                print(f"Ping request to {server_name} ({host}) timed out or failed. Treating as high ping.")
                alert()
            elif ping_time > threshold:
                print(f"High ping detected to {server_name} ({host}): {ping_time} ms")
                alert()
            else:
                print(f"Ping to {server_name} ({host}): {ping_time} ms")
            time.sleep(1)  # You might want to increase this during testing to avoid rapid alerts.
    except KeyboardInterrupt:
        print("Program exited by user")

# Adjust where monitor_ping is called to pass the server name:
if __name__ == "__main__":
    high_ping_threshold, host_ip = load_or_prompt_config()
    
    # Retrieve the server name directly if needed:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    server_name = config.get(CONFIG_SECTION, 'Server') if config.has_section(CONFIG_SECTION) and config.has_option(CONFIG_SECTION, 'Server') else "Unknown Server"

    print(f"Monitoring {server_name} ({host_ip}) with a high ping threshold of {high_ping_threshold} ms")
    monitor_ping(host_ip, high_ping_threshold, server_name)

