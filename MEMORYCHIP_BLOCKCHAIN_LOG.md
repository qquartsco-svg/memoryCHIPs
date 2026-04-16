# Memory Chip Readiness — Blockchain Log

## Block #5 — v0.3.1 (Graph-Rank + Association-Edge Extension)

- **Date**: 2026-04-16
- **Author**: GNJz / 00_BRAIN
- **Version**: memory-chip-readiness 0.3.1
- **Previous Block**: Block #4 (v0.3.0 DesignPhase + Reality Presets)

### 핵심 개선 사항

#### L02 — `LTMSearchAccelProfile` : graph-rank (PageRank-style) 확장

기존 벡터 유사도(cosine / dot_product / L2 / Hamming) 위에 **연상 그래프 재순위 엔진**을 설계 방향으로 기록할 수 있는 파라미터 4종을 추가했다.

| 파라미터 | 의미 |
|----------|------|
| `graph_rank_support` | SpMV(희소 행렬×벡터) PageRank 파이프라인 HW 설계 여부 |
| `adjacency_store_kb` | 연상 엣지(인접 리스트) 온칩 SRAM KB |
| `rank_propagation_hw` | 수렴 판정 + 랭크 벡터 버퍼 HW 구현 여부 |
| `graph_search_latency_ns` | 그래프 재순위 1회 지연 목표 (ns) |

ω 가중치: 기존 5개 서브스코어를 ×0.90 정규화 + graph_rank 최대 +0.10 → 총합 1.00 유지.

#### L03 — `ConsolidationSchedulerProfile` : association-edge (연상 엣지 소스) 확장

STM→LTM 통합(consolidation) 이벤트 시 **함께 통합된 기억 쌍을 연상 엣지로 기록**하는 HW 로그 파라미터 3종 추가.  
이 엣지 데이터가 L02 graph_rank 엔진의 직접 입력 소스가 된다.

| 파라미터 | 의미 |
|----------|------|
| `association_edge_log` | consolidation 이벤트 시 공동 통합 기억 쌍 → 엣지 HW 기록 버퍼 |
| `edge_weight_decay_hw` | 엣지 강도 시간 감쇠 HW 처리 |
| `max_edges_per_event` | 단일 이벤트당 기록 최대 엣지 수 |

ω 가중치: 기존 5개 서브스코어 ×0.90 + association_edge 최대 +0.10 → 총합 1.00 유지.

#### 설계 흐름 연결

```
ConsolidationSchedulerProfile.association_edge_log  (L03)
        │  STM→LTM 통합 시 공동 활성화 기억 쌍 → 엣지 기록
        ▼
LTMSearchAccelProfile.graph_rank_support            (L02)
        │  벡터 유사도 top-k 후보 → SpMV 재순위
        ▼
최종 recall: "유사도" + "연상 구조에서 자주 연결된 기억" 가중 합산
```

#### 프리셋 업데이트 (graph_rank 파라미터 반영)

| 프리셋 | LTM graph_rank | consolidation edge_log |
|--------|---------------|------------------------|
| `Robot_Memory_SoC` | ✓ (adjacency 256KB, propagation HW) | ✓ (edge_decay, max 8) |
| `EdgeAI_Memory_Coprocessor` | ✓ (adjacency 64KB) | ✓ (max 4) |
| `Brain_Spec_Target` | ✓ (adjacency 128KB, concept 방향) | ✓ (max 4) |

#### 테스트

- `TestGraphRankExtension` 신규 8케이스 추가
- 기존 CLI 테스트 `_CWD` 하드코딩 경로 버그 수정 (동적 Path 계산으로 대체)
- **89/89 passing**

### Integrity

- `pytest`: **89 passed**
- `ruff`: All checks passed
- `SIGNATURE.sha256`: **22개 파일** 재서명 완료
- push: `origin/main` `13f54b4`

---

## Block #4 — v0.3.0 (DesignPhase + Reality Presets)

- **Date**: 2026-04-16
- **Author**: GNJz / 00_BRAIN
- **Version**: memory-chip-readiness 0.3.0
- **Previous Block**: Block #3 (v0.2.0 최종 공개 점검)

### 핵심 개선 사항

- **DesignPhase 도입**: `concept / specification / prototype / rtl_complete / production` 5단계 enum.  
  `omega_chip`(이상값)과 `omega_context`(phase × 현실 보정값)를 분리하여 "시뮬레이션 점수 ≠ 실제 구현 완성도" 혼동 해소.
- **omega_context**: `omega_chip × phase_realism` 계산. concept(×0.30)~production(×1.00).
- **gap_to_tapeout**: `max(0, 0.85 − omega_chip)` — tapeout_ready 임계까지 남은 이상값 거리.
- **phase_note**: 단계별 설명 문자열. `to_summary_dict()` / `to_edge_signal()`에 포함.
- **Reality 프리셋 2종 추가**:
  - `Brain_Current_State` (concept): 실제 00_BRAIN 현재 상태. Ω=0.170, ctx=0.051.
  - `Brain_Spec_Target` (specification): 마이크로아키텍처 명세 완성 목표. Ω=0.387, ctx=0.201.
- **테스트 수**: 63 → 80개 (TestDesignPhase 10개 + TestRealityPresets 7개 추가)
- **SIGNATURE.sha256**: 재서명 완료

### Integrity

- `pytest`: 80 passed
- `ruff`: All checks passed
- `SIGNATURE.sha256`: 재서명 완료

---

## Block #3 — v0.2.0 (최종 공개 점검)

- **Date**: 2026-04-15
- **Author**: GNJz / 00_BRAIN
- **Version**: memory-chip-readiness 0.2.0 (공개 전 최종 검증)
- **Previous Block**: Block #2 (v0.2.0 초기 릴리스)

### 최종 점검 수정 사항

- **[P1] L04 물리 메모리 미설계 페널티**: `physical_memory.py`에 `stm_capacity_kb=0 AND ltm_capacity_mb=0 AND tech_validated=False` 조건일 때 `tech_score *= 0.25` 페널티 추가. 기본 프로파일(아무것도 입력 안 한 상태)이 SRAM 기본값 성숙도(1.0)로 인해 실제 설계 없이 0.15 이상 받던 문제 수정.
- **[P2] GP 게이트 다운그레이드 테스트**: `TestFoundationGP.test_gp_gate_downgrade_when_std_missing` 추가. 코어 레이어가 고성능이더라도 `standard_interface` / `cache_coherency` 미정의 시 GP 티어는 반드시 gate 블록됨을 검증.
- **[P3] 가중치 합 불변식 테스트**: `TestWeightIntegrity` 클래스 신설. ACCEL / GP / HYB 3종 가중치 합이 정확히 1.0임을 pytest로 단언. 가중치 키 집합 및 양수 조건도 함께 검증.
- **README 정확도**: 버전 배지 0.1.0 → 0.2.0, 프리셋 표 5종 → 8종으로 확장, `Robot_Memory_SoC` best-case 주석 추가, 패키지 구조 10레이어 반영.
- **테스트 수**: 58 → 63개 (5개 추가)
- **SIGNATURE.sha256**: 22개 파일 재서명 완료

### Integrity

- `pytest`: 63 passed
- `ruff`: All checks passed
- `SIGNATURE.sha256`: 22 files verified

---

## Block #2 — v0.2.0

- **Date**: 2026-04-15
- **Author**: GNJz / 00_BRAIN
- **Version**: memory-chip-readiness 0.2.0
- **Previous Block**: Block #1 (v0.1.0)

### Changes

- DesignTier 도입 (accelerator / general_purpose / hybrid)
- GP Extension 4개 레이어 추가:
  - L07 Standard Memory Interface (standard_interface.py)
  - L08 Cache Coherency & MMU (cache_coherency.py)
  - L09 Multi-Tenant & Scalability (multi_tenant.py)
  - L10 OS & Ecosystem Compatibility (ecosystem_compat.py)
- 티어별 가중치 테이블 3종
- GP Fabrication Gate 확장 블로커 2종
- 프리셋 3종 추가 (GP_DDR5_Compatible, GP_CXL_Datacenter, Hybrid_SmartMemory_Module)
- CLI --tier 옵션
- Edge signal / summary에 design_tier 필드

### Test Count

- **58 tests** (pytest)

### Integrity

- `SIGNATURE.sha256` regenerated at release time

---

## Block #1 — v0.1.0

- **Date**: 2026-04-15
- **Author**: GNJz / 00_BRAIN
- **Version**: memory-chip-readiness 0.1.0

### Changes

- 최초 릴리스: 6레이어 Ω_chip, ChipVerdict, Fabrication Gate, Chip Bridge
- 프리셋 5종, CLI, Edge AI, SHA-256 서명
- GitHub Actions CI

### Test Count

- **37 tests**

---

*Previous Block: Genesis (none)*
