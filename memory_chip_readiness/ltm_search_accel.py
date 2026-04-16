"""L02 — LTM Search Accelerator Readiness.

장기 메모리 로직(well/recall/top-k/episodic)을
검색형 메모리 가속기(similarity engine + persistent store interface)로
번역할 준비도.

Graph-rank 확장:
  벡터 유사도 검색 위에 PageRank-style 연상 그래프 재순위 엔진을
  하드웨어로 설계할 준비도를 선택 가중치(0.10)로 반영한다.
  기존 ω 가중치는 0.90으로 정규화되어 총합 1.00을 유지한다.
"""

from __future__ import annotations

from .contracts import LayerResult, LTMSearchAccelProfile

_LAYER = "ltm_search_accel"

# graph_rank 미지원 시 기존 가중치를 그대로 사용하기 위한 정규화 상수
_W_BASE = 0.90   # graph_rank 없을 때 기존 5개 서브스코어 합계 비율
_W_GRAPH = 0.10  # graph_rank 확장 최대 기여


def assess_ltm_search(p: LTMSearchAccelProfile) -> LayerResult:
    """Evaluate LTM search accelerator readiness (0 – 1).

    가중치 구조:
      similarity    0.27  (기존 0.30 × 0.90)
      dim/prec      0.135 (기존 0.15 × 0.90)
      storage       0.18  (기존 0.20 × 0.90)
      latency       0.135 (기존 0.15 × 0.90)
      rtl           0.18  (기존 0.20 × 0.90)
      graph_rank    0.10  (신규, 선택)
      ─────────────────────────────────────
      합계          1.00
    """

    # 1. similarity engine design maturity
    sim_score = 0.0
    valid_engines = {"dot_product", "cosine", "l2", "hamming"}
    if p.similarity_engine_type in valid_engines:
        sim_score += 0.4
    if p.top_k_hw:
        sim_score += 0.3
    if p.cam_lookup_support:
        sim_score += 0.3

    # 2. vector dimensions & precision
    dim_feasible = 1.0 if p.vector_dim <= 512 else max(0.0, 1.0 - (p.vector_dim - 512) / 1024)
    prec_map = {"int8": 1.0, "fp16": 0.9, "bf16": 0.85, "fp32": 0.6}
    prec_score = prec_map.get(p.fixed_point_precision, 0.5)

    # 3. storage & index architecture
    storage_score = 0.0
    if p.external_storage_interface:
        storage_score += 0.4
    if p.episodic_log_engine:
        storage_score += 0.3
    if p.index_cache_kb > 0:
        storage_score += min(0.3, p.index_cache_kb / 256 * 0.3)

    # 4. latency budget
    lat_score = 0.0
    if p.search_latency_target_ns > 0:
        lat_score = 0.5
        if p.search_latency_target_ns <= 100:
            lat_score = 1.0
        elif p.search_latency_target_ns <= 500:
            lat_score = 0.75

    # 5. RTL maturity
    rtl_score = min(1.0, p.rtl_coverage_pct / 100)

    # 6. Graph-rank extension — PageRank-style associative recall readiness
    #    adjacency_store_kb > 0 : 인접 리스트용 온칩 SRAM 설계됨
    #    graph_rank_support     : SpMV 파이프라인 설계됨
    #    rank_propagation_hw    : 수렴 판정 + 랭크 버퍼 HW 구현
    #    graph_search_latency_ns: 랭크 재순위 지연 목표 설정됨
    graph_score = 0.0
    if p.adjacency_store_kb > 0:
        graph_score += 0.25
        graph_score += min(0.15, p.adjacency_store_kb / 512 * 0.15)
    if p.graph_rank_support:
        graph_score += 0.35
    if p.rank_propagation_hw:
        graph_score += 0.20
    if p.graph_search_latency_ns > 0:
        graph_score += 0.05
    graph_score = min(1.0, graph_score)

    # weighted — 기존 5개 서브스코어는 0.90 정규화, graph_rank는 0.10 추가
    base_omega = (
        0.30 * sim_score
        + 0.15 * (dim_feasible * 0.6 + prec_score * 0.4)
        + 0.20 * storage_score
        + 0.15 * lat_score
        + 0.20 * rtl_score
    )
    omega = _W_BASE * base_omega + _W_GRAPH * graph_score
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "similarity_score": round(sim_score, 3),
        "dim_feasible": round(dim_feasible, 3),
        "precision_score": round(prec_score, 3),
        "storage_score": round(storage_score, 3),
        "latency_score": round(lat_score, 3),
        "rtl_score": round(rtl_score, 3),
        "graph_rank_score": round(graph_score, 3),
    }

    notes_parts: list[str] = []
    if sim_score < 0.4:
        notes_parts.append("유사도 엔진 타입 미정의 또는 불분명")
    if not p.external_storage_interface:
        notes_parts.append("외부 persistent storage 인터페이스 미설계")
    if lat_score == 0:
        notes_parts.append("검색 지연 목표 미설정")
    if rtl_score < 0.3:
        notes_parts.append("RTL 커버리지 부족")
    if not p.graph_rank_support:
        notes_parts.append(
            "graph_rank 미설계 — 연상 그래프 재순위 없이 벡터 유사도만으로 recall"
        )

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "LTM 검색 가속기 설계 양호",
    )
