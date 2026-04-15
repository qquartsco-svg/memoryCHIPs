> **English.** Korean (정본): [CONCEPT.md](CONCEPT.md)

# Memory Chip Readiness Foundation — Design Philosophy

## Core Question

> "Can memory logic running in software be made to run on silicon?"

This engine measures the **readiness** for that translation.

---

## Background: Why a Memory Chip?

The short-term, long-term, and consolidation memory systems designed in 00_BRAIN
are **cognitive memory systems** intended for agents, robots, androids, spaceships, and similar platforms.

While they work purely in software, **hardware acceleration** becomes essential for:

- **Ultra-low latency**: Robot real-time reflexes (μs-level recall)
- **Low power**: Edge/IoT/spacecraft (mW-class power budgets)
- **Bandwidth**: Searching tens of thousands of vectors per second in LTM
- **Durability**: Power failure, radiation, extreme temperatures

This engine reads the **current position** and **bottleneck** on the path
from "software memory" to "silicon memory" as numeric scores.

---

## Recommended Architecture: Memory Accelerator Chip

Rather than a general-purpose CPU, the target is a **Memory Coprocessor (Accelerator)**:

- **Host CPU/NPU** handles language processing, agent logic, inference
- **Memory Accelerator Chip** handles STM policy, recall, similarity search, consolidation
- **External Persistent Storage** (Flash/SSD/MRAM) holds long-term data

---

## 6-Layer Model

| Layer | What it measures |
|---|---|
| L01 STM Microarchitecture | Slot SRAM, decay/TTL/eviction HW blocks, cycle budget |
| L02 LTM Search Accelerator | Similarity engine, top-k, persistent store interface |
| L03 Consolidation Scheduler | Eligibility FSM, DMA, merge, pipeline |
| L04 Physical Memory Layer | SRAM/Flash/MRAM selection, capacity, reliability, endurance |
| L05 Host Interface & DMA | Bus protocol, register map, driver API, bandwidth |
| L06 Process, Area, Power, Test | Process node, area/power feasibility, DFT, signoff, yield |

---

## Position in 00_BRAIN Ecosystem

```
R&D Readiness (idea → evidence)
     │
Memory Logic (STM / LTM / Consolidation)  ← behavioural spec
     │
Memory Chip Readiness  ← this engine (translation readiness)
     │
     ├── NPU Architecture Foundation
     ├── HBM System
     ├── HBF Readiness
     ├── Chip Signoff / Logic Die Stack
     │
     └── Foundry Ramp → ASIC tape-out
```

---

## Conclusion

Memory Chip Readiness Foundation is a **dashboard** that reads
where memory software logic currently stands on its journey to silicon.

It does not generate RTL or run EDA tools, but it tells you
**how ready you are and what the bottleneck is** — in numbers.

When those numbers are high enough, the next step is **real Verilog/VHDL → FPGA → ASIC**.
