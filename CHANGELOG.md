> **한국어 (정본).** English: [CHANGELOG_EN.md](CHANGELOG_EN.md)

# Changelog

## [0.2.0] — 2026-04-15

### 범용(General-Purpose) 확장

- **DesignTier** 도입: `accelerator` / `general_purpose` / `hybrid` 모드 전환
- **GP Extension 4개 레이어 추가** (L07-L10):
  - L07 Standard Memory Interface (DDR5/LPDDR5/HBM3/CXL, JEDEC 준수)
  - L08 Cache Coherency & MMU (MESI/MOESI/CHI, TLB, 가상 메모리)
  - L09 Multi-Tenant & Scalability (프로세스 격리, QoS, 다이 스태킹)
  - L10 OS & Ecosystem Compatibility (커널 드라이버, Linux, NUMA, RAS)
- **티어별 가중치 테이블** 3종 (accelerator 6레이어 / GP 10레이어 / hybrid 10레이어)
- **GP Fabrication Gate** 확장: `standard_interface_not_defined`, `cache_coherency_missing` 블로커 추가
- **GP 프리셋 3종 추가**: `GP_DDR5_Compatible`, `GP_CXL_Datacenter`, `Hybrid_SmartMemory_Module`
- **CLI `--tier` 옵션** 추가 (gate-test에서 티어 오버라이드)
- **Edge signal / summary에 `design_tier` 필드** 추가
- **테스트 58개** (37 → 58, +21)
- 버전 0.1.0 → 0.2.0

## [0.1.0] — 2026-04-15

### 최초 릴리스

- 6레이어 Ω_chip 스크리닝 엔진 (L01-L06)
- ChipVerdict 5단계 판정
- Fabrication Readiness Gate (7 blockers)
- Chip Bridge Signal (NPU/HBM/HBF 연동)
- 프리셋 5종, CLI, Edge AI signal, JSON summary
- 테스트 37개, CI, SHA-256 서명
