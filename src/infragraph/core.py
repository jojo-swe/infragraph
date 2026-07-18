"""Infrastructure dependency graph and impact analysis."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import asdict, dataclass, field
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Node:
    id: str
    kind: str = "service"
    label: str | None = None
    criticality: str = "medium"
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Dependency:
    source: str
    target: str
    kind: str = "depends_on"
    required: bool = True


@dataclass(slots=True)
class ImpactReport:
    failed_nodes: list[str]
    impacted_nodes: list[str]
    critical_impacts: list[str]
    paths: dict[str, list[str]]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class InfrastructureGraph:
    """Directed graph where each source depends on its target."""

    def __init__(self, nodes: Iterable[Node], dependencies: Iterable[Dependency]) -> None:
        self.nodes = {node.id: node for node in nodes}
        self.dependencies = list(dependencies)
        self._validate()
        self._dependents: dict[str, list[str]] = defaultdict(list)
        self._requirements: dict[str, list[str]] = defaultdict(list)
        for edge in self.dependencies:
            self._dependents[edge.target].append(edge.source)
            self._requirements[edge.source].append(edge.target)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "InfrastructureGraph":
        nodes = [Node(**item) for item in payload.get("nodes", [])]  # type: ignore[arg-type]
        edges = [Dependency(**item) for item in payload.get("dependencies", [])]  # type: ignore[arg-type]
        return cls(nodes, edges)

    def _validate(self) -> None:
        missing: set[str] = set()
        for edge in self.dependencies:
            if edge.source not in self.nodes:
                missing.add(edge.source)
            if edge.target not in self.nodes:
                missing.add(edge.target)
        if missing:
            raise ValueError(f"Dependencies reference unknown nodes: {', '.join(sorted(missing))}")

    def blast_radius(self, failed: str | Iterable[str]) -> ImpactReport:
        failed_nodes = [failed] if isinstance(failed, str) else list(failed)
        unknown = sorted(set(failed_nodes) - self.nodes.keys())
        if unknown:
            raise KeyError(f"Unknown node(s): {', '.join(unknown)}")

        queue = deque(failed_nodes)
        paths: dict[str, list[str]] = {node: [node] for node in failed_nodes}
        impacted = set(failed_nodes)
        while queue:
            current = queue.popleft()
            for dependent in sorted(self._dependents.get(current, [])):
                if dependent in impacted:
                    continue
                impacted.add(dependent)
                paths[dependent] = [dependent, *paths[current]]
                queue.append(dependent)

        only_impacted = sorted(impacted - set(failed_nodes))
        critical = [node for node in only_impacted if self.nodes[node].criticality == "critical"]
        return ImpactReport(sorted(failed_nodes), only_impacted, sorted(critical), paths)

    def single_points_of_failure(self) -> dict[str, list[str]]:
        findings: dict[str, list[str]] = {}
        for node_id in sorted(self.nodes):
            critical = self.blast_radius(node_id).critical_impacts
            if critical:
                findings[node_id] = critical
        return findings

    def dependency_chain(self, node_id: str) -> list[str]:
        if node_id not in self.nodes:
            raise KeyError(f"Unknown node: {node_id}")
        result: list[str] = []
        queue = deque(sorted(self._requirements.get(node_id, [])))
        seen: set[str] = set()
        while queue:
            item = queue.popleft()
            if item in seen:
                continue
            seen.add(item)
            result.append(item)
            queue.extend(sorted(self._requirements.get(item, [])))
        return result

    def to_mermaid(self) -> str:
        lines = ["flowchart LR"]
        for node in sorted(self.nodes.values(), key=lambda item: item.id):
            label = (node.label or node.id).replace('"', "'")
            lines.append(f'    {self._safe_id(node.id)}["{label}<br/>{node.kind}"]')
        for edge in sorted(self.dependencies, key=lambda item: (item.source, item.target, item.kind)):
            arrow = "-->" if edge.required else "-.->"
            lines.append(
                f"    {self._safe_id(edge.source)} {arrow}|{edge.kind}| {self._safe_id(edge.target)}"
            )
        return "\n".join(lines) + "\n"

    @staticmethod
    def _safe_id(value: str) -> str:
        return "n_" + "".join(char if char.isalnum() else "_" for char in value)


def build_graph(payload: dict[str, object]) -> InfrastructureGraph:
    return InfrastructureGraph.from_dict(payload)
