"""Memory Chip Readiness Foundation — CLI entry-point.

Usage:
    memory-chip-readiness list-presets
    memory-chip-readiness analyze <preset> [--json] [--edge]
    memory-chip-readiness gate-test <preset> [overrides...] [--json] [--edge]
"""

from __future__ import annotations

import argparse
import json as _json
import sys

from .version import __version__


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="memory-chip-readiness",
        description=(
            "Memory Chip Readiness Foundation — "
            "STM/LTM → Silicon 준비도 스크리닝 (accelerator / general_purpose / hybrid)"
        ),
    )
    p.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    sub = p.add_subparsers(dest="command")

    sub.add_parser("list-presets", help="등록된 프리셋 목록 출력")

    ap = sub.add_parser("analyze", help="프리셋으로 분석 실행")
    ap.add_argument("preset", type=str)
    ap.add_argument("--json", action="store_true", help="JSON 출력")
    ap.add_argument("--edge", action="store_true", help="Edge AI flat signal 출력")

    gp = sub.add_parser("gate-test", help="프리셋 + 오버라이드로 게이트 테스트")
    gp.add_argument("preset", type=str)
    gp.add_argument("--tier", type=str, default=None, choices=["accelerator", "general_purpose", "hybrid"])
    gp.add_argument("--max-slots", type=int, default=None)
    gp.add_argument("--vector-dim", type=int, default=None)
    gp.add_argument("--process-node", type=str, default=None)
    gp.add_argument("--rtl-coverage", type=float, default=None)
    gp.add_argument("--json", action="store_true")
    gp.add_argument("--edge", action="store_true")

    return p


def _print_report(rpt: object, *, as_json: bool, as_edge: bool) -> None:
    from .contracts import MemoryChipReadinessReport

    assert isinstance(rpt, MemoryChipReadinessReport)

    if as_edge:
        print(_json.dumps(rpt.to_edge_signal(), indent=2, ensure_ascii=False))
        return
    if as_json:
        print(_json.dumps(rpt.to_summary_dict(), indent=2, ensure_ascii=False))
        return

    tier_label = rpt.design_tier.value.upper()
    print(f"Tier    = {tier_label}")
    print(f"Ω_chip  = {rpt.omega_chip:.4f}")
    print(f"Verdict = {rpt.verdict.value}")
    print(f"Bottleneck = {rpt.key_bottleneck}")
    print()
    for lr in rpt.layer_details:
        print(f"  [{lr.layer:30s}]  Ω = {lr.omega:.4f}  {lr.notes}")
    print()
    gate = rpt.fabrication_gate
    status = "PASS" if gate.ready_for_tapeout else "BLOCKED"
    print(f"Fabrication Gate: {status}  (est. {gate.estimated_tapeout_months} months)")
    if gate.blockers:
        print(f"  Blockers: {', '.join(gate.blockers)}")
    print()
    b = rpt.chip_bridge
    print(
        f"Bridge → NPU={b.npu_omega_hint:.3f}  HBM={b.hbm_omega_hint:.3f}  "
        f"HBF={b.hbf_omega_hint:.3f}  foundry={b.foundry_gate_status}"
    )


def cli_main(argv: list[str] | None = None) -> None:
    """CLI entry."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "list-presets":
        from .presets import list_presets

        for name in list_presets():
            print(name)
        return

    from .presets import _REGISTRY, analyze_preset

    if args.command == "analyze":
        rpt = analyze_preset(args.preset)
        _print_report(rpt, as_json=args.json, as_edge=args.edge)
        return

    if args.command == "gate-test":
        if args.preset not in _REGISTRY:
            print(f"Unknown preset: {args.preset}", file=sys.stderr)
            sys.exit(1)

        kwargs = dict(_REGISTRY[args.preset])

        if args.tier is not None:
            from .contracts import DesignTier

            kwargs["tier"] = DesignTier(args.tier)

        if args.max_slots is not None:
            from .contracts import STMMicroarchProfile

            stm = kwargs.get("stm") or STMMicroarchProfile()
            kwargs["stm"] = STMMicroarchProfile(
                **{**stm.__dict__, "max_slots": args.max_slots}
            )

        if args.vector_dim is not None:
            from .contracts import LTMSearchAccelProfile

            ltm = kwargs.get("ltm") or LTMSearchAccelProfile()
            kwargs["ltm"] = LTMSearchAccelProfile(
                **{**ltm.__dict__, "vector_dim": args.vector_dim}
            )

        if args.process_node is not None:
            from .contracts import ProcessAreaPowerProfile, ProcessNode

            proc = kwargs.get("process") or ProcessAreaPowerProfile()
            try:
                node = ProcessNode(args.process_node)
            except ValueError:
                node_names = [n.value for n in ProcessNode]
                print(f"Invalid node. Choose from: {node_names}", file=sys.stderr)
                sys.exit(1)
            kwargs["process"] = ProcessAreaPowerProfile(
                **{**proc.__dict__, "process_node": node}
            )

        if args.rtl_coverage is not None:
            from .contracts import STMMicroarchProfile

            stm = kwargs.get("stm") or STMMicroarchProfile()
            kwargs["stm"] = STMMicroarchProfile(
                **{**stm.__dict__, "rtl_coverage_pct": args.rtl_coverage}
            )

        from .foundation import analyze

        rpt = analyze(**kwargs)
        _print_report(rpt, as_json=args.json, as_edge=args.edge)


if __name__ == "__main__":
    cli_main()
