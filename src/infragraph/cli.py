"""Command-line interface for InfraGraph."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import build_graph


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="infragraph", description="Analyze infrastructure dependencies.")
    parser.add_argument("inventory", type=Path, help="JSON inventory file")
    sub = parser.add_subparsers(dest="command", required=True)

    impact = sub.add_parser("impact", help="Calculate blast radius")
    impact.add_argument("nodes", nargs="+", help="Failed node IDs")
    impact.add_argument("--json", action="store_true")

    chain = sub.add_parser("chain", help="Show dependencies required by a node")
    chain.add_argument("node")

    sub.add_parser("spof", help="Find nodes whose failure impacts critical services")

    mermaid = sub.add_parser("mermaid", help="Export Mermaid topology")
    mermaid.add_argument("--output", "-o", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(args.inventory.read_text(encoding="utf-8"))
        graph = build_graph(payload)
        if args.command == "impact":
            report = graph.blast_radius(args.nodes)
            if args.json:
                print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
            else:
                print(f"Failed: {', '.join(report.failed_nodes)}")
                print(f"Impacted ({len(report.impacted_nodes)}): {', '.join(report.impacted_nodes) or 'none'}")
                print(f"Critical impacts: {', '.join(report.critical_impacts) or 'none'}")
                for node in report.impacted_nodes:
                    print(f"  {node}: {' -> '.join(report.paths[node])}")
            return 1 if report.critical_impacts else 0
        if args.command == "chain":
            print("\n".join(graph.dependency_chain(args.node)))
            return 0
        if args.command == "spof":
            findings = graph.single_points_of_failure()
            print(json.dumps(findings, indent=2, sort_keys=True))
            return 1 if findings else 0
        output = graph.to_mermaid()
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"infragraph: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
