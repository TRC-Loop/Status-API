from fastapi import FastAPI
from fastapi.responses import JSONResponse
import psutil
import platform
import time
import cpuinfo
import os
import socket

app = FastAPI()

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "used": mem.used,
        "free": mem.free,
        "percent": mem.percent
    }

def get_disk_info():
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except PermissionError:
            continue
    return disks

def get_os_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "node": platform.node()
    }

def get_shell():
    shell = os.environ.get('SHELL') or os.environ.get('COMSPEC') or 'N/A'
    return shell

def get_network_info():
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_io_counters(pernic=True)
    network_data = []

    for interface_name, addrs in interfaces.items():
        ip_addrs = []
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_addrs.append(addr.address)
            elif addr.family == socket.AF_INET6:
                ip_addrs.append(addr.address)
        net_stats = stats.get(interface_name, {})
        network_data.append({
            "interface": interface_name,
            "ip_addresses": ip_addrs,
            "bytes_sent": net_stats.bytes_sent,
            "bytes_recv": net_stats.bytes_recv,
            "packets_sent": net_stats.packets_sent,
            "packets_recv": net_stats.packets_recv,
            "errin": net_stats.errin,
            "errout": net_stats.errout,
            "dropin": net_stats.dropin,
            "dropout": net_stats.dropout
        })
    return network_data

@app.get("/api/v1/status/")
async def full_status():
    return {
        "status": "ok",
        "uptime": get_uptime(),
        "cpu": cpuinfo.get_cpu_info(),
        "cpu_usage_percent": psutil.cpu_percent(),
        "cpu_usage_percent_per": psutil.cpu_percent(percpu=True),
        "memory": get_memory_info(),
        "disks": get_disk_info(),
        "os": get_os_info(),
        "default_shell": get_shell(),
        "network": get_network_info()
    }

@app.get("/api/v1/status/uptime/")
async def uptime():
    return {"status": "ok", "uptime": get_uptime()}

@app.get("/api/v1/status/cpu/")
async def cpu():
    return {
        "status": "ok",
        "cpu": cpuinfo.get_cpu_info(),
        "usage_percent": psutil.cpu_percent(),
        "usage_percent_per": psutil.cpu_percent(percpu=True)
    }

@app.get("/api/v1/status/ram/")
async def ram():
    return {"status": "ok", "memory": get_memory_info()}

@app.get("/api/v1/status/disks/")
async def disks():
    return {"status": "ok", "disks": get_disk_info()}

@app.get("/api/v1/status/os/")
async def os_info():
    return {"status": "ok", "os": get_os_info()}

@app.get("/api/v1/status/network/")
async def network():
    return {"status": "ok", "network": get_network_info()}

@app.get("/api/v1/status/shell/")
async def shell():
    return {"status": "ok", "default_shell": get_shell()}
