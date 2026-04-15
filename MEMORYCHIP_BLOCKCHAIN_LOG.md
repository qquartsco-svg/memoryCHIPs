# Memory Chip Readiness — Blockchain Log

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
