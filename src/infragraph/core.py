from __future__ import annotations

def build_graph(devices: list[dict]) -> dict[str,list[str]]:
    return {device["name"]: sorted(set(device.get("neighbors", []))) for device in devices}
