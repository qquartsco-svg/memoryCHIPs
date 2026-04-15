"""L03 — Consolidation Scheduler Readiness.

STM → LTM 메모리 통합(컨솔리데이션) 로직을
하드웨어 스케줄러(DMA + eligibility FSM + merge arbiter)로
번역할 준비도.
"""

from __future__ import annotations

from .contracts import ConsolidationSchedulerProfile, LayerResult

_LAYER = "consolidation_scheduler"


def assess_consolidation(p: ConsolidationSchedulerProfile) -> LayerResult:
    """Evaluate consolidation scheduler HW readiness (0 – 1)."""

    # 1. core blocks defined
    core_items = [
        p.eligibility_fsm,
        p.dma_controller,
        p.strength_threshold_hw,
        p.merge_arbiter,
    ]
    core_score = sum(core_items) / len(core_items)

    # 2. advanced features
    adv_items = [
        p.compression_engine,
        p.interrupt_driven,
        p.power_gating_support,
    ]
    adv_score = sum(adv_items) / len(adv_items)

    # 3. throughput
    throughput_score = min(1.0, p.max_consolidation_per_cycle / 4)

    # 4. pipeline depth
    pipe_score = 0.0
    if p.pipeline_stages >= 1:
        pipe_score = 0.4
    if p.pipeline_stages >= 3:
        pipe_score = 0.7
    if p.pipeline_stages >= 5:
        pipe_score = 1.0

    # 5. RTL maturity
    rtl_score = min(1.0, p.rtl_coverage_pct / 100)

    omega = (
        0.30 * core_score
        + 0.15 * adv_score
        + 0.15 * throughput_score
        + 0.15 * pipe_score
        + 0.25 * rtl_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "core_score": round(core_score, 3),
        "advanced_score": round(adv_score, 3),
        "throughput_score": round(throughput_score, 3),
        "pipeline_score": round(pipe_score, 3),
        "rtl_score": round(rtl_score, 3),
    }

    notes_parts: list[str] = []
    if core_score < 0.5:
        notes_parts.append("eligibility FSM / DMA / arbiter 핵심 블록 부족")
    if not p.dma_controller:
        notes_parts.append("DMA 컨트롤러 미설계")
    if rtl_score < 0.3:
        notes_parts.append("RTL 커버리지 부족")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "컨솔리데이션 스케줄러 준비 양호",
    )
