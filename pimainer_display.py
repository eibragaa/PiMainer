import requests
import json
import time
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

# --- Configuração Inicial ---
console = Console()
start_time = datetime.now()

# APIs
URL_BLOCK_TIP = "https://mempool.space/api/blocks/tip/height"
URL_FEES = "https://mempool.space/api/v1/fees/recommended"
URL_MINER_API = "http://127.0.0.1:4048"

# --- Funções para Coleta de Dados ---

def format_hashrate(hashrate_hs):
    """Formata o hashrate de H/s para uma unidade legível (KH/s, MH/s, etc.)."""
    if hashrate_hs is None:
        return "N/A"
    if hashrate_hs < 1000:
        return f"{hashrate_hs:.2f} H/s"
    if hashrate_hs < 1000000:
        return f"{hashrate_hs / 1000:.2f} KH/s"
    return f"{hashrate_hs / 1000000:.2f} MH/s"

def get_miner_data():
    """Coleta dados do minerador via API local."""
    try:
        response = requests.get(URL_MINER_API, timeout=2)
        if response.status_code == 200:
            data = response.json()
            hashrate_10s = data.get("hashrate", {}).get("total", [None])[0]
            return format_hashrate(hashrate_10s)
    except requests.RequestException:
        return "Offline"
    return "N/A"

def get_system_data():
    """Coleta dados do sistema como temperatura e uptime."""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            cpu_temp = f"{int(f.read().strip()) / 1000.0:.1f}°C"
    except FileNotFoundError:
        cpu_temp = "N/A"

    total_seconds = int((datetime.now() - start_time).total_seconds())
    uptime_str = f"{total_seconds}S"

    return cpu_temp, uptime_str

def get_network_data():
    """Coleta dados da rede Bitcoin via API."""
    try:
        height_res = requests.get(URL_BLOCK_TIP, timeout=5)
        block_height = height_res.json() if height_res.status_code == 200 else 0
        return {"block_height": block_height}
    except requests.RequestException:
        return {"block_height": 0}

# --- Funções de Construção da UI ---

def build_stat_card(label: str, value: str, style: str) -> Panel:
    return Panel(
        Text(f"{label}\n", style="default", justify="center") + Text(str(value), style=f"bold {style}", justify="center"),
        border_style=style,
        padding=(1, 1)
    )

def generate_layout(sys_data: dict, net_data: dict, miner_data: dict) -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(Text("PiMainer Dashboard", style="bold white", justify="center"), name="header", size=3),
        Layout(ratio=1, name="main"),
        Layout(Text("Pressione CTRL+C para sair", style="dim", justify="center"), name="footer", size=3),
    )

    interface_layout = Layout(name="interface")
    interface_layout.split(
        Layout(Text("CRYPTO² MINER", style="bold white", justify="center"), name="title", size=3),
        Layout(Text(datetime.now().strftime('%H:%M:%S'), style="bold white", justify="center"), name="clock", size=3),
        Layout(name="stats_grid"),
        Layout(name="status_bar", size=3)
    )

    stats_table = Table.grid(expand=True, padding=1)
    stats_table.add_column()
    stats_table.add_column()

    hash_rate_card = build_stat_card("HASH RATE", miner_data['hashrate'], "#FFC107")
    block_card = build_stat_card("CURRENT BLOCK", f"{net_data['block_height']:,}", "#03A9F4")
    uptime_card = build_stat_card("UPTIME", sys_data['uptime'], "#4CAF50")
    temp_card = build_stat_card("TEMPERATURE", sys_data['cpu_temp'], "#FF5252")

    stats_table.add_row(hash_rate_card, block_card)
    stats_table.add_row(uptime_card, temp_card)
    interface_layout["stats_grid"].update(Align.center(stats_table))

    status_bar = Table.grid(expand=True, padding=(0, 2))
    status_bar.add_column()
    status_bar.add_column()
    status_bar.add_row(
        Text("⛏️ MINING", style="green"),
        Text("📶 API CONNECTED", style="green"),
    )
    interface_layout["status_bar"].update(Align.center(status_bar))
    layout["main"].update(Panel(interface_layout, border_style="blue"))
    return layout

# --- Loop Principal ---
if __name__ == "__main__":
    try:
        with Live(console=console, screen=True, redirect_stderr=False, transient=True) as live:
            while True:
                miner_hashrate = get_miner_data()
                sys_temp, sys_uptime = get_system_data()
                net_info = get_network_data()

                live.update(generate_layout(
                    {"uptime": sys_uptime, "cpu_temp": sys_temp},
                    net_info,
                    {"hashrate": miner_hashrate}
                ))
                time
