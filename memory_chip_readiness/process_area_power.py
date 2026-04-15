"""L06 — Process, Area, Power & Test Feasibility.

공정 노드·면적·전력·DFT·signoff 등
실리콘 구현 타당성 종합 평가.
"""

from __future__ import annotations

from .contracts import LayerResult, ProcessAreaPowerProfile, ProcessNode

_LAYER = "process_area_power"

_NODE_MATURITY: dict[ProcessNode, float] = {
    ProcessNode.nm180: 1.00,
    ProcessNode.nm65: 0.98,
    ProcessNode.nm28: 0.95,
    ProcessNode.nm14: 0.88,
    ProcessNode.nm7: 0.80,
    ProcessNode.nm5: 0.70,
    ProcessNode.nm3: 0.55,
}


def assess_process_area_power(p: ProcessAreaPowerProfile) -> LayerResult:
    """Evaluate process / area / power / test feasibility (0 – 1)."""

    # 1. process node maturity
    node_score = _NODE_MATURITY.get(p.process_node, 0.5)

    # 2. area feasibility
    area_score = 0.0
    if p.target_area_mm2 > 0 and p.estimated_area_mm2 > 0:
        ratio = p.estimated_area_mm2 / p.target_area_mm2
        if ratio <= 1.0:
            area_score = 1.0
        elif ratio <= 1.3:
            area_score = 0.7
        elif ratio <= 1.6:
            area_score = 0.4
        else:
            area_score = 0.1

    # 3. power feasibility
    power_score = 0.0
    if p.target_power_mw > 0 and p.estimated_power_mw > 0:
        ratio = p.estimated_power_mw / p.target_power_mw
        if ratio <= 1.0:
            power_score = 1.0
        elif ratio <= 1.3:
            power_score = 0.7
        elif ratio <= 1.5:
            power_score = 0.4
        else:
            power_score = 0.1

    # 4. DFT & signoff
    dft_items = [
        p.dft_scan_chain,
        p.dft_mbist,
        p.signoff_drc_clean,
        p.signoff_lvs_clean,
    ]
    dft_score = sum(dft_items) / len(dft_items)

    # 5. foundry & yield
    foundry_score = 0.0
    if p.foundry_pdk_available:
        foundry_score += 0.5
    if p.yield_estimate_pct > 0:
        foundry_score += min(0.5, p.yield_estimate_pct / 100 * 0.5)

    omega = (
        0.15 * node_score
        + 0.20 * area_score
        + 0.20 * power_score
        + 0.25 * dft_score
        + 0.20 * foundry_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "process_node": p.process_node.value,
        "node_maturity": round(node_score, 3),
        "area_score": round(area_score, 3),
        "power_score": round(power_score, 3),
        "dft_score": round(dft_score, 3),
        "foundry_score": round(foundry_score, 3),
        "clock_mhz": p.clock_freq_mhz,
        "package": p.package_type,
    }

    notes_parts: list[str] = []
    if area_score == 0:
        notes_parts.append("면적 목표/추정 미설정")
    if power_score == 0:
        notes_parts.append("전력 목표/추정 미설정")
    if dft_score < 0.5:
        notes_parts.append("DFT/Signoff 미충족 항목 있음")
    if not p.foundry_pdk_available:
        notes_parts.append("파운드리 PDK 미확보")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "공정·면적·전력 타당성 양호",
    )
