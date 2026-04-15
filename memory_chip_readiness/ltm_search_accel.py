"""L02 — LTM Search Accelerator Readiness.

장기 메모리 로직(well/recall/top-k/episodic)을
검색형 메모리 가속기(similarity engine + persistent store interface)로
번역할 준비도.
"""

from __future__ import annotations

from .contracts import LayerResult, LTMSearchAccelProfile

_LAYER = "ltm_search_accel"


def assess_ltm_search(p: LTMSearchAccelProfile) -> LayerResult:
    """Evaluate LTM search accelerator readiness (0 – 1)."""

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

    # weighted
    omega = (
        0.30 * sim_score
        + 0.15 * (dim_feasible * 0.6 + prec_score * 0.4)
        + 0.20 * storage_score
        + 0.15 * lat_score
        + 0.20 * rtl_score
    )
    omega = max(0.0, min(1.0, omega))

    evidence = {
        "similarity_score": round(sim_score, 3),
        "dim_feasible": round(dim_feasible, 3),
        "precision_score": round(prec_score, 3),
        "storage_score": round(storage_score, 3),
        "latency_score": round(lat_score, 3),
        "rtl_score": round(rtl_score, 3),
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

    return LayerResult(
        layer=_LAYER,
        omega=omega,
        evidence=evidence,
        notes="; ".join(notes_parts) if notes_parts else "LTM 검색 가속기 설계 양호",
    )
