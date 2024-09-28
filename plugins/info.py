import os
import psutil
import time
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import timedelta

from bot import Bot  # Ensure to replace this with your actual bot import

# Define a target to ping (e.g., Google DNS)
PING_TARGET = "8.8.8.8"  # Google's public DNS server

# Function to get the ping result
def get_ping(target):
    try:
        # Use subprocess to ping the target
        ping_command = ['ping', '-c', '1', target]
        output = subprocess.check_output(ping_command).decode('utf-8')

        # Extract the ping time from the output (depends on the format of your system's ping command)
        ping_time = output.split('time=')[1].split(' ms')[0]
        return float(ping_time)
    except Exception as e:
        return None

# Function to get detailed system stats
def get_system_stats():
    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(timedelta(seconds=uptime_seconds))

    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=False)  # Physical cores
    cpu_logical = psutil.cpu_count(logical=True)  # Logical cores
    cpu_freq = psutil.cpu_freq().current  # Current CPU frequency in MHz

    # Memory Usage
    memory_info = psutil.virtual_memory()
    total_memory = round(memory_info.total / (1024 ** 3), 2)  # GB
    used_memory = round(memory_info.used / (1024 ** 3), 2)  # GB
    memory_usage_percent = memory_info.percent

    # Disk Usage
    disk_info = psutil.disk_usage('/')
    total_disk = round(disk_info.total / (1024 ** 3), 2)  # GB
    used_disk = round(disk_info.used / (1024 ** 3), 2)  # GB
    disk_usage_percent = disk_info.percent

    # Network Usage
    net_info = psutil.net_io_counters()
    bytes_sent = round(net_info.bytes_sent / (1024 ** 2), 2)  # Convert to MB
    bytes_recv = round(net_info.bytes_recv / (1024 ** 2), 2)  # Convert to MB

    # Temperature (if available)
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            core_temps = temps['coretemp']
            cpu_temp = core_temps[0].current  # CPU temperature in Celsius
        else:
            cpu_temp = "N/A"
    except AttributeError:
        cpu_temp = "N/A"

    # Running processes count
    processes_count = len(psutil.pids())

    # Get system load (1, 5, 15 minute averages)
    load1, load5, load15 = psutil.getloadavg()

    # Get ping result
    ping_result = get_ping(PING_TARGET)
    ping_message = f"{ping_result} ms" if ping_result is not None else "Ping failed"

    # Formatted message with stats
    stats_message = f"""
    <b>📊 Server Stats:</b>

    🖥️ <b>Uptime:</b> {uptime_str}

    💻 <b>CPU Usage:</b> {cpu_usage}%
    ⚙️ <b>CPU Cores:</b> {cpu_count} physical, {cpu_logical} logical
    📈 <b>CPU Frequency:</b> {cpu_freq} MHz
    🌡️ <b>CPU Temperature:</b> {cpu_temp}°C

    🧠 <b>Memory Usage:</b> {used_memory} GB / {total_memory} GB ({memory_usage_percent}%)

    💾 <b>Disk Usage:</b> {used_disk} GB / {total_disk} GB ({disk_usage_percent}%)

    🔄 <b>Load Averages:</b> 1 min: {load1}, 5 min: {load5}, 15 min: {load15}

    📡 <b>Ping:</b> {ping_message}

    🌐 <b>Network:</b>
    ⬆️ Sent: {bytes_sent} MB
    ⬇️ Received: {bytes_recv} MB

    🔢 <b>Running Processes:</b> {processes_count}
    """

    return stats_message

# Command to fetch and send server stats
@Bot.on_message(filters.command("info"), group=7664)
async def send_server_info(client: Bot, message: Message):
    # Get the system stats
    stats_message = get_system_stats()
    
    # Send the stats as a reply to the user
    await message.reply_text(stats_message, parse_mode="html")

