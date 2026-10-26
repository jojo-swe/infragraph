from infragraph import build_graph

PAYLOAD = {
    "nodes": [
        {"id": "core", "kind": "switch"},
        {"id": "dns", "kind": "service", "criticality": "critical"},
        {"id": "app", "kind": "application", "criticality": "critical"},
    ],
    "dependencies": [
        {"source": "dns", "target": "core", "kind": "network"},
        {"source": "app", "target": "dns", "kind": "resolution"},
    ],
}


def test_blast_radius_follows_reverse_dependencies() -> None:
    report = build_graph(PAYLOAD).blast_radius("core")
    assert report.impacted_nodes == ["app", "dns"]
    assert report.critical_impacts == ["app", "dns"]
    assert report.paths["app"] == ["app", "dns", "core"]


def test_dependency_chain_follows_requirements() -> None:
    assert build_graph(PAYLOAD).dependency_chain("app") == ["dns", "core"]


def test_single_points_of_failure() -> None:
    findings = build_graph(PAYLOAD).single_points_of_failure()
    assert findings["core"] == ["app", "dns"]
    assert findings["dns"] == ["app"]


def test_mermaid_is_deterministic() -> None:
    output = build_graph(PAYLOAD).to_mermaid()
    assert output.startswith("flowchart LR\n")
    assert "n_app -->|resolution| n_dns" in output


def test_optional_dependency_does_not_propagate_failure() -> None:
    graph = build_graph(
        {
            "nodes": [{"id": "app"}, {"id": "cache"}, {"id": "db"}],
            "dependencies": [
                {"source": "app", "target": "cache", "required": False},
                {"source": "cache", "target": "db"},
            ],
        }
    )
    assert graph.blast_radius("db").impacted_nodes == ["cache"]
    assert graph.dependency_chain("app") == ["cache", "db"]
