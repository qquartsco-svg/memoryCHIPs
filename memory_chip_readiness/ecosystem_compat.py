"""L10 — OS & Ecosystem Compatibility (GP).

커널 드라이버, OS 지원, 메모리 할당자 호환, NUMA, RAS 등
범용 메모리가 실제 소프트웨어 생태계에서 쓰이기 위한 준비도.
"""

from __future__ import annotations

from .contracts import EcosystemCompatProfile, LayerResult

_LAYER = "ecosystem_compat"


def assess_ecosystem_compat(p: EcosystemCompatProfile) -> LayerResult:
    """Evaluate OS & ecosystem compatibility readiness (0 – 1)."""

    # 1. OS support
    os_items = [p.kernel_driver_available, p.linux_support, p.rtos_support]
    os_score = sum(os_items) / len(os_items)

    # 2. memory subsystem integration
    mem_items = [
        p.memory_allocator_compat,
        p.numa_aware,
        p.hotplug_support,
    ]
    mem_score = sum(mem_items) / len(mem_items)

    # 3. reliability & monitoring
    ras_items = [p.ras_features, p.monitoring_counters]
    ras_score = sum(ras_items) / len(ras_items)

    # 4. developer ecosystem
    dev_items = [p.documentation_complete, p.sdk_available]
    dev_score = sum(dev_items) / len(dev_items)

    omega = (
        0.30 * os_score
        + 0.25 * mem_score
        + 0.20 * ras_score
        + 0.25 * dev_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "os_score": round(os_score, 3),
        "memory_integration_score": round(mem_score, 3),
        "ras_score": round(ras_score, 3),
        "developer_score": round(dev_score, 3),
    }

    notes_parts: list[str] = []
    if not p.kernel_driver_available:
        notes_parts.append("커널 드라이버 미개발")
    if not p.linux_support:
        notes_parts.append("Linux 지원 없음")
    if not p.documentation_complete:
        notes_parts.append("문서화 미완료")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "OS·생태계 호환 준비 양호",
    )
