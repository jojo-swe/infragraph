import json
from pathlib import Path

from infragraph.cli import main

CAMPUS = str(Path(__file__).resolve().parents[1] / "examples" / "campus.json")


def test_impact_exits_1_on_critical_impact(capsys) -> None:
    assert main([CAMPUS, "impact", "core-sw"]) == 1
    assert "Critical impacts: auth, dns, portal" in capsys.readouterr().out


def test_impact_exits_0_without_critical_impact(capsys) -> None:
    assert main([CAMPUS, "impact", "portal"]) == 0
    assert "Impacted (0): none" in capsys.readouterr().out


def test_spof_exits_1_when_findings(capsys) -> None:
    assert main([CAMPUS, "spof"]) == 1
    assert json.loads(capsys.readouterr().out)["core-sw"] == ["auth", "dns", "portal"]


def test_unknown_node_exits_2_with_clean_message(capsys) -> None:
    assert main([CAMPUS, "impact", "nope"]) == 2
    assert capsys.readouterr().err == "infragraph: Unknown node(s): nope\n"


def test_unknown_inventory_field_exits_2(tmp_path, capsys) -> None:
    inventory = tmp_path / "bad.json"
    inventory.write_text(json.dumps({"nodes": [{"id": "a", "bogus": 1}]}), encoding="utf-8")
    assert main([str(inventory), "spof"]) == 2
    err = capsys.readouterr().err
    assert err.startswith("infragraph: ")
    assert "unexpected keyword argument 'bogus'" in err


def test_mermaid_writes_output_file(tmp_path) -> None:
    output = tmp_path / "topology.mmd"
    assert main([CAMPUS, "mermaid", "-o", str(output)]) == 0
    assert output.read_text(encoding="utf-8").startswith("flowchart LR\n")


def test_readme_impact_example_matches_real_output(capsys) -> None:
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")
    expected = readme.split("Example output:\n\n```text\n", 1)[1].split("```", 1)[0]
    main([CAMPUS, "impact", "core-sw"])
    assert capsys.readouterr().out == expected
