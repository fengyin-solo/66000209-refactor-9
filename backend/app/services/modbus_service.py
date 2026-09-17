"""Modbus service with mock data (replace with pymodbus for production).

Device and register defaults (count, names, units, initial values) come from
shared/devices.json at the repository root — the single definition shared with
the frontend. Edit that file to change them for both sides at once.
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional

DEVICE_DEFS_PATH = Path(__file__).resolve().parents[3] / "shared" / "devices.json"

def _load_device_definitions() -> List[Dict[str, Any]]:
    with open(DEVICE_DEFS_PATH, encoding="utf-8") as f:
        return json.load(f)["devices"]

DEVICE_DEFINITIONS = _load_device_definitions()

# List view keeps the exact shape /api/modbus/devices has always returned.
MOCK_DEVICES = [
    {key: d[key] for key in ("id", "name", "ip", "port", "slave_id", "online")}
    for d in DEVICE_DEFINITIONS
]

def get_device_status() -> List[Dict[str, Any]]:
    return MOCK_DEVICES

def _initial_value(device_id: str, address: int) -> Optional[float]:
    for d in DEVICE_DEFINITIONS:
        if d["id"] == device_id:
            for r in d["registers"]:
                # bool is excluded: coils have no meaningful holding-register jitter
                if r["address"] == address and type(r["value"]) in (int, float):
                    return r["value"]
    return None

def read_registers(device_id: str, address: int, count: int) -> Dict[str, Any]:
    """Read registers via pymodbus (mock implementation)."""
    # In production: from pymodbus.client import ModbusTcpClient
    # client = ModbusTcpClient(host, port=port)
    # result = client.read_holding_registers(address, count, slave=slave_id)
    values = []
    for i in range(count):
        base = _initial_value(device_id, address + i)
        if base is None:
            values.append(round(random.uniform(0, 100), 2))
        else:
            # Same ±2% jitter around the shared initial value the frontend applies
            noise = (random.random() - 0.5) * base * 0.02
            values.append(round(base + noise, 2))
    return {"device_id": device_id, "address": address, "values": values}
