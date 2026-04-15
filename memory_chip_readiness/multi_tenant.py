"""L09 — Multi-Tenant & Scalability (GP).

다중 프로세스 격리, QoS, 용량 확장, 다이 스태킹, 대역폭 분할 등
범용 메모리 시스템의 확장성 준비도.
"""

from __future__ import annotations

from .contracts import LayerResult, MultiTenantProfile

_LAYER = "multi_tenant"


def assess_multi_tenant(p: MultiTenantProfile) -> LayerResult:
    """Evaluate multi-tenant & scalability readiness (0 – 1)."""

    # 1. isolation & protection
    iso_items = [
        p.memory_protection_unit,
        p.process_isolation_hw,
        p.error_containment,
    ]
    iso_score = sum(iso_items) / len(iso_items)

    # 2. tenant capacity & QoS
    tenant_score = min(1.0, p.max_tenants / 16)
    qos_score = 1.0 if p.qos_arbiter else 0.0
    bw_score = 1.0 if p.bandwidth_partitioning else 0.0
    mgmt_score = 0.4 * tenant_score + 0.3 * qos_score + 0.3 * bw_score

    # 3. scalability
    scale_items = [
        p.capacity_scalable,
        p.die_stacking_support,
        p.channel_bonding,
    ]
    scale_score = sum(scale_items) / len(scale_items)

    # 4. RTL maturity
    rtl_score = min(1.0, p.rtl_coverage_pct / 100)

    omega = (
        0.30 * iso_score
        + 0.25 * mgmt_score
        + 0.20 * scale_score
        + 0.25 * rtl_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "isolation_score": round(iso_score, 3),
        "management_score": round(mgmt_score, 3),
        "scalability_score": round(scale_score, 3),
        "rtl_score": round(rtl_score, 3),
        "max_tenants": p.max_tenants,
    }

    notes_parts: list[str] = []
    if not p.memory_protection_unit:
        notes_parts.append("메모리 보호 유닛 미설계")
    if not p.process_isolation_hw:
        notes_parts.append("프로세스 격리 HW 없음")
    if not p.qos_arbiter:
        notes_parts.append("QoS 아비터 미구현")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "다중 테넌트·확장성 준비 양호",
    )
