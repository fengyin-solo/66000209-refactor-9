"""Modbus service with mock data (replace with pymodbus for production).

Device and register (point) defaults are loaded from the shared definition
at <repo>/shared/devices.json, the single source of truth also used by the
frontend, so the device list and the live-read path never drift apart.
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Any

SHARED_DEVICES_FILE = Path(__file__).resolve().parents[3] / "shared" / "devices.json"

def _load_devices() -> List[Dict[str, Any]]:
    with SHARED_DEVICES_FILE.open(encoding="utf-8") as f:
        return json.load(f)["devices"]

DEVICES = _load_devices()

def get_device_status() -> List[Dict[str, Any]]:
    # Response keeps its existing shape: device info without register details.
    return [{k: v for k, v in dev.items() if k != "registers"} for dev in DEVICES]

def read_registers(device_id: str, address: int, count: int) -> Dict[str, Any]:
    """Read registers via pymodbus (mock implementation)."""
    # In production: from pymodbus.client import ModbusTcpClient
    # client = ModbusTcpClient(host, port=port)
    # result = client.read_holding_registers(address, count, slave=slave_id)
    device = next((d for d in DEVICES if d["id"] == device_id), None)
    points = {r["address"]: r for r in device["registers"]} if device else {}
    values = []
    for offset in range(count):
        point = points.get(address + offset)
        if point is None:
            values.append(round(random.uniform(0, 100), 2))
        elif isinstance(point["value"], bool):
            values.append(float(point["value"]))
        else:
            base = float(point["value"])
            noise = (random.random() - 0.5) * base * 0.02
            values.append(round(base + noise, 2))
    return {"device_id": device_id, "address": address, "values": values}
