"""L07 — Standard Memory Interface Compliance (GP).

DDR5/LPDDR5/HBM3/CXL 등 표준 메모리 인터페이스 호환 준비도.
범용 메모리로 포지셔닝하려면 JEDEC 표준 준수가 필수다.
"""

from __future__ import annotations

from .contracts import LayerResult, MemoryStandard, StandardInterfaceProfile

_LAYER = "standard_interface"

_STANDARD_MATURITY: dict[MemoryStandard, float] = {
    MemoryStandard.ddr4: 1.0,
    MemoryStandard.ddr5: 0.90,
    MemoryStandard.lpddr5: 0.85,
    MemoryStandard.hbm2e: 0.80,
    MemoryStandard.hbm3: 0.70,
    MemoryStandard.cxl_mem: 0.60,
    MemoryStandard.none: 0.0,
}


def assess_standard_interface(p: StandardInterfaceProfile) -> LayerResult:
    """Evaluate standard memory interface compliance (0 – 1)."""

    # 1. standard selection & JEDEC compliance
    std_mat = _STANDARD_MATURITY.get(p.memory_standard, 0.0)
    jedec = min(1.0, p.jedec_compliance_level)
    std_score = 0.5 * std_mat + 0.5 * jedec

    # 2. PHY & signal integrity
    phy_score = 0.0
    if p.phy_ip_validated:
        phy_score += 0.4
    if p.signal_integrity_sim:
        phy_score += 0.3
    if p.timing_margin_pct > 0:
        phy_score += min(0.3, p.timing_margin_pct / 20 * 0.3)

    # 3. channel & data rate
    ch_score = min(1.0, p.channel_count / 8)
    rate_score = min(1.0, p.data_rate_mtps / 8400) if p.data_rate_mtps > 0 else 0.0
    perf_score = 0.5 * ch_score + 0.5 * rate_score

    # 4. protocol features
    feat_items = [p.init_sequence_defined, p.refresh_logic]
    feat_score = sum(feat_items) / len(feat_items)

    # 5. RTL maturity
    rtl_score = min(1.0, p.rtl_coverage_pct / 100)

    omega = (
        0.25 * std_score
        + 0.25 * phy_score
        + 0.15 * perf_score
        + 0.15 * feat_score
        + 0.20 * rtl_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "memory_standard": p.memory_standard.value,
        "standard_score": round(std_score, 3),
        "phy_score": round(phy_score, 3),
        "performance_score": round(perf_score, 3),
        "feature_score": round(feat_score, 3),
        "rtl_score": round(rtl_score, 3),
    }

    notes_parts: list[str] = []
    if p.memory_standard == MemoryStandard.none:
        notes_parts.append("표준 메모리 인터페이스 미선택")
    if not p.phy_ip_validated:
        notes_parts.append("PHY IP 미검증")
    if jedec < 0.5:
        notes_parts.append("JEDEC 준수 수준 부족")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "표준 인터페이스 준비 양호",
    )
