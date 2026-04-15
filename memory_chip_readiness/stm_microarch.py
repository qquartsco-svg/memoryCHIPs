"""L01 — STM Microarchitecture Readiness.

단기 메모리 로직(슬롯/감쇠/TTL/축출/쿼리)을
하드웨어 블록(SRAM + FSM + 우선순위 큐)으로 번역할 준비도.
"""

from __future__ import annotations

from .contracts import LayerResult, STMMicroarchProfile

_LAYER = "stm_microarch"


def assess_stm_microarch(p: STMMicroarchProfile) -> LayerResult:
    """Evaluate STM microarchitecture readiness (0 – 1)."""

    # ── sub-scores ──────────────────────────────────────────────
    # 1. slot capacity feasibility (SRAM area proxy)
    total_bits = p.max_slots * p.slot_width_bits
    capacity_ok = 1.0 if total_bits <= 2 * 1024 * 1024 else max(0.0, 1.0 - (total_bits - 2_097_152) / 8_388_608)

    # 2. control logic completeness
    ctrl_items = [
        p.eviction_policy_defined,
        p.decay_engine_fsm,
        p.ttl_timer_hw,
        p.query_filter_block,
        p.namespace_support,
        p.priority_queue_hw,
    ]
    ctrl_score = sum(ctrl_items) / len(ctrl_items)

    # 3. strength precision (8-bit minimum for useful decay)
    prec_score = min(1.0, p.strength_bits / 8)

    # 4. cycle budget defined
    cycle_score = 0.0
    if p.cycle_budget_put > 0 and p.cycle_budget_get > 0:
        cycle_score = 0.5
        if p.cycle_budget_put <= 4 and p.cycle_budget_get <= 4:
            cycle_score = 1.0
        elif p.cycle_budget_put <= 10 and p.cycle_budget_get <= 10:
            cycle_score = 0.75

    # 5. validation maturity
    val_score = 0.0
    if p.sram_compiler_validated:
        val_score += 0.5
    val_score += min(0.5, p.rtl_coverage_pct / 100 * 0.5)

    # ── weighted combination ────────────────────────────────────
    omega = (
        0.15 * capacity_ok
        + 0.30 * ctrl_score
        + 0.10 * prec_score
        + 0.20 * cycle_score
        + 0.25 * val_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "capacity_bits": total_bits,
        "capacity_ok": round(capacity_ok, 3),
        "ctrl_score": round(ctrl_score, 3),
        "precision_score": round(prec_score, 3),
        "cycle_score": round(cycle_score, 3),
        "validation_score": round(val_score, 3),
    }

    notes_parts: list[str] = []
    if ctrl_score < 0.5:
        notes_parts.append("eviction/decay/TTL HW 블록 정의 부족")
    if cycle_score == 0:
        notes_parts.append("put/get 사이클 버짓 미정의")
    if val_score < 0.25:
        notes_parts.append("RTL 검증 또는 SRAM 컴파일러 미확보")

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "STM 마이크로아키텍처 준비 양호",
    )
