"""L08 — Cache Coherency & MMU (GP).

캐시 일관성(MESI/MOESI), TLB, 가상 메모리, MMU 지원 준비도.
범용 메모리가 CPU와 직접 붙으려면 캐시 일관성 프로토콜이 필수다.
"""

from __future__ import annotations

from .contracts import CacheCoherencyProfile, LayerResult

_LAYER = "cache_coherency"

_PROTOCOL_MATURITY: dict[str, float] = {
    "mesi": 1.0,
    "moesi": 0.95,
    "mesif": 0.90,
    "amba_ace": 0.85,
    "chi": 0.80,
    "none": 0.0,
}


def assess_cache_coherency(p: CacheCoherencyProfile) -> LayerResult:
    """Evaluate cache coherency & MMU readiness (0 – 1)."""

    # 1. coherency protocol
    proto_score = _PROTOCOL_MATURITY.get(p.coherency_protocol.lower(), 0.3)
    if p.snoop_filter:
        proto_score = min(1.0, proto_score + 0.1)

    # 2. MMU / virtual memory
    mmu_score = 0.0
    if p.tlb_entries > 0:
        mmu_score += min(0.3, p.tlb_entries / 256 * 0.3)
    if p.virtual_address_bits >= 32:
        mmu_score += 0.2
    if p.virtual_address_bits >= 48:
        mmu_score += 0.2
    if p.mmu_hw_walker:
        mmu_score += 0.3
    mmu_score = min(1.0, mmu_score)

    # 3. cache architecture
    cache_score = 0.0
    if p.cache_line_bytes >= 64:
        cache_score += 0.4
    if p.multi_level_cache:
        cache_score += 0.3
    if p.atomic_ops_support:
        cache_score += 0.3

    # 4. RTL maturity
    rtl_score = min(1.0, p.rtl_coverage_pct / 100)

    omega = (
        0.30 * proto_score
        + 0.30 * mmu_score
        + 0.15 * cache_score
        + 0.25 * rtl_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "coherency_protocol": p.coherency_protocol,
        "protocol_score": round(proto_score, 3),
        "mmu_score": round(mmu_score, 3),
        "cache_score": round(cache_score, 3),
        "rtl_score": round(rtl_score, 3),
    }

    notes_parts: list[str] = []
    if p.coherency_protocol.lower() == "none":
        notes_parts.append("캐시 일관성 프로토콜 미정의")
    if p.tlb_entries == 0:
        notes_parts.append("TLB 미설계")
    if not p.mmu_hw_walker:
        notes_parts.append("MMU HW 워커 미구현")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "캐시 일관성·MMU 준비 양호",
    )
