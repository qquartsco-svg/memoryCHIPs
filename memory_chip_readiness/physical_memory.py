"""L04 — Physical Memory Layer Mapping.

SRAM / Flash / HBM / MRAM 등 물리 메모리 기술 선택과
STM/LTM 계층 매핑 준비도.
"""

from __future__ import annotations

from .contracts import LayerResult, MemoryTech, PhysicalMemoryProfile

_LAYER = "physical_memory"

_TECH_MATURITY: dict[MemoryTech, float] = {
    MemoryTech.sram: 1.0,
    MemoryTech.dram: 0.95,
    MemoryTech.edram: 0.80,
    MemoryTech.hbm: 0.85,
    MemoryTech.mram: 0.65,
    MemoryTech.nand_flash: 0.70,
    MemoryTech.reram: 0.45,
}


def assess_physical_memory(p: PhysicalMemoryProfile) -> LayerResult:
    """Evaluate physical memory layer mapping readiness (0 – 1)."""

    # 1. technology maturity
    stm_mat = _TECH_MATURITY.get(p.stm_tech, 0.5)
    ltm_mat = _TECH_MATURITY.get(p.ltm_tech, 0.5)
    tech_score = 0.6 * stm_mat + 0.4 * ltm_mat

    # Penalty: if no capacity is provisioned AND technology is not validated,
    # the tech maturity score represents an unselected placeholder, not a real design.
    if p.stm_capacity_kb == 0 and p.ltm_capacity_mb == 0 and not p.tech_validated:
        tech_score *= 0.25

    # 2. capacity provisioned
    cap_score = 0.0
    if p.stm_capacity_kb > 0:
        cap_score += 0.5
    if p.ltm_capacity_mb > 0:
        cap_score += 0.5

    # 3. reliability features
    rel_items = [
        p.ecc_support,
        p.wear_leveling,
        p.thermal_guard,
        p.memory_bist,
    ]
    rel_score = sum(rel_items) / len(rel_items)

    # 4. endurance & retention
    dur_score = 0.0
    if p.retention_hours >= 24:
        dur_score += 0.3
    if p.retention_hours >= 8760:
        dur_score += 0.2
    if p.endurance_cycles >= 10_000:
        dur_score += 0.3
    if p.endurance_cycles >= 1_000_000:
        dur_score += 0.2
    dur_score = min(1.0, dur_score)

    # 5. technology validated
    val_score = 1.0 if p.tech_validated else 0.0

    omega = (
        0.25 * tech_score
        + 0.15 * cap_score
        + 0.20 * rel_score
        + 0.20 * dur_score
        + 0.20 * val_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "stm_tech": p.stm_tech.value,
        "ltm_tech": p.ltm_tech.value,
        "tech_maturity_score": round(tech_score, 3),
        "capacity_score": round(cap_score, 3),
        "reliability_score": round(rel_score, 3),
        "durability_score": round(dur_score, 3),
        "validated": p.tech_validated,
    }

    notes_parts: list[str] = []
    if cap_score < 0.5:
        notes_parts.append("STM 또는 LTM 용량 미산정")
    if rel_score < 0.5:
        notes_parts.append("ECC/wear-leveling/thermal/BIST 부족")
    if not p.tech_validated:
        notes_parts.append("물리 메모리 기술 미검증")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "물리 메모리 계층 준비 양호",
    )
