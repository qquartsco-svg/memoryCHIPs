> **English.** Korean (정본): [README.md](README.md)

# 🧠 Memory Chip Readiness Foundation

**Brain Memory Logic (STM · LTM · Consolidation) → Silicon Chip Readiness Screening Engine**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.2.0-orange)
![Tests](https://img.shields.io/badge/tests-63%20passed-brightgreen)
![CI](https://github.com/qquartsco-svg/memoryCHIPs/actions/workflows/ci.yml/badge.svg)

---

> **Legal & Technical Scope (required reading)**
> This software is NOT an EDA tool, foundry production system, or tapeout validation tool.
> ASIC/FPGA/SoC concepts are referenced as an educational framework only.
> All outputs are heuristic model estimates. Actual chip design, fabrication, and verification
> require qualified IC design engineers and professional EDA toolchains.

---

## Table of Contents

1. [Background: Why This Engine Exists](#1-background-why-this-engine-exists)
2. [Core Concept: What Is a Memory Machine?](#2-core-concept-what-is-a-memory-machine)
3. [Software → Silicon Translation Path](#3-software--silicon-translation-path)
4. [Chip Architecture: The Memory Coprocessor](#4-chip-architecture-the-memory-coprocessor)
5. [10-Layer Evaluation Model — Ω_chip Formula](#5-10-layer-evaluation-model--ω_chip-formula)
6. [DesignTier: Three Tracks](#6-designtier-three-tracks)
7. [Verdict Bands (ChipVerdict)](#7-verdict-bands-chipverdict)
8. [Fabrication Readiness Gate](#8-fabrication-readiness-gate)
9. [Chip Bridge — Ecosystem Integration](#9-chip-bridge--ecosystem-integration)
10. [Quick Start](#10-quick-start)
11. [8 Presets](#11-8-presets)
12. [CLI Usage](#12-cli-usage)
13. [End-to-End Workflow](#13-end-to-end-workflow)
14. [Extension & Use Cases](#14-extension--use-cases)
15. [Current Limitations](#15-current-limitations)
16. [Roadmap](#16-roadmap)
17. [Integrity & Blockchain Signature](#17-integrity--blockchain-signature)
18. [Package Structure](#18-package-structure)
19. [License](#19-license)

---

## 1. Background: Why This Engine Exists

AI agents, robots, androids, and spacecraft computers share a common problem:

> "Where, how, and how fast can we store and retrieve memory?"

Most AI systems today manage memory entirely in software — Python dicts, vector databases,
file caches. These depend on the host CPU/GPU and are inefficient in latency, power, and
dedicated throughput.

**00_BRAIN** is a project modeling the human brain in Python, with three memory layers:

```
Short-Term Memory (STM)    ← Working memory / seconds to minutes / fast access
Long-Term Memory  (LTM)    ← Persistent memory / similarity search / retrieval
Consolidation              ← STM → LTM integration / "sleep-time" memory organization
```

**Memory Chip Readiness Foundation** evaluates whether this software memory logic is ready
to become a **real silicon chip**, using a 10-layer scoring model (Ω_chip).

What changes when the logic moves to hardware:

| Aspect | Software | Dedicated Chip |
|---|---|---|
| Response latency | ms–tens of ms | sub-μs (microseconds) |
| Power efficiency | CPU always on | sleep + event-driven |
| Parallelism | single-thread/core | hardware parallel pipelines |
| Memory policy | executed in code | FSMs/circuits run immediately |
| Host burden | CPU handles everything | coprocessor distributes load |

---

## 2. Core Concept: What Is a Memory Machine?

### How It Differs from Conventional Memory Chips

```
[ Conventional Memory Chip ]        [ Memory Machine (this engine's target) ]

 CPU ──► DRAM                        CPU/NPU ──► Memory Coprocessor ──► DRAM/Flash
         │                                       │
         store & read                            ├─ decay  (memory weakens over time)
         (no policy)                             ├─ eviction (remove weakest when full)
                                                 ├─ TTL    (expiry timer per memory)
                                                 ├─ similarity search (find related)
                                                 ├─ top-k recall (return top-k matches)
                                                 └─ consolidation (STM → LTM transfer)
```

Conventional chips are **storage devices**. A memory machine is a **storage device with
memory management policy built into hardware**.

### STM: Short-Term Memory

```
┌──────────────────────────────────────────────────────────┐
│  STM Slot Array  (SRAM-based, up to N slots)             │
│                                                          │
│  slot[0]: {key, strength=0.87, ttl=120s, ns="work"}     │
│  slot[1]: {key, strength=0.54, ttl=60s,  ns="env"}      │
│  slot[2]: {key, strength=0.21, ttl=15s,  ns="work"} ← fading
│  ...                                                     │
│                                                          │
│  ──[ Decay Engine FSM ]──  reduces strength every clock  │
│  ──[ TTL Timer ]──         auto-evicts expired slots     │
│  ──[ Eviction Arbiter ]──  removes weakest on overflow   │
│  ──[ Query Filter Block ]── namespace · priority filter  │
└──────────────────────────────────────────────────────────┘
```

- **strength**: Memory intensity (0.0–1.0). Decays over time.
- **TTL**: Time-to-live. Expired slots are removed automatically.
- **eviction**: When slots are full, the weakest memory is displaced.
- **namespace**: Memory type separation (task / environment / sensory, etc.).

### LTM: Long-Term Memory

```
┌──────────────────────────────────────────────────────────────┐
│  LTM Well Store  (MRAM/Flash, thousands to millions of items) │
│                                                              │
│  well[0]: {vector[256], importance=0.92, recall_cnt=15}      │
│  well[1]: {vector[256], importance=0.67, recall_cnt=3}       │
│  ...                                                         │
│                                                              │
│  ──[ Similarity Engine ]──  cosine/dot-product vs. query     │
│       query_vec ──► dot_product_accel ──► distances[]        │
│       distances[] ──► top-k sorter ──► top k results         │
│                                                              │
│  ──[ Episodic Log Engine ]── chronological episode record    │
└──────────────────────────────────────────────────────────────┘
```

- **vector**: Semantic embedding of a memory (dim = 128–512).
- **importance**: Priority for consolidation promotion.
- **top-k recall**: Returns the k most similar memories to a query.
- **similarity engine**: Dedicated circuit for dot-product or cosine distance.

### Consolidation: Memory Integration

```
STM slots whose strength exceeds threshold θ
          │
          ▼  (eligibility FSM evaluates condition)
    [ Consolidation Controller ]
          │  DMA: STM SRAM → Compression Engine → LTM Flash
          │
          ▼
    Permanently stored in LTM as a well
    STM slot is released or strength reset
```

During sleep, or on a periodic timer, strong STM memories are promoted to LTM.
This is the hardware version of "memories consolidate during sleep."

---

## 3. Software → Silicon Translation Path

Every software concept maps directly to a hardware block:

```
Python Software Logic                Silicon Hardware Block
────────────────────────────────────────────────────────────
STM: slot dict               →  Slot SRAM (fixed-size register file)
STM: strength float          →  8-bit fixed-point strength register
STM: decay(strength, dt)     →  Decay Engine FSM (subtract-per-clock circuit)
STM: ttl / expiry check      →  TTL Counter Array + Comparator
STM: evict_weakest()         →  Min-Heap Arbiter (HW sort)
STM: query(ns, priority)     →  Query Filter Block (CAM lookup)

LTM: well storage            →  MRAM / NOR Flash (persistent)
LTM: vector embedding        →  Fixed-dim register (dim × width bits)
LTM: cosine_similarity()     →  Dot-Product Accelerator (MAC array)
LTM: top_k()                 →  Partial Sort Network (k-way merge)
LTM: episodic_log            →  Ring Buffer + Timestamp Unit

Consolidation: eligibility() →  Strength Threshold Comparator + FSM
Consolidation: bridge()      →  DMA Controller (STM→LTM block transfer)
Consolidation: compress()    →  Compression Engine (delta/entropy)
Consolidation: merge_arbiter →  Merge Priority Arbiter
```

Core translation principles:

```
Software "function call"   →  Hardware "1–few clock operation"
Software "conditional"     →  Hardware "combinational logic"
Software "loop"            →  Hardware "parallel pipeline"
Software "float op"        →  Hardware "fixed-point arithmetic (minimal precision loss)"
```

---

## 4. Chip Architecture: The Memory Coprocessor

```
┌──────────────────────────────────────────────────────────────────────┐
│                    HOST SYSTEM                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────────┐  │
│  │  Host    │    │  NPU     │    │  Memory Coprocessor (this)   │  │
│  │  CPU     │◄──►│(inference│◄──►│                              │  │
│  └──────────┘    └──────────┘    │  ┌──────────────────────┐   │  │
│        │                         │  │  STM Policy Engine    │   │  │
│        │    AXI4 / PCIe / CXL   │  │  - Slot SRAM          │   │  │
│        └───────────────────────►│  │  - Decay FSM          │   │  │
│                                  │  │  - Eviction Arbiter   │   │  │
│                                  │  │  - TTL Timer          │   │  │
│                                  │  │  - Query Filter       │   │  │
│                                  │  └──────────┬───────────┘   │  │
│                                  │             │ DMA            │  │
│                                  │  ┌──────────▼───────────┐   │  │
│                                  │  │  Consolidation Ctrl   │   │  │
│                                  │  │  - Eligibility FSM    │   │  │
│                                  │  │  - Compression Engine │   │  │
│                                  │  │  - Merge Arbiter      │   │  │
│                                  │  └──────────┬───────────┘   │  │
│                                  │             │                │  │
│                                  │  ┌──────────▼───────────┐   │  │
│                                  │  │  LTM Search Engine    │   │  │
│                                  │  │  - Similarity Accel   │   │  │
│                                  │  │  - Top-k Sorter       │   │  │
│                                  │  │  - Episodic Log       │   │  │
│                                  │  └──────────┬───────────┘   │  │
│                                  └─────────────┼───────────────┘  │
└────────────────────────────────────────────────┼──────────────────┘
                                                 │
                                   ┌─────────────▼─────────────┐
                                   │   External Memory         │
                                   │  (MRAM / NOR Flash / SSD) │
                                   └───────────────────────────┘
```

What sets this apart:
- Host CPU focuses entirely on **inference and control** — no memory management overhead
- Memory policies (decay · eviction · consolidation) run in **dedicated hardware in real time**
- Top-k similarity search is handled by a **dedicated MAC array** in microseconds

---

## 5. 10-Layer Evaluation Model — Ω_chip Formula

### Base Formula

```
         N
Ω_chip = Σ  w_i × ω_i       (0 ≤ Ω_chip ≤ 1)
        i=1

where:
  w_i  = weight of layer i   (depends on DesignTier)
  ω_i  = score of layer i    (0.0 – 1.0)
  N    = active layer count  (Accelerator: 6, GP/Hybrid: 10)

  Σ w_i = 1.000  (invariant — enforced by tests)
```

### Accelerator Tier — 6 Layers

```
Ω_accel = 0.20·ω_stm + 0.22·ω_ltm + 0.13·ω_consol
         + 0.18·ω_phys + 0.12·ω_host + 0.15·ω_proc

          ┌──────────────────────────────────────────────────────┐
          │ L01 STM Microarch      [0.20] ████████████████████  │
          │ L02 LTM Search Accel   [0.22] ██████████████████████ ← max │
          │ L03 Consolidation Sch  [0.13] █████████████         │
          │ L04 Physical Memory    [0.18] ██████████████████    │
          │ L05 Host Interface     [0.12] ████████████          │
          │ L06 Process/Area/Power [0.15] ███████████████       │
          └──────────────────────────────────────────────────────┘
```

### General-Purpose Tier — 10 Layers

```
Ω_gp = 0.10·ω_stm + 0.10·ω_ltm + 0.06·ω_consol
      + 0.12·ω_phys + 0.08·ω_host + 0.12·ω_proc
      + 0.16·ω_std  + 0.10·ω_cache + 0.08·ω_mt + 0.08·ω_eco

          ┌──────────────────────────────────────────────────────┐
          │  [Core Layers — shared with Accelerator]             │
          │  L01 STM Microarch      [0.10] ██████████           │
          │  L02 LTM Search Accel   [0.10] ██████████           │
          │  L03 Consolidation Sch  [0.06] ██████               │
          │  L04 Physical Memory    [0.12] ████████████         │
          │  L05 Host Interface     [0.08] ████████             │
          │  L06 Process/Area/Power [0.12] ████████████         │
          │  [GP Extension Layers — GP/Hybrid only]              │
          │  L07 Standard Interface [0.16] ████████████████ ← max │
          │  L08 Cache Coherency    [0.10] ██████████           │
          │  L09 Multi-Tenant       [0.08] ████████             │
          │  L10 Ecosystem Compat   [0.08] ████████             │
          └──────────────────────────────────────────────────────┘
```

### What Each Layer Evaluates

```
L01  STM Microarchitecture
     ├─ Slot SRAM sizing (max_slots, slot_width_bits)
     ├─ Control logic presence (eviction / decay_fsm / ttl_timer / query_filter)
     ├─ Cycle budget (put ≤ 4cy, get ≤ 2cy target)
     └─ RTL verification coverage (%)

L02  LTM Search Accelerator  ← highest-weight core layer
     ├─ Similarity engine design (dot_product / cosine / hamming)
     ├─ Top-k hardware acceleration
     ├─ External storage interface (Flash/MRAM)
     ├─ Search latency target (ns)
     └─ RTL coverage

L03  Consolidation Scheduler
     ├─ Eligibility FSM (strength > θ detection circuit)
     ├─ DMA controller (STM SRAM → LTM Flash block transfer)
     ├─ Merge arbiter (duplicate memory merging)
     └─ Power gating (sleep mode support)

L04  Physical Memory Layer
     ├─ Technology maturity (SRAM:1.0, DRAM:0.95, HBM:0.85, MRAM:0.65, ReRAM:0.45)
     ├─ Capacity provisioning (stm_capacity_kb, ltm_capacity_mb)
     ├─ Reliability (ECC, wear-leveling, thermal guard, BIST)
     └─ Durability (retention_hours, endurance_cycles)

L05  Host Interface & DMA
     ├─ Bus protocol (AXI4 / AXI4-Lite / PCIe / CXL)
     ├─ DMA channel count
     ├─ Register map definition
     └─ Bandwidth target (GB/s)

L06  Process, Area, Power, Test
     ├─ Process node maturity (3nm:1.0 → 350nm:0.3)
     ├─ Area/power feasibility (target vs. estimated)
     ├─ DFT scan chain / MBIST design
     └─ Signoff DRC/LVS clean

L07  Standard Memory Interface  [GP/Hybrid only]
     ├─ JEDEC standard selection (DDR5 / LPDDR5 / HBM3 / CXL)
     ├─ PHY IP validation
     └─ Signal integrity simulation

L08  Cache Coherency & MMU  [GP/Hybrid only]
     ├─ Coherency protocol (MESI / MOESI / CHI)
     ├─ TLB size (entries)
     ├─ Virtual address support (bits)
     └─ Multi-level cache hierarchy

L09  Multi-Tenant & Scalability  [GP/Hybrid only]
     ├─ Memory protection unit (MPU)
     ├─ Process isolation HW
     ├─ QoS arbiter
     └─ Die stacking / channel bonding

L10  OS & Ecosystem Compatibility  [GP/Hybrid only]
     ├─ Kernel driver (Linux / RTOS)
     ├─ NUMA-aware support
     ├─ RAS (Reliability, Availability, Serviceability)
     └─ SDK / developer documentation
```

---

## 6. DesignTier: Three Tracks

```
                   ┌──────────────────────────────────────────┐
                   │          DesignTier Selection Guide       │
                   └──────────────────────────────────────────┘

  accelerator                general_purpose              hybrid
  ─────────────              ────────────────             ──────────────
  Robot / Edge AI            Servers · PCs · Data centers  AI accel + std interface
  Spacecraft computer        JEDEC standard compliance       STM policy + DDR link
  Workload-specific          OS driver required             Balanced between both

  6-layer evaluation         10-layer evaluation            10-layer evaluation
  STM/LTM weights high       Standard interface weight max  Balanced weights
  DDR compat not needed      STM/LTM weights low            Both STM + DDR required

  Use: dedicated coprocessor  Use: DIMM/HBM replacement     Use: smart memory module

  Usage:
  analyze(tier=DesignTier.accelerator)
  analyze(tier=DesignTier.general_purpose)
  analyze(tier=DesignTier.hybrid)
```

---

## 7. Verdict Bands (ChipVerdict)

```
 Ω_chip
 1.00 ┤
      │  ╔══════════════════════════════════╗
 0.85 ┤  ║  tapeout_ready                  ║  ← RTL · signoff · PDK complete
      │  ║  Ready to submit to foundry      ║
 0.70 ┤──╠══════════════════════════════════╣
      │  ║  silicon_candidate               ║  ← Silicon candidate
      │  ║  Tapeout possible after RTL      ║     (gate blockers must be cleared)
 0.50 ┤──╠══════════════════════════════════╣
      │  ║  rtl_ready                      ║  ← RTL-level readiness
      │  ║  Microarchitecture confirmed,    ║     Verilog/VHDL being written
      │  ║  writing RTL                     ║
 0.30 ┤──╠══════════════════════════════════╣
      │  ║  architecture_defined            ║  ← Architecture defined
      │  ║  Block diagram exists,           ║     RTL not yet started
      │  ║  RTL not started                 ║
 0.00 ┤──╠══════════════════════════════════╣
      │  ║  concept_only                   ║  ← Concept only
      │  ║  Only software logic exists      ║     No HW design
      └──╚══════════════════════════════════╝
```

> **Note**: `tapeout_ready` is maintained only when Ω_chip ≥ 0.85 **AND** the
> Fabrication Gate passes. Any gate blocker automatically downgrades verdict to `silicon_candidate`.

---

## 8. Fabrication Readiness Gate

Beyond the Ω_chip score, **all** of the following conditions must pass for `ready_for_tapeout = True`:

```
Fabrication Readiness Gate
══════════════════════════

[ Common Conditions — Accelerator / GP / Hybrid ]
  ┌──────────────────────────────────────────────────────────┐
  │ ✗  overall_omega_below_0.70   │  Ω_chip < 0.70          │
  │ ✗  stm_microarch_immature     │  L01 ω < 0.40           │
  │ ✗  ltm_search_accel_immature  │  L02 ω < 0.35           │
  │ ✗  process_signoff_incomplete │  L06 ω < 0.40           │
  │ ✗  no_foundry_pdk             │  No foundry PDK secured  │
  │ ✗  no_dft_scan_chain          │  DFT scan chain missing  │
  │ ✗  no_register_map            │  Register map undefined  │
  └──────────────────────────────────────────────────────────┘

[ GP / Hybrid Additional Conditions ]
  ┌──────────────────────────────────────────────────────────┐
  │ ✗  standard_interface_not_defined │ L07 ω < 0.30        │
  │ ✗  cache_coherency_missing        │ L08 ω < 0.20        │
  └──────────────────────────────────────────────────────────┘

Any single blocker → ready_for_tapeout = False
```

### Estimated Time to Tapeout

```
Ω_chip ≥ 0.85  →  ~  6 months
Ω_chip ≥ 0.70  →  ~ 12 months
Ω_chip ≥ 0.50  →  ~ 18 months
Ω_chip ≥ 0.30  →  ~ 24 months
Ω_chip < 0.30  →  ~ 36+ months
```

---

## 9. Chip Bridge — Ecosystem Integration

Memory Chip Readiness exchanges signals with other 00_BRAIN chip engines:

```
                   ┌──────────────────────────────┐
  R&D Readiness    │   Memory Chip Readiness       │
  (upstream) ─────►│   Foundation                  │─► RTL / FPGA / ASIC
                   └──────────┬──────────┬─────────┘
                              │          │
              chip_bridge     │          │
                    ┌─────────▼──┐  ┌────▼──────────┐
                    │ NPU Arch   │  │  HBM / HBF    │
                    │ Foundation │  │  System        │
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

bridge = rpt.chip_bridge
print(bridge.npu_omega_hint)       # hint score when coupling with NPU
print(bridge.hbm_omega_hint)       # hint score for HBM integration
print(bridge.foundry_gate_status)  # "pass" or "pending"

# Flat signal dict for edge AI systems
sig = rpt.to_edge_signal()
# {"omega_chip": 0.80, "verdict": "silicon_candidate",
#  "l01_stm_microarch": 0.85, "l02_ltm_search_accel": 0.77, ...}
```

---

## 10. Quick Start

```bash
# Install (stdlib-only — no extra dependencies)
cd Memory_Chip_Readiness_Foundation
pip install -e ".[dev]"

# Run tests (63 tests)
python -m pytest memory_chip_readiness/tests -q

# Verify integrity
python scripts/generate_signature.py --verify
```

```python
from memory_chip_readiness import (
    analyze, analyze_preset, list_presets,
    STMMicroarchProfile, LTMSearchAccelProfile,
    PhysicalMemoryProfile, DesignTier, MemoryTech,
)

# ── 1. Preset analysis ──────────────────────────────────────────
rpt = analyze_preset("EdgeAI_Memory_Coprocessor")
print(f"Ω_chip     = {rpt.omega_chip:.4f}")
print(f"verdict    = {rpt.verdict.value}")          # silicon_candidate
print(f"bottleneck = {rpt.key_bottleneck}")
print(f"gate_ready = {rpt.fabrication_gate.ready_for_tapeout}")
print(f"blockers   = {rpt.fabrication_gate.blockers}")

# ── 2. Custom profile (Accelerator tier) ────────────────────────
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

# ── 3. General-Purpose tier ─────────────────────────────────────
rpt3 = analyze_preset("GP_DDR5_Compatible")
print(f"GP Ω_chip   = {rpt3.omega_chip:.4f}")
print(f"Layer count = {len(rpt3.layer_details)}")   # 10

# ── 4. Portfolio screening ──────────────────────────────────────
results = {name: analyze_preset(name) for name in list_presets()}
ranked  = sorted(results.items(), key=lambda x: x[1].omega_chip, reverse=True)
for name, r in ranked:
    print(f"{r.omega_chip:.3f}  {r.verdict.value:25s}  {name}")

# ── 5. Integration signals ──────────────────────────────────────
sig     = rpt.to_edge_signal()   # flat dict (float/bool/str/int values only)
summary = rpt.to_summary_dict()  # JSON-serializable dict
```

---

## 11. 8 Presets

### Accelerator Tier — Dedicated Memory Accelerator (5 presets)

| Preset | Scenario | Expected Ω | Verdict |
|---|---|---|---|
| `FPGA_STM_Prototype` | STM-only FPGA prototype — early validation | ~0.15 | concept_only |
| `EdgeAI_Memory_Coprocessor` | Edge AI memory coprocessor (14nm, near production) | ~0.72 | silicon_candidate |
| `Robot_Memory_SoC` | Robot/android memory SoC (7nm, idealized target) | ~0.80 | silicon_candidate |
| `Concept_BrainChip` | Early concept brain chip — software logic only | ~0.08 | concept_only |
| `Spaceship_MemoryUnit` | Spacecraft memory unit (65nm, extreme temp/radiation) | ~0.50 | rtl_ready |

> `Robot_Memory_SoC`'s ~0.80 is a **target benchmark** with all parameters ideally set.
> Real robot SoC projects typically start in the 0.15–0.30 range.

### General-Purpose Tier — Standard Memory (2 presets)

| Preset | Scenario | Expected Ω | Verdict |
|---|---|---|---|
| `GP_DDR5_Compatible` | DDR5 JEDEC-compliant general-purpose memory | ~0.75 | silicon_candidate |
| `GP_CXL_Datacenter` | CXL 3.0 datacenter memory expansion module | ~0.65 | rtl_ready |

### Hybrid Tier — Mixed Design (1 preset)

| Preset | Scenario | Expected Ω | Verdict |
|---|---|---|---|
| `Hybrid_SmartMemory_Module` | STM policy engine + DDR5 interface hybrid | ~0.60 | rtl_ready |

All presets are **hypothetical scenarios** unrelated to any specific chip product.

---

## 12. CLI Usage

```bash
# List available presets
memory-chip-readiness list-presets

# Analyze a preset (text report)
memory-chip-readiness analyze EdgeAI_Memory_Coprocessor

# JSON output
memory-chip-readiness analyze Robot_Memory_SoC --json

# Edge AI signal output
memory-chip-readiness analyze Spaceship_MemoryUnit --edge

# Gate test with tier override
memory-chip-readiness gate-test FPGA_STM_Prototype --tier general_purpose --json

# GP-specific presets
memory-chip-readiness analyze GP_DDR5_Compatible --json
memory-chip-readiness analyze Hybrid_SmartMemory_Module
```

---

## 13. End-to-End Workflow

```
◀──── upstream (research) ─────────────────────────── downstream (silicon) ────►

[R&D Readiness] → [Memory Chip Readiness] → [RTL] → [FPGA] → [ASIC Tapeout]
  · hypothesis      · 10-layer Ω_chip           Verilog   prototype   foundry
  · reproducibility · DesignTier selection       VHDL      validation  fab
  · IP/FTO          · Gate pass/fail

──────────────────────────────────────────────────────────────────────────────

Detailed flow:

 [1] Complete STM / LTM / Consolidation software logic
      │
      ▼
 [2] Run Memory Chip Readiness analysis (select DesignTier)
      │   ├─ Accelerator: 6-layer evaluation
      │   ├─ General-Purpose: 10-layer evaluation
      │   └─ Hybrid: 10-layer evaluation (balanced weights)
      │
      ▼
 [3] Check verdict and improve bottleneck layer
      │   concept_only  → start microarchitecture design
      │   arch_defined  → write RTL skeleton
      │   rtl_ready     → simulation + coverage improvement
      │   silicon_cand  → clear gate blockers
      │   tapeout_ready → submit to foundry
      │
      ▼
 [4] Pass Fabrication Gate
      │   clear blockers → ready_for_tapeout = True
      │   check estimated_tapeout_months
      │
      ▼
 [5] Chip Bridge signals → ecosystem engine integration
      │   NPU / HBM / HBF / Chip Signoff
      │
      ▼
 [6] Write Verilog/VHDL RTL → EDA toolchain (Synopsys/Cadence)
      │
      ▼
 [7] FPGA prototype → measure latency/power
      │
      ▼
 [8] ASIC tapeout → foundry (TSMC / Samsung / GF)
```

---

## 14. Extension & Use Cases

### 14.1 Agent & Ecosystem Integration

```python
rpt = analyze_preset("EdgeAI_Memory_Coprocessor")

# RockLEE IndustrialSignal format
sig = rpt.to_edge_signal()
# → {"omega_chip": 0.72, "verdict": "silicon_candidate",
#    "l01_stm_microarch": 0.81, "l02_ltm_search_accel": 0.68, ...}

# JSON summary for Streamlit / React dashboard
summary = rpt.to_summary_dict()
```

### 14.2 Portfolio Screening

```python
results    = {n: analyze_preset(n) for n in list_presets()}
ranked     = sorted(results.items(), key=lambda x: x[1].omega_chip, reverse=True)

from collections import Counter
bottlenecks = Counter(r.key_bottleneck for r in results.values())
print(bottlenecks)   # identify most common blockers
```

### 14.3 What-If Simulation

```python
base     = analyze_preset("FPGA_STM_Prototype")
improved = analyze(
    ltm=LTMSearchAccelProfile(top_k_hw=True, similarity_engine_type="cosine",
                               rtl_coverage_pct=60),
)
print(f"Before: {base.omega_chip:.4f}")
print(f"After:  {improved.omega_chip:.4f}")
print(f"Delta:  +{improved.omega_chip - base.omega_chip:.4f}")
```

### 14.4 Dashboard / Reports

`to_summary_dict()` JSON can be passed directly to Streamlit, React, or Grafana.
Layer scores → radar chart; verdict history → timeline visualization.

---

## 15. Current Limitations

| Item | Description |
|---|---|
| Model simplification | Layer scores are linear heuristics; do not replace EDA simulation or signoff |
| No RTL generation | Does not generate Verilog/VHDL — readiness assessment only |
| No EDA integration | No direct integration with Synopsys/Cadence/Mentor EDA tools |
| Uncalibrated | Weights not calibrated against real tapeout data |
| Memory subsystem only | Evaluates memory subsystem, not full CPU/GPU/NPU SoC |
| Limited presets | 8 presets do not cover the full diversity of chip design scenarios |
| Simple PPA estimation | Area/power/delay estimation is a simple heuristic based on process node maturity |

---

## 16. Roadmap

```
Phase 1 (short-term — 3–6 months)
  ├─ Expand presets: MCU memory, IoT memory, automotive (ISO 26262)
  ├─ STM RTL skeleton generator: auto-generate Verilog templates
  └─ Streamlit dashboard: 10-layer radar chart + verdict history

Phase 2 (mid-term — 6–18 months)
  ├─ LTM Similarity Engine RTL: dot-product accelerator in Verilog
  ├─ FPGA prototype workflow: Vivado / Quartus integration
  ├─ EDA adapter: Synopsys DC / Innovus area·power feedback
  └─ 00_BRAIN ecosystem: NPU / HBM / HBF formal adapters

Phase 3 (long-term — 18+ months)
  ├─ Calibrate weights against real tapeout data
  ├─ ML-based PPA estimation (area · power · delay prediction)
  ├─ Memory SoC full stack: CPU + Memory Accelerator integrated evaluation
  └─ GDS II / OASIS layout-level verification integration
```

---

## 17. Integrity & Blockchain Signature

Memory Chip Readiness Foundation tracks code integrity with a **SHA-256 manifest**.

```bash
# Regenerate signature (after file changes)
python scripts/generate_signature.py

# Verify (run before any release)
python scripts/generate_signature.py --verify
```

```
SIGNATURE.sha256              ← SHA-256 hashes for 22 files
MEMORYCHIP_BLOCKCHAIN_LOG.md  ← per-release change history + integrity record
BLOCKCHAIN_INFO.md            ← signature policy documentation
```

Current signature state:

```
v0.2.0  22 files verified  ✓  (Block #3 — 2026-04-15 final pre-release review)
```

Release history → [MEMORYCHIP_BLOCKCHAIN_LOG.md](MEMORYCHIP_BLOCKCHAIN_LOG.md)
Signature policy → [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)

---

## 18. Package Structure

```
memoryCHIPs/
├── LICENSE
├── pyproject.toml                  memory-chip-readiness 0.2.0, stdlib-only
├── .gitignore
├── .github/workflows/ci.yml       Python 3.10 · 3.12 CI
├── README.md                      Korean canonical (정본)
├── README_EN.md                   English companion (this file)
├── CONCEPT.md / CONCEPT_EN.md     Design philosophy & deep-dive concepts
├── CHANGELOG.md / CHANGELOG_EN.md Version history
├── MEMORYCHIP_BLOCKCHAIN_LOG.md   Integrity blockchain log
├── BLOCKCHAIN_INFO.md             Signature policy
├── SIGNATURE.sha256               SHA-256 manifest (22 files)
├── scripts/
│   └── generate_signature.py      Signature generation & verification
└── memory_chip_readiness/
    ├── py.typed                   PEP 561 type marker
    ├── __init__.py                Public API
    ├── __main__.py                python -m entry point
    ├── version.py                 __version__ = "0.2.0"
    ├── contracts.py               All dataclass contracts (I/O · enum · DesignTier)
    │
    ├── [Core Layers — all tiers]
    ├── stm_microarch.py            L01 STM microarchitecture evaluation
    ├── ltm_search_accel.py         L02 LTM search accelerator evaluation
    ├── consolidation_scheduler.py  L03 consolidation scheduler evaluation
    ├── physical_memory.py          L04 physical memory layer evaluation
    ├── host_interface.py           L05 host interface & DMA evaluation
    ├── process_area_power.py       L06 process / area / power / test evaluation
    │
    ├── [GP Extension Layers — GP & Hybrid tiers only]
    ├── standard_interface.py       L07 standard memory interface (JEDEC/CXL)
    ├── cache_coherency.py          L08 cache coherency & MMU
    ├── multi_tenant.py             L09 multi-tenant & scalability
    ├── ecosystem_compat.py         L10 OS & ecosystem compatibility
    │
    ├── foundation.py               Orchestrator (DesignTier-based 10-layer engine)
    ├── presets.py                  8 presets (Accel 5 + GP 2 + Hybrid 1)
    ├── cli.py                      CLI entry point (--tier support)
    └── tests/
        ├── __init__.py
        └── test_memory_chip.py    63 tests
                                    (contracts · core · GP layers · foundation ·
                                     presets · serialization · CLI · weight invariants)
```

---

## 19. License

MIT — see [LICENSE](LICENSE).

Copyright © 2026 00_BRAIN / GNJz

---

**Memory Chip Readiness Foundation**
*"The readiness screening engine connecting memory dreams to silicon reality."*

> Part of the 00_BRAIN ecosystem — [R&D Readiness](../RnD_Readiness_Foundation) · [PHAMacy](../PHAMacy) · [SmartFarm](../SmartFarm_Readiness_Foundation)
