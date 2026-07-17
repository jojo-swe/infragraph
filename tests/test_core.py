from infragraph import build_graph

def test_graph_deduplicates_neighbors() -> None:
    assert build_graph([{"name":"edge-a","neighbors":["core-b","core-b"]}]) == {"edge-a":["core-b"]}
