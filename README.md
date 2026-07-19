# InfraGraph

Build infrastructure dependency graphs, calculate failure blast radius, and find single points of failure before an outage does.

InfraGraph models a simple but operationally useful relationship: **source depends on target**. From that inventory it can answer:

- What breaks if this switch, service, site, database, or provider fails?
- Which critical systems are transitively affected?
- Why is a service affected?
- Which nodes are single points of failure?
- What does the dependency topology look like?

## Quick start

```bash
pip install -e ".[dev]"
infragraph examples/campus.json impact core-sw
```

Example output:

```text
Failed: core-sw
Impacted (3): auth, dns, portal
Critical impacts: auth, dns, portal
  auth: auth -> dns -> core-sw
  dns: dns -> core-sw
  portal: portal -> auth -> dns -> core-sw
```

The command exits with status `1` when critical systems are impacted, making it suitable for maintenance checks and CI policy gates.

## Commands

```bash
# Calculate failure blast radius
infragraph inventory.json impact edge-fw core-sw

# Machine-readable report
infragraph inventory.json impact edge-fw --json

# Show everything a node depends on
infragraph inventory.json chain portal

# Find nodes whose loss affects critical services
infragraph inventory.json spof

# Export a Mermaid diagram
infragraph inventory.json mermaid -o topology.mmd
```

## Inventory format

```json
{
  "nodes": [
    {"id": "core-sw", "kind": "switch", "criticality": "high"},
    {"id": "dns", "kind": "service", "criticality": "critical"}
  ],
  "dependencies": [
    {"source": "dns", "target": "core-sw", "kind": "network"}
  ]
}
```

Dependencies are directional: `dns -> core-sw` means DNS requires the core switch. Required dependencies use solid Mermaid edges; optional dependencies use dashed edges.

## Python API

```python
import json
from infragraph import build_graph

payload = json.loads(open("inventory.json").read())
graph = build_graph(payload)
report = graph.blast_radius("core-sw")
print(report.critical_impacts)
```

## Portfolio relevance

InfraGraph demonstrates graph modelling, transitive dependency analysis, deterministic exports, operational risk analysis, typed Python APIs, CLI design, testing, and CI-friendly automation.
