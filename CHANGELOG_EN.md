> **English.** Korean (정본): [CHANGELOG.md](CHANGELOG.md)

# Changelog

## [0.2.0] — 2026-04-15

### General-Purpose Extension

- **DesignTier** introduced: `accelerator` / `general_purpose` / `hybrid` mode switching
- **4 GP Extension layers added** (L07-L10):
  - L07 Standard Memory Interface (DDR5/LPDDR5/HBM3/CXL, JEDEC compliance)
  - L08 Cache Coherency & MMU (MESI/MOESI/CHI, TLB, virtual memory)
  - L09 Multi-Tenant & Scalability (process isolation, QoS, die stacking)
  - L10 OS & Ecosystem Compatibility (kernel driver, Linux, NUMA, RAS)
- **3 tier-based weight tables** (accelerator 6-layer / GP 10-layer / hybrid 10-layer)
- **GP Fabrication Gate** extended with `standard_interface_not_defined`, `cache_coherency_missing` blockers
- **3 GP presets added**: `GP_DDR5_Compatible`, `GP_CXL_Datacenter`, `Hybrid_SmartMemory_Module`
- **CLI `--tier` option** for gate-test tier override
- **`design_tier` field** added to edge signal and summary dict
- **58 tests** (37 → 58, +21)
- Version 0.1.0 → 0.2.0

## [0.1.0] — 2026-04-15

### Initial Release

- 6-layer Ω_chip screening engine (L01-L06)
- ChipVerdict 5-band verdict, Fabrication Gate, Chip Bridge Signal
- 5 presets, CLI, Edge AI signal, JSON summary
- 37 tests, CI, SHA-256 signatures
