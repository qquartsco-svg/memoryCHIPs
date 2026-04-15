> **한국어 (정본).** English: [CONCEPT_EN.md](CONCEPT_EN.md)

# Memory Chip Readiness Foundation — 설계 철학

## 핵심 질문

> "소프트웨어로 돌아가는 기억 로직을, 실리콘 위에서 돌릴 수 있는가?"

이 엔진은 이 질문에 대한 **준비도**를 측정한다.

---

## 배경: 왜 메모리를 칩으로?

00_BRAIN에서 설계한 단기/장기/통합 메모리는
에이전트, 로봇, 안드로이드, 자비스, 우주선 등에 탑재될 **인지 기억 시스템**이다.

소프트웨어만으로도 동작하지만, 다음 시나리오에서는 **하드웨어 가속**이 필수다:

- **초저지연**: 로봇 실시간 반사 (μs 단위 recall)
- **저전력**: 엣지/IoT/우주선 (mW 급 예산)
- **대역폭**: LTM에서 수만 벡터를 초당 검색
- **내구성**: 전원 장애, 방사선, 극한 온도

이 엔진은 "소프트웨어 기억"이 "실리콘 기억"으로 전환되는 경로의
**현재 위치**와 **병목**을 수치로 읽는다.

---

## 칩 설계 4층 모델

| 층 | 설명 | 이 엔진과의 관계 |
|---|---|---|
| **동작 명세** | Python 코드 (put/get/decay/recall/consolidate) | STM/LTM 패키지가 이미 완성 |
| **마이크로아키텍처** | 블록 다이어그램, FSM, 파이프라인 | L01–L03이 측정 |
| **RTL/회로** | Verilog/VHDL, SRAM controller, CAM | RTL coverage %로 추적 |
| **물리 구현** | 공정 노드, SRAM/MRAM/Flash, 면적/전력/DFT | L04–L06이 측정 |

---

## STM vs LTM: 칩 구현 난이도 차이

### STM — "정책형 스마트 버퍼"

단기 메모리는 하드웨어화가 비교적 쉽다.

- bounded slots → 고정 크기 SRAM 배열
- strength / decay → fixed-point 연산 + FSM
- TTL / eviction → 타이머 + 우선순위 선택기
- query / namespace → 태그 매칭 로직

**칩 블록**: Slot SRAM + Decay Engine + TTL Timer + Eviction Arbiter + Query Filter + Control FSM

### LTM — "검색형 메모리 서브시스템"

장기 메모리는 칩 단독보다 **하이브리드**가 현실적이다.

- well / importance → 외부 persistent storage + 온칩 메타데이터 캐시
- similarity / top-k → dot product 가속기 (고정소수점)
- episodic log → 시간순 링 버퍼 + 외부 저장소
- consolidation → DMA 기반 스케줄러

**칩 블록**: Persistent Store Interface + Similarity Engine + Top-K Selector + Episodic Log + Consolidation Controller + Host Interface

---

## 권장 구조: Memory Accelerator Chip

범용 CPU처럼 만들지 않고, **메모리 코프로세서(Memory Accelerator)**로 만든다.

```
┌─────────────────────────────────────────────┐
│            Host CPU / NPU                    │
│  (언어 처리, 에이전트 로직, 추론)             │
└──────────────────┬──────────────────────────┘
                   │ AXI4 / PCIe / SPI
┌──────────────────┴──────────────────────────┐
│        Memory Accelerator Chip               │
│  ┌─────────────┐  ┌─────────────────────┐   │
│  │ STM Engine  │  │ LTM Search Engine   │   │
│  │ (On-chip    │  │ (Similarity + Top-K)│   │
│  │  SRAM)      │  │                     │   │
│  └─────────────┘  └─────────────────────┘   │
│  ┌─────────────────────────────────────┐    │
│  │ Consolidation Scheduler (DMA)       │    │
│  └─────────────────────────────────────┘    │
│  ┌──────────────┐  ┌──────────────────┐     │
│  │ Decay/TTL HW │  │ Host Interface   │     │
│  └──────────────┘  └──────────────────┘     │
└──────────────────┬──────────────────────────┘
                   │ SPI / QSPI / ONFI
┌──────────────────┴──────────────────────────┐
│       External Persistent Storage            │
│       (Flash / SSD / MRAM)                   │
└─────────────────────────────────────────────┘
```

---

## 00_BRAIN 에코시스템 내 위치

```
R&D Readiness (아이디어 → 증거)
     │
Memory Logic (STM/LTM/Consolidation)  ← 행동 명세
     │
Memory Chip Readiness  ← 이 엔진 (번역 준비도)
     │
     ├── NPU Architecture Foundation (연산 검증)
     ├── HBM System (대역폭 정합)
     ├── HBF Readiness (플래시 계층)
     ├── Chip Signoff (DRC/LVS/수율)
     ├── Logic Die Stack (풀 스택 통합)
     │
     └── Foundry Ramp → ASIC 테이프아웃
```

---

## 6레이어가 동시에 약하면

"상류가 깨지면 하류 팩토리는 무너진다"는 원칙이 여기서도 적용된다.

- L01(STM)이 약하면: 기본 버퍼조차 하드웨어로 못 내림
- L02(LTM)가 약하면: 지능형 검색 없이 단순 메모리로 전락
- L04(물리)가 약하면: 좋은 설계도 실리콘 위에 올릴 수 없음
- L06(공정)이 약하면: 테이프아웃 자체가 불가능

이 엔진은 이 6개 축의 **동시 건강도**를 Ω_chip으로 읽는다.

---

## 결론

Memory Chip Readiness Foundation은
**메모리 소프트웨어 로직이 실리콘으로 가는 길의 현재 위치를 읽는 계기판**이다.

실제 RTL을 생성하지 않고, 실제 EDA를 돌리지 않지만,
"지금 어디까지 준비됐고, 무엇이 병목인가"를 수치로 알려준다.

이 수치가 충분히 높아지면, 다음 단계는 **실제 Verilog/VHDL → FPGA → ASIC**이다.
