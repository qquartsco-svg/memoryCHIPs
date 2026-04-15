> **한국어 (정본).** English: [README_EN.md](README_EN.md)

# 🧠 Memory Chip Readiness Foundation

**뇌 메모리 로직(STM · LTM · Consolidation) → 실리콘 칩 준비도 스크리닝 엔진**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.3.0-orange)](CHANGELOG.md)
[![Tests](https://img.shields.io/badge/tests-80%20passed-brightgreen)](memory_chip_readiness/tests/test_memory_chip.py)
[![CI](https://github.com/qquartsco-svg/memoryCHIPs/actions/workflows/ci.yml/badge.svg)](https://github.com/qquartsco-svg/memoryCHIPs/actions)

---

> **법적·기술적 범위 (필독)**
> 이 소프트웨어는 실제 EDA 툴·파운드리 생산·테이프아웃 도구가 아니다.
> ASIC/FPGA/SoC 개념은 교육적 프레임으로만 참조하며, 모든 출력은 휴리스틱 모형의 추정이다.
> 실제 칩 설계·제조·검증에 관한 판단은 자격 있는 IC 설계 전문가와 EDA 툴체인에 따른다.

---

## 목차

1. [배경: 왜 이 엔진이 필요한가](#1-배경-왜-이-엔진이-필요한가)
2. [핵심 개념: 기억 기계란 무엇인가](#2-핵심-개념-기억-기계란-무엇인가)
3. [소프트웨어 → 실리콘 변환 경로](#3-소프트웨어--실리콘-변환-경로)
4. [칩 아키텍처: 기억 전용 코프로세서](#4-칩-아키텍처-기억-전용-코프로세서)
5. [10레이어 평가 모델 — Ω_chip 수식](#5-10레이어-평가-모델--ω_chip-수식)
6. [DesignTier: 전문·범용·혼합 3트랙](#6-designtier-전문범용혼합-3트랙)
7. [DesignPhase: 구현 성숙도 5단계](#7-designphase-구현-성숙도-5단계)
8. [판정 구간 (ChipVerdict)](#8-판정-구간-chipverdict)
9. [Fabrication Readiness Gate](#9-fabrication-readiness-gate)
10. [Chip Bridge — 기존 엔진 연동](#10-chip-bridge--기존-엔진-연동)
11. [빠른 시작](#11-빠른-시작)
12. [프리셋 10종](#12-프리셋-10종)
13. [CLI 사용법](#13-cli-사용법)
14. [전체 운영 흐름](#14-전체-운영-흐름)
15. [확장·활용 방향](#15-확장활용-방향)
16. [현재 한계](#16-현재-한계)
17. [추후 방향](#17-추후-방향)
18. [무결성·블록체인 서명](#18-무결성블록체인-서명)
19. [패키지 구조](#19-패키지-구조)
20. [라이선스](#20-라이선스)

---

## 1. 배경: 왜 이 엔진이 필요한가

인공지능 에이전트, 로봇, 안드로이드, 우주선 탑재 컴퓨터에는 공통된 문제가 있다.

> "기억을 어디에, 어떻게, 얼마나 빠르게 저장하고 다시 꺼낼 수 있는가?"

현재 대부분의 AI 시스템은 **소프트웨어 레벨**에서만 기억을 관리한다 —  
Python 딕셔너리, 벡터 DB, 파일 캐시 등. 하지만 이것들은 본질적으로 CPU/GPU에 의존하며  
전력·지연·전용성 측면에서 비효율적이다.

**00_BRAIN**은 인간의 뇌를 모델링하는 프로젝트로, 다음 세 가지 메모리 레이어를 Python으로 설계했다:

```
Short-Term Memory (STM)    ← 작업 기억 / 수 초~수 분 / 고속 접근
Long-Term Memory  (LTM)    ← 장기 기억 / 영구 저장 / 유사도 검색
Consolidation              ← STM → LTM 통합 / 잠자는 동안의 기억 정리
```

**Memory Chip Readiness Foundation**은 이 소프트웨어 기억 로직이  
**실제 실리콘 칩**이 될 수 있는지를 10개 레이어로 정량 평가하는 엔진이다.

칩이 되면 무엇이 달라지는가:

| 항목 | 소프트웨어 | 전용 칩 |
|---|---|---|
| 응답 지연 | ms ~ 수십 ms | μs (마이크로초) 미만 |
| 전력 효율 | CPU 항상 온 | 슬립 + 이벤트 기반 |
| 병렬 처리 | 단일 스레드/코어 | 하드웨어 병렬 파이프라인 |
| 메모리 정책 | 코드로 실행 | FSM·회로로 즉시 실행 |
| 호스트 부담 | CPU가 전부 처리 | 코프로세서가 분산 처리 |

---

## 2. 핵심 개념: 기억 기계란 무엇인가

### 기존 메모리 칩과 무엇이 다른가

```
[ 기존 메모리 칩 ]           [ 기억형 메모리 칩 (이 엔진이 목표) ]

 CPU ──► DRAM                CPU/NPU ──► Memory Coprocessor ──► DRAM/Flash
         │                              │
         저장 & 읽기                    ├─ decay (시간에 따라 기억 약화)
         (정책 없음)                    ├─ eviction (가득 차면 약한 기억 제거)
                                        ├─ TTL (기억 만료 타이머)
                                        ├─ similarity search (유사한 기억 찾기)
                                        ├─ top-k recall (상위 k개 회상)
                                        └─ consolidation (단기 → 장기 통합)
```

기존 칩이 **"저장 장치"**라면, 기억형 칩은 **"운용 정책이 하드웨어에 내장된 기억 장치"**다.

### STM: 단기 기억 (Short-Term Memory)

```
┌─────────────────────────────────────────────────────┐
│  STM Slot Array  (SRAM 기반, 최대 N 슬롯)            │
│                                                      │
│  slot[0]: {key, strength=0.87, ttl=120s, ns="work"} │
│  slot[1]: {key, strength=0.54, ttl=60s,  ns="env"}  │
│  slot[2]: {key, strength=0.21, ttl=15s,  ns="work"} ← 약해짐
│  ...                                                 │
│                                                      │
│  ──[ Decay Engine FSM ]──  매 클럭마다 strength 감소 │
│  ──[ TTL Timer ]──         만료 슬롯 자동 퇴출        │
│  ──[ Eviction Arbiter ]──  가득 차면 약한 슬롯 제거   │
│  ──[ Query Filter Block ]── namespace·priority 필터  │
└─────────────────────────────────────────────────────┘
```

- **strength**: 기억 강도 (0.0 ~ 1.0). 시간이 지나면 decay 감소.
- **TTL**: 기억 유효 시간. 만료되면 자동 제거.
- **eviction**: 슬롯이 가득 찰 때 가장 약한 기억을 밀어냄.
- **namespace**: 기억 종류 분리 (작업/환경/감각 등).

### LTM: 장기 기억 (Long-Term Memory)

```
┌──────────────────────────────────────────────────────────┐
│  LTM Well Store  (MRAM/Flash, 수천~수백만 레코드)         │
│                                                          │
│  well[0]: {vector[256], importance=0.92, recall_cnt=15}  │
│  well[1]: {vector[256], importance=0.67, recall_cnt=3}   │
│  ...                                                     │
│                                                          │
│  ──[ Similarity Engine ]──  입력 벡터와 코사인/내적 계산  │
│       query_vec ──► dot_product_accel ──► distance[]     │
│       distance[] ──► top-k sorter ──► 상위 k개 반환       │
│                                                          │
│  ──[ Episodic Log Engine ]── 시간순 에피소드 기록          │
└──────────────────────────────────────────────────────────┘
```

- **vector**: 기억의 의미적 표현 (임베딩). dim=128~512.
- **importance**: 중요도. 높을수록 consolidation 우선.
- **top-k recall**: 쿼리와 가장 유사한 k개 기억 반환.
- **similarity engine**: 내적(dot product) 또는 코사인 거리 연산 전용 회로.

### Consolidation: 기억 통합

```
STM의 strength가 임계치(θ) 이상인 슬롯
          │
          ▼ (eligibility FSM이 조건 판단)
    [ Consolidation Controller ]
          │  DMA: STM SRAM → Compression Engine → LTM Flash
          │
          ▼
    LTM에 well로 영구 저장
    STM 슬롯은 해제 또는 strength 초기화
```

수면 중, 또는 주기적 타이머에 의해 STM의 강한 기억이 LTM으로 이동된다.  
이것이 인간의 "잠자는 동안 기억이 정리되는" 현상의 하드웨어 버전이다.

---

## 3. 소프트웨어 → 실리콘 변환 경로

소프트웨어 로직의 각 개념은 하드웨어 블록으로 직접 번역된다:

```
Python 소프트웨어 로직               실리콘 하드웨어 블록
────────────────────────────────────────────────────────
STM: slot dict                  →   Slot SRAM (fixed-size register file)
STM: strength float             →   8-bit fixed-point strength register
STM: decay(strength, dt)        →   Decay Engine FSM (클럭당 감산 회로)
STM: ttl / expiry check         →   TTL Counter Array + Comparator
STM: evict_weakest()            →   Min-Heap Arbiter (HW sort)
STM: query(ns, priority)        →   Query Filter Block (CAM lookup)

LTM: well storage               →   MRAM / NOR Flash (persistent)
LTM: vector embedding           →   Fixed-dim register (dim × width bits)
LTM: cosine_similarity()        →   Dot-Product Accelerator (MAC array)
LTM: top_k()                    →   Partial Sort Network (k-way merge)
LTM: episodic_log               →   Ring Buffer + Timestamp Unit

Consolidation: eligibility()    →   Strength Threshold Comparator + FSM
Consolidation: bridge()         →   DMA Controller (STM→LTM transfer)
Consolidation: compress()       →   Compression Engine (delta/entropy)
Consolidation: merge_arbiter    →   Merge Priority Arbiter
```

변환의 핵심 원리:

```
소프트웨어의 "함수 호출"  →  하드웨어의 "1~수 클럭 동작"
소프트웨어의 "조건문"     →  하드웨어의 "조합 논리 (combinational logic)"
소프트웨어의 "반복문"     →  하드웨어의 "병렬 파이프라인"
소프트웨어의 "float 연산" →  하드웨어의 "fixed-point 연산기 (정밀도 손실 최소화)"
```

---

## 4. 칩 아키텍처: 기억 전용 코프로세서

```
┌─────────────────────────────────────────────────────────────────────┐
│                 HOST SYSTEM                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────────────────────────┐ │
│   │  Host    │    │  NPU     │    │  Memory Coprocessor (이 칩)  │ │
│   │  CPU     │◄──►│ (추론)   │◄──►│                              │ │
│   └──────────┘    └──────────┘    │  ┌──────────────────────┐   │ │
│         │                         │  │  STM Policy Engine    │   │ │
│         │    AXI4 / PCIe / CXL    │  │  - Slot SRAM          │   │ │
│         └────────────────────────►│  │  - Decay FSM          │   │ │
│                                   │  │  - Eviction Arbiter   │   │ │
│                                   │  │  - TTL Timer          │   │ │
│                                   │  │  - Query Filter       │   │ │
│                                   │  └──────────┬───────────┘   │ │
│                                   │             │ DMA            │ │
│                                   │  ┌──────────▼───────────┐   │ │
│                                   │  │  Consolidation Ctrl   │   │ │
│                                   │  │  - Eligibility FSM    │   │ │
│                                   │  │  - Compression Engine │   │ │
│                                   │  │  - Merge Arbiter      │   │ │
│                                   │  └──────────┬───────────┘   │ │
│                                   │             │                │ │
│                                   │  ┌──────────▼───────────┐   │ │
│                                   │  │  LTM Search Engine    │   │ │
│                                   │  │  - Similarity Accel   │   │ │
│                                   │  │  - Top-k Sorter       │   │ │
│                                   │  │  - Episodic Log       │   │ │
│                                   │  └──────────┬───────────┘   │ │
│                                   └─────────────┼───────────────┘ │
└─────────────────────────────────────────────────┼─────────────────┘
                                                  │
                                    ┌─────────────▼─────────────┐
                                    │   External Memory         │
                                    │  (MRAM / NOR Flash / SSD) │
                                    └───────────────────────────┘
```

이 구조가 기존 칩과 다른 점:
- 호스트 CPU는 "기억 관리" 부담 없이 **추론과 제어에만 집중**
- 기억 정책(decay·eviction·consolidation)은 **전용 하드웨어**가 실시간 처리
- top-k 유사도 검색은 **전용 MAC 배열**이 μs 단위로 처리

---

## 5. 10레이어 평가 모델 — Ω_chip 수식

### 기본 수식

```
         N
Ω_chip = Σ  w_i × ω_i       (0 ≤ Ω_chip ≤ 1)
        i=1

여기서:
  w_i  = 레이어 i 의 가중치   (tier 에 따라 다름)
  ω_i  = 레이어 i 의 점수     (0.0 ~ 1.0)
  N    = 활성 레이어 수       (Accelerator: 6, GP/Hybrid: 10)

  Σ w_i = 1.000  (항상 성립)
```

### Accelerator Tier — 6레이어 (전문 메모리 가속기)

```
Ω_accel = 0.20·ω_stm + 0.22·ω_ltm + 0.13·ω_consol
         + 0.18·ω_phys + 0.12·ω_host + 0.15·ω_proc

          ┌─────────────────────────────────────────────────────┐
          │ L01 STM Microarch      [0.20] ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │
          │ L02 LTM Search Accel   [0.22] ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ← 최대 │
          │ L03 Consolidation Sch  [0.13] ▓▓▓▓▓▓▓▓▓▓▓▓▓         │
          │ L04 Physical Memory    [0.18] ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │
          │ L05 Host Interface     [0.12] ▓▓▓▓▓▓▓▓▓▓▓▓           │
          │ L06 Process/Area/Power [0.15] ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        │
          └─────────────────────────────────────────────────────┘
```

### General-Purpose Tier — 10레이어 (범용 메모리)

```
Ω_gp = 0.10·ω_stm + 0.10·ω_ltm + 0.06·ω_consol
      + 0.12·ω_phys + 0.08·ω_host + 0.12·ω_proc
      + 0.16·ω_std  + 0.10·ω_cache + 0.08·ω_mt + 0.08·ω_eco

          ┌─────────────────────────────────────────────────────┐
          │  [Core Layers — 가속기와 공유]                       │
          │  L01 STM Microarch      [0.10] ▓▓▓▓▓▓▓▓▓▓           │
          │  L02 LTM Search Accel   [0.10] ▓▓▓▓▓▓▓▓▓▓           │
          │  L03 Consolidation Sch  [0.06] ▓▓▓▓▓▓               │
          │  L04 Physical Memory    [0.12] ▓▓▓▓▓▓▓▓▓▓▓▓         │
          │  L05 Host Interface     [0.08] ▓▓▓▓▓▓▓▓             │
          │  L06 Process/Area/Power [0.12] ▓▓▓▓▓▓▓▓▓▓▓▓         │
          │  [GP Extension Layers — 범용 전용]                   │
          │  L07 Standard Interface [0.16] ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ← 최대 │
          │  L08 Cache Coherency    [0.10] ▓▓▓▓▓▓▓▓▓▓           │
          │  L09 Multi-Tenant       [0.08] ▓▓▓▓▓▓▓▓             │
          │  L10 OS & Ecosystem     [0.08] ▓▓▓▓▓▓▓▓             │
          └─────────────────────────────────────────────────────┘
```

### Hybrid Tier — 10레이어 (혼합형)

```
Ω_hyb = 0.14·ω_stm + 0.15·ω_ltm + 0.08·ω_consol
       + 0.14·ω_phys + 0.09·ω_host + 0.12·ω_proc
       + 0.10·ω_std  + 0.07·ω_cache + 0.05·ω_mt + 0.06·ω_eco
```

### 각 레이어가 평가하는 것

```
L01 STM Microarchitecture
  ├─ 슬롯 SRAM 크기 타당성 (max_slots, slot_width_bits)
  ├─ 제어 로직 존재 (eviction / decay_fsm / ttl_timer / query_filter)
  ├─ 사이클 버짓 (put: ≤ 4cy, get: ≤ 2cy 목표)
  └─ RTL 검증 커버리지 (%)

L02 LTM Search Accelerator  ← 가장 중요 (기억형 칩의 핵심)
  ├─ 유사도 엔진 설계 (dot_product / cosine / hamming)
  ├─ top-k 하드웨어 가속 존재
  ├─ 외부 저장소 인터페이스 (Flash/MRAM 연결)
  ├─ 검색 지연 목표 (ns)
  └─ RTL 커버리지

L03 Consolidation Scheduler
  ├─ eligibility FSM (strength > θ 판정 회로)
  ├─ DMA 컨트롤러 (STM SRAM → LTM Flash 블록 이동)
  ├─ Merge Arbiter (중복 기억 병합)
  └─ 전력 게이팅 (슬립 모드)

L04 Physical Memory Layer
  ├─ 기술 선택 성숙도 (SRAM: 1.0, DRAM: 0.95, HBM: 0.85, MRAM: 0.65, ReRAM: 0.45)
  ├─ 용량 산정 (stm_capacity_kb, ltm_capacity_mb)
  ├─ 신뢰성 (ECC, wear-leveling, thermal guard, BIST)
  └─ 내구성 (retention_hours, endurance_cycles)

L05 Host Interface & DMA
  ├─ 버스 프로토콜 (AXI4 / AXI4-Lite / PCIe / CXL)
  ├─ DMA 채널 수
  ├─ 레지스터 맵 정의 여부
  └─ 대역폭 목표 (GB/s)

L06 Process, Area, Power, Test
  ├─ 공정 노드 성숙도 (3nm: 1.0 → 350nm: 0.3)
  ├─ 면적·전력 타당성 (target vs. estimated)
  ├─ DFT scan chain / MBIST 설계
  └─ Signoff DRC/LVS clean

L07 Standard Memory Interface  [GP/Hybrid 전용]
  ├─ JEDEC 표준 선택 (DDR5 / LPDDR5 / HBM3 / CXL)
  ├─ PHY IP 검증
  └─ 신호 무결성 시뮬레이션

L08 Cache Coherency & MMU  [GP/Hybrid 전용]
  ├─ 코히런시 프로토콜 (MESI / MOESI / CHI)
  ├─ TLB 크기 (entries)
  ├─ 가상 주소 지원 (bits)
  └─ 멀티레벨 캐시 구조

L09 Multi-Tenant & Scalability  [GP/Hybrid 전용]
  ├─ 메모리 보호 유닛 (MPU)
  ├─ 프로세스 격리 HW
  ├─ QoS 아비터
  └─ 다이 스태킹 / 채널 본딩

L10 OS & Ecosystem Compatibility  [GP/Hybrid 전용]
  ├─ 커널 드라이버 (Linux / RTOS)
  ├─ NUMA-aware 지원
  ├─ RAS (Reliability, Availability, Serviceability)
  └─ SDK / 개발자 문서
```

---

## 6. DesignTier: 전문·범용·혼합 3트랙

```
                    ┌─────────────────────────────────────────┐
                    │           DesignTier 선택 가이드          │
                    └─────────────────────────────────────────┘

  accelerator (전문)          general_purpose (범용)        hybrid (혼합)
  ─────────────────           ──────────────────────        ─────────────
  로봇 / 엣지 AI              일반 서버·PC·데이터센터        AI 가속 + 표준 인터페이스
  우주선 탑재 컴퓨터          JEDEC 표준 호환 필요           STM 정책 + DDR 연결
  특정 워크로드 전용          OS 드라이버 필요               두 세계의 균형

  6레이어 평가                10레이어 평가                  10레이어 평가
  STM/LTM 가중치 높음         표준 인터페이스 가중치 최대     균형 잡힌 가중치
  DDR 호환 불필요             STM/LTM 가중치 낮음            STM + DDR 동시 요구

  용도: 전용 코프로세서        용도: DIMM/HBM 대체            용도: 스마트 메모리 모듈

  사용법:
  analyze(tier=DesignTier.accelerator)
  analyze(tier=DesignTier.general_purpose)
  analyze(tier=DesignTier.hybrid)
```

---

## 7. DesignPhase: 구현 성숙도 5단계

### 왜 DesignPhase가 필요한가?

Ω_chip 점수는 **입력 파라미터를 기준으로 계산한 이상값(목표값)**이다.  
`rtl_coverage_pct=90`을 넣는다고 해서 RTL이 90% 완성된 게 아니다 —  
"RTL이 90% 완성된다면 이 점수가 나온다"는 **가정 위 추정**이다.

`DesignPhase`는 이 이상값과 현실 사이의 간극을 명시하는 장치다.

```
omega_chip    = 입력 파라미터 기준 이상/목표 점수   (phase 무관)
omega_context = omega_chip × phase_realism         (현실 반영 추정치)
gap_to_tapeout = max(0, 0.85 − omega_chip)          (목표까지 남은 거리)
```

### 5단계 구조

```
 단계              현실 계수   의미
 ──────────────────────────────────────────────────────────────────
 concept       ×0.30   소프트웨어 로직만 존재. RTL·PDK·파운드리 전무.
 specification ×0.52   마이크로아키텍처 명세 완성. RTL 스켈레톤 미착수.
 prototype     ×0.72   FPGA 프로토타입 존재. 일부 RTL 검증됨.
 rtl_complete  ×0.90   Verilog/VHDL 완성. 합성·시뮬레이션 진행 중.
 production    ×1.00   DRC/LVS Signoff 완료. 파운드리 테이프아웃 준비.
```

### 실제 사용 예

```
현재 00_BRAIN 메모리 시스템의 실제 위치
─────────────────────────────────────────────────────────────────
analyze_preset("Brain_Current_State")
  omega_chip    = 0.170  ← "이 설계 방향이 완성되면 달성 가능한 이상값"
  omega_context = 0.051  ← 현실 보정값 (concept × 0.30)
  gap_to_tapeout = 0.680 ← tapeout_ready(0.85)까지 남은 거리

analyze_preset("Robot_Memory_SoC")   ← 목표 시나리오
  omega_chip    = 0.944  ← 모든 파라미터 이상적 설정 시 목표값
  omega_context = 0.283  ← concept 단계에서 현실 보정값
  gap_to_tapeout = 0.000 ← 이상값 기준으론 이미 도달
```

이 두 숫자의 차이가 중요하다:

```
                omega_chip   omega_context
                (이상값)       (현실값)
                ─────────────────────────
Brain_Current_State:   0.170  →  0.051   ← 지금 여기
Brain_Spec_Target:     0.387  →  0.201   ← 명세 완성 후
Robot_Memory_SoC:      0.944  →  0.283   ← 모든 것이 완성될 때
```

### Python API

```python
from memory_chip_readiness import analyze, DesignPhase

# concept 단계 (기본값) — 소프트웨어만 있음
rpt = analyze(design_phase=DesignPhase.concept)
print(f"이상값:       {rpt.omega_chip:.3f}")
print(f"현실 보정값:  {rpt.omega_context:.3f}")   # × 0.30
print(f"목표까지:     {rpt.gap_to_tapeout:.3f}")
print(rpt.phase_note)

# prototype 단계 — FPGA 검증 후
rpt2 = analyze(design_phase=DesignPhase.prototype)
print(f"현실 보정값:  {rpt2.omega_context:.3f}")  # × 0.72
```

---

## 8. 판정 구간 (ChipVerdict)

```
 Ω_chip
 1.00 ┤
      │  ╔══════════════════════════════╗
 0.85 ┤  ║  tapeout_ready              ║  ← 테이프아웃 준비 완료
      │  ║  RTL·signoff·PDK 확보 완료  ║
 0.70 ┤──╠══════════════════════════════╣
      │  ║  silicon_candidate           ║  ← 실리콘 후보
      │  ║  RTL 정리 후 테이프아웃 가능 ║     (게이트 블로커 해소 필요)
 0.50 ┤──╠══════════════════════════════╣
      │  ║  rtl_ready                  ║  ← RTL 수준
      │  ║  마이크로아키텍처 확정       ║     RTL(Verilog/VHDL) 작성 중
 0.30 ┤──╠══════════════════════════════╣
      │  ║  architecture_defined        ║  ← 아키텍처 정의됨
      │  ║  블록 다이어그램 존재        ║     세부 RTL 미착수
 0.00 ┤──╠══════════════════════════════╣
      │  ║  concept_only               ║  ← 콘셉트 단계
      │  ║  소프트웨어 로직만 존재      ║     하드웨어 설계 미착수
      └──╚══════════════════════════════╝
```

> **주의**: `tapeout_ready`는 Ω_chip ≥ 0.85 **AND** Fabrication Gate 통과 시에만 유지된다.  
> Gate 블로커가 있으면 자동으로 `silicon_candidate`로 하향된다.

---

## 8. Fabrication Readiness Gate

Ω_chip 점수와 별개로, 다음 조건들이 **모두** 통과해야 `ready_for_tapeout = True`가 된다.

```
Fabrication Readiness Gate
══════════════════════════

[ 공통 조건 — Accelerator / GP / Hybrid ]
  ┌─────────────────────────────────────────────────────────┐
  │ ✗  overall_omega_below_0.70  │  Ω_chip < 0.70          │
  │ ✗  stm_microarch_immature    │  L01 ω < 0.40           │
  │ ✗  ltm_search_accel_immature │  L02 ω < 0.35           │
  │ ✗  process_signoff_incomplete│  L06 ω < 0.40           │
  │ ✗  no_foundry_pdk            │  파운드리 PDK 미확보     │
  │ ✗  no_dft_scan_chain         │  DFT scan chain 미설계  │
  │ ✗  no_register_map           │  레지스터 맵 미정의      │
  └─────────────────────────────────────────────────────────┘

[ GP/Hybrid 추가 조건 ]
  ┌─────────────────────────────────────────────────────────┐
  │ ✗  standard_interface_not_defined │ L07 ω < 0.30       │
  │ ✗  cache_coherency_missing        │ L08 ω < 0.20       │
  └─────────────────────────────────────────────────────────┘

블로커가 1개라도 있으면 → ready_for_tapeout = False
```

### 예상 테이프아웃 소요 기간

```
Ω_chip ≥ 0.85  →  약  6개월
Ω_chip ≥ 0.70  →  약 12개월
Ω_chip ≥ 0.50  →  약 18개월
Ω_chip ≥ 0.30  →  약 24개월
Ω_chip < 0.30  →  약 36개월 이상
```

---

## 9. Chip Bridge — 기존 엔진 연동

Memory Chip Readiness는 00_BRAIN 에코시스템의 기존 칩 엔진들과 신호를 교환한다:

```
                    ┌──────────────────────────────┐
  R&D Readiness     │   Memory Chip Readiness       │
  (상류: 연구 단계) ─►│   Foundation                  │─► RTL / FPGA / ASIC
                    └──────────┬─────────┬──────────┘
                               │         │
              chip_bridge       │         │
                     ┌─────────▼──┐  ┌───▼──────────┐
                     │ NPU Arch   │  │  HBM / HBF   │
                     │ Foundation │  │  System       │
                     │            │  │               │
                     │ npu_omega_ │  │ hbm_omega_    │
                     │ hint       │  │ hint          │
                     └────────────┘  └───────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Chip Signoff /     │
                    │  Logic Die Stack    │
                    │  (DRC/LVS/yield)   │
                    └─────────────────────┘
```

```python
rpt = analyze_preset("Robot_Memory_SoC")

# 기존 엔진으로 신호 전달
bridge = rpt.chip_bridge
print(bridge.npu_omega_hint)       # NPU와 결합 시 힌트 점수
print(bridge.hbm_omega_hint)       # HBM 연동 시 힌트 점수
print(bridge.hbf_omega_hint)       # HBF(고속 플래시) 연동 시 힌트 점수
print(bridge.foundry_gate_status)  # "pass" or "pending"
print(bridge.notes)                # 자동 생성 메모

# Edge AI 시스템용 플랫 딕셔너리
sig = rpt.to_edge_signal()
# {"omega_chip": 0.80, "verdict": "silicon_candidate",
#  "l01_stm_microarch": 0.85, "l02_ltm_search_accel": 0.77, ...}
```

---

## 10. 빠른 시작

```bash
# 설치 (stdlib-only — 추가 의존성 없음)
cd Memory_Chip_Readiness_Foundation
pip install -e ".[dev]"

# 테스트 (63개)
python -m pytest memory_chip_readiness/tests -q

# 무결성 검증
python scripts/generate_signature.py --verify
```

```python
from memory_chip_readiness import (
    analyze, analyze_preset, list_presets,
    STMMicroarchProfile, LTMSearchAccelProfile,
    PhysicalMemoryProfile, DesignTier, MemoryTech,
)

# ── 1. 프리셋 분석 ──────────────────────────────────────────────
rpt = analyze_preset("EdgeAI_Memory_Coprocessor")
print(f"Ω_chip     = {rpt.omega_chip:.4f}")
print(f"verdict    = {rpt.verdict.value}")          # silicon_candidate
print(f"bottleneck = {rpt.key_bottleneck}")
print(f"gate_ready = {rpt.fabrication_gate.ready_for_tapeout}")
print(f"blockers   = {rpt.fabrication_gate.blockers}")

# ── 2. 커스텀 프로필 (Accelerator 기본) ────────────────────────
rpt2 = analyze(
    stm=STMMicroarchProfile(
        max_slots=128,
        eviction_policy_defined=True,
        decay_engine_fsm=True,
        ttl_timer_hw=True,
        sram_compiler_validated=True,
        cycle_budget_put=3,
        cycle_budget_get=2,
        rtl_coverage_pct=60.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=256,
        similarity_engine_type="cosine",
        top_k_hw=True,
        max_wells=8192,
        external_storage_interface=True,
        search_latency_target_ns=500,
        rtl_coverage_pct=50.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram,
        stm_capacity_kb=64,
        ltm_capacity_mb=256,
        ecc_support=True,
        tech_validated=True,
    ),
)
print(f"Custom Ω_chip = {rpt2.omega_chip:.4f}")

# ── 3. General-Purpose 티어 분석 ───────────────────────────────
rpt3 = analyze_preset("GP_DDR5_Compatible")
print(f"GP Ω_chip = {rpt3.omega_chip:.4f}")
print(f"Layer count = {len(rpt3.layer_details)}")   # 10

# ── 4. 포트폴리오 스크리닝 ─────────────────────────────────────
results = {name: analyze_preset(name) for name in list_presets()}
ranked  = sorted(results.items(), key=lambda x: x[1].omega_chip, reverse=True)
for name, r in ranked:
    print(f"{r.omega_chip:.3f}  {r.verdict.value:25s}  {name}")

# ── 5. 연동 신호 추출 ──────────────────────────────────────────
sig     = rpt.to_edge_signal()   # flat dict (float/bool/str/int 값만)
summary = rpt.to_summary_dict()  # JSON 직렬화 가능 딕셔너리
```

---

## 12. 프리셋 10종

### Reality Tier — 실제 현재 구현 상태 (2종) ← 여기서부터 읽는다

| 프리셋 | 단계 | Ω 이상값 | Ω 현실값 | 판정 |
|---|---|---|---|---|
| `Brain_Current_State` | concept (RTL 전무) | 0.17 | **0.05** | concept_only |
| `Brain_Spec_Target` | specification (명세 완성 목표) | 0.39 | **0.20** | architecture_defined |

> **이것이 실제 우리가 지금 있는 위치다.** `Brain_Current_State`는 Python 코드는 완성됐지만
> RTL·파운드리·PDK가 없는 현재 상태를 반영한다. omega_context(현실값)=**0.05**.

### Accelerator Tier — 전문 메모리 가속기 목표 시나리오 (5종)

| 프리셋 | Ω 이상값 | Ω 현실값(concept) | 판정 |
|---|---|---|---|
| `FPGA_STM_Prototype` | 0.29 | 0.09 | concept_only |
| `EdgeAI_Memory_Coprocessor` | **0.82** | 0.25 | silicon_candidate |
| `Robot_Memory_SoC` | **0.94** | 0.28 | tapeout_ready |
| `Concept_BrainChip` | 0.17 | 0.05 | concept_only |
| `Spaceship_MemoryUnit` | 0.78 | 0.24 | silicon_candidate |

> 모든 Accelerator 프리셋의 design_phase는 `concept`(기본값). Ω 이상값은 "해당 파라미터가
> 모두 달성되면 얻는 목표 점수"이며, Ω 현실값은 concept 단계 보정(×0.30)이다.

### General-Purpose Tier — 범용 메모리 (2종)

| 프리셋 | Ω 이상값 | Ω 현실값(concept) | 판정 |
|---|---|---|---|
| `GP_DDR5_Compatible` | **0.88** | 0.26 | tapeout_ready |
| `GP_CXL_Datacenter` | **0.89** | 0.27 | tapeout_ready |

### Hybrid Tier — 혼합형 (1종)

| 프리셋 | Ω 이상값 | Ω 현실값(concept) | 판정 |
|---|---|---|---|
| `Hybrid_SmartMemory_Module` | **0.84** | 0.25 | silicon_candidate |

Reality 2종 외 모든 프리셋은 **가상 설계 목표 시나리오**이며 실제 특정 칩 제품과 무관하다.

---

## 12. CLI 사용법

```bash
# 프리셋 목록 확인
memory-chip-readiness list-presets

# 프리셋 분석 (텍스트 리포트)
memory-chip-readiness analyze EdgeAI_Memory_Coprocessor

# JSON 출력
memory-chip-readiness analyze Robot_Memory_SoC --json

# Edge AI 신호 출력
memory-chip-readiness analyze Spaceship_MemoryUnit --edge

# General-Purpose 티어로 Gate 테스트
memory-chip-readiness gate-test FPGA_STM_Prototype --tier general_purpose --json

# GP 전용 프리셋 분석
memory-chip-readiness analyze GP_DDR5_Compatible --json
memory-chip-readiness analyze GP_CXL_Datacenter
memory-chip-readiness analyze Hybrid_SmartMemory_Module
```

---

## 13. 전체 운영 흐름

```
◀──────────────── 상류 (연구) ─────────────────────────────── 하류 (실리콘) ──────────────►

[R&D Readiness]  →  [Memory Chip Readiness]  →  [RTL]  →  [FPGA]  →  [ASIC Tapeout]
  · 가설 명료성        · 10레이어 Ω_chip              Verilog     프로토타입    파운드리
  · 재현성              · DesignTier 선택              VHDL       검증           제조
  · IP/FTO             · Gate 통과 확인
  · 런웨이

──────────────────────────────────────────────────────────────────────────────────────────

상세 흐름:

 [1] STM / LTM / Consolidation 소프트웨어 로직 완성
      │
      ▼
 [2] Memory Chip Readiness 분석 (DesignTier 선택)
      │   ├─ Accelerator: 6레이어 평가
      │   ├─ General-Purpose: 10레이어 평가
      │   └─ Hybrid: 10레이어 평가 (균형 가중치)
      │
      ▼
 [3] verdict 확인 및 병목 레이어 개선
      │   concept_only  → 마이크로아키텍처 설계 착수
      │   arch_defined  → RTL 스켈레톤 작성
      │   rtl_ready     → 시뮬레이션 + 커버리지 향상
      │   silicon_cand  → Gate 블로커 해소
      │   tapeout_ready → 테이프아웃 준비
      │
      ▼
 [4] Fabrication Gate 통과
      │   blockers 해소 → ready_for_tapeout = True
      │   estimated_tapeout_months 확인
      │
      ▼
 [5] Chip Bridge 신호 → 기존 엔진 연동
      │   NPU / HBM / HBF / Chip Signoff 연결
      │
      ▼
 [6] Verilog/VHDL RTL 작성 → EDA 툴체인 (Synopsys/Cadence)
      │
      ▼
 [7] FPGA 프로토타입 → latency/power 실측
      │
      ▼
 [8] ASIC 테이프아웃 → 파운드리 (TSMC/Samsung/GF)
```

---

## 14. 확장·활용 방향

### 14.1 에이전트·상위 시스템 연동

```python
# 00_BRAIN 에코시스템 연동 예시
rpt = analyze_preset("EdgeAI_Memory_Coprocessor")

# RockLEE IndustrialSignal 형식
sig = rpt.to_edge_signal()
# → {"omega_chip": 0.72, "verdict": "silicon_candidate",
#    "l01_stm_microarch": 0.81, "l02_ltm_search_accel": 0.68, ...}

# JSON 요약 (Streamlit / React 대시보드용)
summary = rpt.to_summary_dict()
```

### 14.2 포트폴리오 스크리닝

```python
# 모든 프리셋을 한번에 분석하여 랭킹 추출
results = {n: analyze_preset(n) for n in list_presets()}
ranked  = sorted(results.items(), key=lambda x: x[1].omega_chip, reverse=True)

# 병목 레이어 분포 확인
from collections import Counter
bottlenecks = Counter(r.key_bottleneck for r in results.values())
print(bottlenecks)  # 가장 많이 막히는 레이어 파악
```

### 14.3 What-if 시뮬

```python
# "LTM 검색 엔진을 더 발전시키면 얼마나 올라가는가?"
base = analyze_preset("FPGA_STM_Prototype")
improved = analyze(
    stm=...,
    ltm=LTMSearchAccelProfile(
        top_k_hw=True,
        similarity_engine_type="cosine",
        rtl_coverage_pct=60,
    ),
    # 나머지는 기본값
)
print(f"개선 전: {base.omega_chip:.4f}")
print(f"개선 후: {improved.omega_chip:.4f}")
print(f"증가분:  +{improved.omega_chip - base.omega_chip:.4f}")
```

### 14.4 대시보드 / 리포트

`to_summary_dict()` JSON을 Streamlit, React, Grafana 등에 직접 전달 가능.  
레이어별 점수 → 레이더 차트, 판정 히스토리 → 타임라인 시각화를 즉시 구성할 수 있다.

---

## 15. 현재 한계

| 항목 | 내용 |
|---|---|
| 모형 단순화 | 각 레이어 점수는 선형 휴리스틱이며 실제 EDA 시뮬레이션·signoff를 대체하지 않음 |
| RTL 미생성 | Verilog/VHDL 코드를 생성하지 않음 — 준비도 평가만 수행 |
| EDA 미연동 | 실제 EDA 툴(Synopsys/Cadence/Mentor) 직접 연동 없음 |
| 미보정 | 실제 테이프아웃 데이터로 가중치가 보정되지 않음 |
| 메모리 전용 | CPU/GPU/NPU 전체 SoC 평가가 아닌 메모리 서브시스템 평가 |
| 프리셋 제한 | 8종. 실제 칩 설계 다양성을 커버하기에 부족 |
| PPA 추정 단순 | 면적·전력·지연 추정이 공정 노드 성숙도 기반 단순 휴리스틱 |

---

## 16. 추후 방향

```
Phase 1 (단기 — 3~6개월)
  ├─ 프리셋 확장: MCU 메모리, IoT 메모리, 자동차 기능안전(ISO 26262) 메모리
  ├─ STM RTL 스켈레톤 생성기: Verilog 템플릿 자동 생성
  └─ Streamlit 대시보드: 10레이어 레이더 차트 + 판정 히스토리

Phase 2 (중기 — 6~18개월)
  ├─ LTM Similarity Engine RTL: dot-product 가속기 Verilog 구현
  ├─ FPGA 프로토타입 워크플로우: Vivado / Quartus 연동
  ├─ EDA 어댑터: Synopsys DC / Innovus 면적·전력 피드백
  └─ 00_BRAIN 에코시스템: NPU / HBM / HBF 정식 어댑터

Phase 3 (장기 — 18개월+)
  ├─ 실제 테이프아웃 데이터로 가중치 재보정
  ├─ ML 기반 PPA 추정 (면적·전력·지연 예측 모델)
  ├─ Memory SoC 풀 스택: CPU + Memory Accelerator 통합 평가
  └─ GDS II / OASIS 레이아웃 수준 검증 연동
```

---

## 17. 무결성·블록체인 서명

Memory Chip Readiness Foundation은 **SHA-256 매니페스트**로 코드 무결성을 추적한다.

```bash
# 서명 재생성 (파일 변경 후)
python scripts/generate_signature.py

# 검증 (배포 전 반드시 실행)
python scripts/generate_signature.py --verify
```

```
SIGNATURE.sha256       ← 22개 파일의 SHA-256 해시 매니페스트
MEMORYCHIP_BLOCKCHAIN_LOG.md ← 릴리스별 변경 이력 + 무결성 기록
BLOCKCHAIN_INFO.md     ← 서명 정책 설명
```

현재 서명 상태:

```
v0.2.0  22 files verified  ✓  (Block #3 — 2026-04-15 최종 공개 점검)
```

릴리스 내역 → [MEMORYCHIP_BLOCKCHAIN_LOG.md](MEMORYCHIP_BLOCKCHAIN_LOG.md)  
서명 정책   → [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)

---

## 18. 패키지 구조

```
memoryCHIPs/
├── LICENSE
├── pyproject.toml                  memory-chip-readiness 0.3.0, stdlib-only
├── .gitignore
├── .github/workflows/ci.yml       Python 3.10 · 3.12 CI
├── README.md                      한국어 정본 (이 파일)
├── README_EN.md                   English companion
├── CONCEPT.md / CONCEPT_EN.md     설계 철학 · 개념 심층 문서
├── CHANGELOG.md / CHANGELOG_EN.md 버전별 변경 이력
├── MEMORYCHIP_BLOCKCHAIN_LOG.md   무결성 블록체인 로그
├── BLOCKCHAIN_INFO.md             서명 정책
├── SIGNATURE.sha256               SHA-256 매니페스트 (22 files)
├── scripts/
│   └── generate_signature.py      서명 생성·검증 스크립트
└── memory_chip_readiness/
    ├── py.typed                   PEP 561 타입 마커
    ├── __init__.py                공개 API
    ├── __main__.py                python -m 진입점
    ├── version.py                 __version__ = "0.2.0"
    ├── contracts.py               dataclass 계약 전체 (입출력·enum·DesignTier)
    │
    ├── [Core Layers — 모든 Tier]
    ├── stm_microarch.py            L01 STM 마이크로아키텍처 평가
    ├── ltm_search_accel.py         L02 LTM 검색 가속기 평가
    ├── consolidation_scheduler.py  L03 컨솔리데이션 스케줄러 평가
    ├── physical_memory.py          L04 물리 메모리 계층 평가
    ├── host_interface.py           L05 호스트 인터페이스 & DMA 평가
    ├── process_area_power.py       L06 공정·면적·전력·테스트 평가
    │
    ├── [GP Extension Layers — GP·Hybrid Tier]
    ├── standard_interface.py       L07 표준 메모리 인터페이스 (JEDEC/CXL)
    ├── cache_coherency.py          L08 캐시 코히런시 & MMU
    ├── multi_tenant.py             L09 멀티 테넌트 & 확장성
    ├── ecosystem_compat.py         L10 OS·에코시스템 호환성
    │
    ├── foundation.py               통합 오케스트레이터 (DesignTier 기반 10레이어)
    ├── presets.py                  프리셋 10종 (Accel 5 + GP 2 + Hybrid 1 + Reality 2)
    ├── cli.py                      CLI entry-point (--tier 지원)
    └── tests/
        ├── __init__.py
        └── test_memory_chip.py    80개 테스트
                                    (계약·코어·GP레이어·Foundation·프리셋·
                                     직렬화·CLI·가중치불변식·DesignPhase·Reality)
```

---

## 19. 라이선스

MIT — [LICENSE](LICENSE) 참조.

Copyright © 2026 00_BRAIN / GNJz

---

**Memory Chip Readiness Foundation**
*"메모리의 꿈을 실리콘의 현실로 연결하는 준비도 스크리닝 엔진"*

> 00_BRAIN 에코시스템의 일부 — [R&D Readiness](../RnD_Readiness_Foundation) · [PHAMacy](../PHAMacy) · [SmartFarm](../SmartFarm_Readiness_Foundation)
