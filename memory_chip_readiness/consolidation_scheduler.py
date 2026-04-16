"""L03 — Consolidation Scheduler Readiness.

STM → LTM 메모리 통합(컨솔리데이션) 로직을
하드웨어 스케줄러(DMA + eligibility FSM + merge arbiter)로
번역할 준비도.

Association-edge 확장:
  consolidation 이벤트 시 함께 통합된 기억들 사이의 연상 엣지를 기록하는
  하드웨어 로그(association_edge_log)를 선택 가중치(0.10)로 반영한다.
  이 엣지 데이터가 L02 graph_rank 엔진의 입력이 된다.
  기존 5개 서브스코어는 0.90으로 정규화해 총합 1.00을 유지한다.
"""

from __future__ import annotations

from .contracts import ConsolidationSchedulerProfile, LayerResult

_LAYER = "consolidation_scheduler"

_W_BASE = 0.90
_W_EDGE = 0.10


def assess_consolidation(p: ConsolidationSchedulerProfile) -> LayerResult:
    """Evaluate consolidation scheduler HW readiness (0 – 1).

    가중치 구조:
      core blocks   0.27  (기존 0.30 × 0.90)
      advanced      0.135 (기존 0.15 × 0.90)
      throughput    0.135 (기존 0.15 × 0.90)
      pipeline      0.135 (기존 0.15 × 0.90)
      rtl           0.225 (기존 0.25 × 0.90)
      assoc_edge    0.10  (신규, 선택)
      ─────────────────────────────────────
      합계          1.00
    """

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

    # 6. Association-edge log — graph-rank 엣지 소스 준비도
    #    association_edge_log   : STM→LTM 통합 시 공동 통합된 기억 쌍을 엣지로 기록
    #    edge_weight_decay_hw   : 엣지 강도 시간 감쇠 하드웨어 처리
    #    max_edges_per_event    : 단일 이벤트당 기록 가능한 최대 엣지 수 (0=미설계)
    edge_score = 0.0
    if p.association_edge_log:
        edge_score += 0.55
    if p.edge_weight_decay_hw:
        edge_score += 0.25
    if p.max_edges_per_event > 0:
        edge_score += min(0.20, p.max_edges_per_event / 8 * 0.20)
    edge_score = min(1.0, edge_score)

    base_omega = (
        0.30 * core_score
        + 0.15 * adv_score
        + 0.15 * throughput_score
        + 0.15 * pipe_score
        + 0.25 * rtl_score
    )
    omega = _W_BASE * base_omega + _W_EDGE * edge_score
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "core_score": round(core_score, 3),
        "advanced_score": round(adv_score, 3),
        "throughput_score": round(throughput_score, 3),
        "pipeline_score": round(pipe_score, 3),
        "rtl_score": round(rtl_score, 3),
        "association_edge_score": round(edge_score, 3),
    }

    notes_parts: list[str] = []
    if core_score < 0.5:
        notes_parts.append("eligibility FSM / DMA / arbiter 핵심 블록 부족")
    if not p.dma_controller:
        notes_parts.append("DMA 컨트롤러 미설계")
    if rtl_score < 0.3:
        notes_parts.append("RTL 커버리지 부족")
    if not p.association_edge_log:
        notes_parts.append(
            "association_edge_log 미설계 — graph_rank 엔진에 공급할 연상 엣지 없음"
        )

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "컨솔리데이션 스케줄러 준비 양호",
    )
