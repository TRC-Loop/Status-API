import os
import socket
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
import psutil
import platform
import time
import cpuinfo

# Load API key from environment variable
API_KEY = os.getenv("API_KEY_STATUS")
if not API_KEY:
    raise RuntimeError("Please set the API_KEY_STATUS environment variable.")

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="System Info API",
    description="A comprehensive API to retrieve system metrics like CPU, RAM, Disk, Network, OS info, and more. "
                "Requires an API key for access, set via the 'API_KEY_STATUS' environment variable.",
    version="1.0.0",
    contact={
        "name": "TRC Loop",
        "email": "ak@stellar-code.com",
        "website": "https://github.com/TRC-Loop/Status-API/"
    },
    openapi_tags=[
        {"name": "System Metrics", "description": "Endpoints for system metrics like CPU, RAM, Disk, etc."},
        {"name": "OS Info", "description": "Operating system details."},
        {"name": "Network", "description": "Network interfaces and stats."},
        {"name": "Security", "description": "API key authentication."}
    ]
)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency to verify API key from request headers.
    """
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

def get_uptime():
    """
    Calculate system uptime.
    """
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_memory_info():
    """
    Retrieve virtual memory info.
    """
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "used": mem.used,
        "free": mem.free,
        "percent": mem.percent
    }

def get_disk_info():
    """
    Retrieve disk partitions and usage.
    """
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
    """
    Retrieve OS details.
    """
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
    """
    Retrieve default shell.
    """
    shell = os.environ.get('SHELL') or os.environ.get('COMSPEC') or 'N/A'
    return shell

def get_network_info():
    """
    Retrieve network interfaces and stats.
    """
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

@app.get("/api/v1/status/", tags=["System Metrics"])
async def full_status(api_key: str = Security(get_api_key)):
    """
    Get a full snapshot of system metrics including CPU, RAM, Disk, Network, OS info, and uptime.
    """
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

@app.get("/api/v1/status/uptime/", tags=["System Metrics"])
async def uptime_endpoint(api_key: str = Security(get_api_key)):
    """
    Get system uptime.
    """
    return {"status": "ok", "uptime": get_uptime()}

@app.get("/api/v1/status/cpu/", tags=["System Metrics"])
async def cpu_endpoint(api_key: str = Security(get_api_key)):
    """
    Get CPU info and usage percentages.
    """
    return {
        "status": "ok",
        "cpu": cpuinfo.get_cpu_info(),
        "usage_percent": psutil.cpu_percent(),
        "usage_percent_per": psutil.cpu_percent(percpu=True)
    }

@app.get("/api/v1/status/ram/", tags=["System Metrics"])
async def ram_endpoint(api_key: str = Security(get_api_key)):
    """
    Get RAM usage info.
    """
    return {"status": "ok", "memory": get_memory_info()}

@app.get("/api/v1/status/disks/", tags=["System Metrics"])
async def disks_endpoint(api_key: str = Security(get_api_key)):
    """
    Get disk partitions and usage.
    """
    return {"status": "ok", "disks": get_disk_info()}

@app.get("/api/v1/status/os/", tags=["OS Info"])
async def os_endpoint(api_key: str = Security(get_api_key)):
    """
    Get operating system details.
    """
    return {"status": "ok", "os": get_os_info()}

@app.get("/api/v1/status/network/", tags=["Network"])
async def network_endpoint(api_key: str = Security(get_api_key)):
    """
    Get network interfaces and stats.
    """
    return {"status": "ok", "network": get_network_info()}

@app.get("/api/v1/status/shell/", tags=["System Metrics"])
async def shell_endpoint(api_key: str = Security(get_api_key)):
    """
    Get default shell.
    """
    return {"status": "ok", "default_shell": get_shell()}
