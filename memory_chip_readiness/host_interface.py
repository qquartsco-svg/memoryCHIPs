"""L05 — Host Interface, DMA & Bus Design.

메모리 가속기 칩이 Host CPU/NPU와 데이터를 교환하기 위한
버스·DMA·레지스터맵·드라이버 준비도.
"""

from __future__ import annotations

from .contracts import HostInterfaceProfile, LayerResult

_LAYER = "host_interface"


def assess_host_interface(p: HostInterfaceProfile) -> LayerResult:
    """Evaluate host interface & DMA design readiness (0 – 1)."""

    # 1. bus specification maturity
    bus_score = 0.0
    if p.register_map_defined:
        bus_score += 0.35
    if p.driver_api_spec:
        bus_score += 0.35
    if p.protocol_compliance_tested:
        bus_score += 0.30

    # 2. bandwidth adequacy
    bw_score = 0.0
    if p.bandwidth_gbps > 0:
        bw_score = min(1.0, p.bandwidth_gbps / 10.0)

    # 3. DMA & interrupt
    dma_score = min(1.0, p.dma_channels / 4)
    int_score = min(1.0, p.interrupt_lines / 4)
    infra_score = 0.5 * dma_score + 0.5 * int_score

    # 4. latency target
    lat_score = 0.0
    if p.latency_target_ns > 0:
        lat_score = 0.5
        if p.latency_target_ns <= 50:
            lat_score = 1.0
        elif p.latency_target_ns <= 200:
            lat_score = 0.75

    # 5. firmware readiness
    fw_score = 1.0 if p.firmware_hal_ready else 0.0

    omega = (
        0.30 * bus_score
        + 0.15 * bw_score
        + 0.20 * infra_score
        + 0.15 * lat_score
        + 0.20 * fw_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "bus_protocol": p.bus_protocol.value,
        "bus_score": round(bus_score, 3),
        "bandwidth_score": round(bw_score, 3),
        "infra_score": round(infra_score, 3),
        "latency_score": round(lat_score, 3),
        "firmware_score": round(fw_score, 3),
    }

    notes_parts: list[str] = []
    if not p.register_map_defined:
        notes_parts.append("레지스터 맵 미정의")
    if not p.driver_api_spec:
        notes_parts.append("드라이버 API 스펙 미작성")
    if p.bandwidth_gbps == 0:
        notes_parts.append("대역폭 목표 미설정")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "호스트 인터페이스 설계 양호",
    )
