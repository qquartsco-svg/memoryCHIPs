"""Memory Chip Readiness Foundation — contracts (data-classes & enums).

10-Layer Ω_chip scoring:
  Core (L01-L06): STM/LTM/Consolidation 메모리 로직 → 실리콘 준비도.
  GP Extension (L07-L10): 범용 메모리 표준 호환성 준비도.

DesignTier로 accelerator(전문) / general_purpose(범용) / hybrid 모드 전환.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# ── Enums ────────────────────────────────────────────────────────


class DesignTier(Enum):
    """설계 티어 — 가중치 세트를 결정한다."""

    accelerator = "accelerator"
    general_purpose = "general_purpose"
    hybrid = "hybrid"


class ChipVerdict(Enum):
    """Ω_chip 기반 궤적 판정."""

    concept_only = "concept_only"
    architecture_defined = "architecture_defined"
    rtl_ready = "rtl_ready"
    silicon_candidate = "silicon_candidate"
    tapeout_ready = "tapeout_ready"


class MemoryTech(Enum):
    """물리 메모리 기술 선택지."""

    sram = "sram"
    edram = "edram"
    mram = "mram"
    reram = "reram"
    nand_flash = "nand_flash"
    hbm = "hbm"
    dram = "dram"


class ProcessNode(Enum):
    """공정 노드."""

    nm180 = "180nm"
    nm65 = "65nm"
    nm28 = "28nm"
    nm14 = "14nm"
    nm7 = "7nm"
    nm5 = "5nm"
    nm3 = "3nm"


class BusProtocol(Enum):
    """호스트 버스 프로토콜."""

    axi4 = "axi4"
    ahb = "ahb"
    apb = "apb"
    wishbone = "wishbone"
    custom = "custom"


class MemoryStandard(Enum):
    """표준 메모리 인터페이스 프로토콜."""

    ddr4 = "ddr4"
    ddr5 = "ddr5"
    lpddr5 = "lpddr5"
    hbm2e = "hbm2e"
    hbm3 = "hbm3"
    cxl_mem = "cxl_mem"
    none = "none"


# ── L01  STM Microarchitecture ───────────────────────────────────


@dataclass
class STMMicroarchProfile:
    """L01: 단기 메모리 마이크로아키텍처 준비도 입력."""

    max_slots: int = 64
    slot_width_bits: int = 256
    eviction_policy_defined: bool = False
    decay_engine_fsm: bool = False
    ttl_timer_hw: bool = False
    query_filter_block: bool = False
    namespace_support: bool = False
    priority_queue_hw: bool = False
    strength_bits: int = 8
    cycle_budget_put: int = 0
    cycle_budget_get: int = 0
    sram_compiler_validated: bool = False
    rtl_coverage_pct: float = 0.0


# ── L02  LTM Search Accelerator ─────────────────────────────────


@dataclass
class LTMSearchAccelProfile:
    """L02: 장기 메모리 검색 가속기 준비도 입력."""

    vector_dim: int = 128
    similarity_engine_type: str = "dot_product"
    top_k_hw: bool = False
    max_wells: int = 1024
    external_storage_interface: bool = False
    episodic_log_engine: bool = False
    cam_lookup_support: bool = False
    fixed_point_precision: str = "fp16"
    index_cache_kb: int = 0
    search_latency_target_ns: int = 0
    rtl_coverage_pct: float = 0.0


# ── L03  Consolidation Scheduler ─────────────────────────────────


@dataclass
class ConsolidationSchedulerProfile:
    """L03: 통합(컨솔리데이션) 스케줄러 준비도 입력."""

    eligibility_fsm: bool = False
    dma_controller: bool = False
    strength_threshold_hw: bool = False
    compression_engine: bool = False
    merge_arbiter: bool = False
    interrupt_driven: bool = False
    max_consolidation_per_cycle: int = 1
    pipeline_stages: int = 0
    power_gating_support: bool = False
    rtl_coverage_pct: float = 0.0


# ── L04  Physical Memory Layer ───────────────────────────────────


@dataclass
class PhysicalMemoryProfile:
    """L04: 물리 메모리 계층 매핑 준비도 입력."""

    stm_tech: MemoryTech = MemoryTech.sram
    ltm_tech: MemoryTech = MemoryTech.nand_flash
    stm_capacity_kb: int = 0
    ltm_capacity_mb: int = 0
    ecc_support: bool = False
    wear_leveling: bool = False
    retention_hours: float = 0.0
    endurance_cycles: int = 0
    thermal_guard: bool = False
    memory_bist: bool = False
    tech_validated: bool = False


# ── L05  Host Interface & DMA ────────────────────────────────────


@dataclass
class HostInterfaceProfile:
    """L05: 호스트 인터페이스·DMA·버스 설계 준비도 입력."""

    bus_protocol: BusProtocol = BusProtocol.axi4
    bus_width_bits: int = 64
    dma_channels: int = 1
    interrupt_lines: int = 1
    register_map_defined: bool = False
    driver_api_spec: bool = False
    bandwidth_gbps: float = 0.0
    latency_target_ns: int = 0
    firmware_hal_ready: bool = False
    protocol_compliance_tested: bool = False


# ── L06  Process, Area, Power, Test ──────────────────────────────


@dataclass
class ProcessAreaPowerProfile:
    """L06: 공정·면적·전력·테스트 타당성 입력."""

    process_node: ProcessNode = ProcessNode.nm28
    target_area_mm2: float = 0.0
    estimated_area_mm2: float = 0.0
    target_power_mw: float = 0.0
    estimated_power_mw: float = 0.0
    clock_freq_mhz: float = 0.0
    dft_scan_chain: bool = False
    dft_mbist: bool = False
    signoff_drc_clean: bool = False
    signoff_lvs_clean: bool = False
    foundry_pdk_available: bool = False
    yield_estimate_pct: float = 0.0
    package_type: str = "qfn"


# ── L07  Standard Memory Interface (GP) ─────────────────────────


@dataclass
class StandardInterfaceProfile:
    """L07: DDR/HBM/CXL 등 표준 메모리 인터페이스 호환 준비도."""

    memory_standard: MemoryStandard = MemoryStandard.none
    jedec_compliance_level: float = 0.0
    channel_count: int = 1
    data_rate_mtps: int = 0
    burst_length: int = 8
    phy_ip_validated: bool = False
    timing_margin_pct: float = 0.0
    signal_integrity_sim: bool = False
    init_sequence_defined: bool = False
    refresh_logic: bool = False
    rtl_coverage_pct: float = 0.0


# ── L08  Cache Coherency & MMU (GP) ─────────────────────────────


@dataclass
class CacheCoherencyProfile:
    """L08: 캐시 일관성·가상 메모리·MMU 지원 준비도."""

    coherency_protocol: str = "none"
    snoop_filter: bool = False
    tlb_entries: int = 0
    page_size_kb: int = 4
    virtual_address_bits: int = 0
    mmu_hw_walker: bool = False
    cache_line_bytes: int = 64
    multi_level_cache: bool = False
    atomic_ops_support: bool = False
    rtl_coverage_pct: float = 0.0


# ── L09  Multi-Tenant & Scalability (GP) ────────────────────────


@dataclass
class MultiTenantProfile:
    """L09: 다중 프로세스 격리·확장성 준비도."""

    memory_protection_unit: bool = False
    process_isolation_hw: bool = False
    max_tenants: int = 1
    qos_arbiter: bool = False
    capacity_scalable: bool = False
    die_stacking_support: bool = False
    channel_bonding: bool = False
    bandwidth_partitioning: bool = False
    error_containment: bool = False
    rtl_coverage_pct: float = 0.0


# ── L10  OS & Ecosystem Compatibility (GP) ──────────────────────


@dataclass
class EcosystemCompatProfile:
    """L10: OS·커널·소프트웨어 생태계 호환 준비도."""

    kernel_driver_available: bool = False
    linux_support: bool = False
    rtos_support: bool = False
    memory_allocator_compat: bool = False
    numa_aware: bool = False
    hotplug_support: bool = False
    ras_features: bool = False
    monitoring_counters: bool = False
    documentation_complete: bool = False
    sdk_available: bool = False


# ── Shared result ────────────────────────────────────────────────


@dataclass
class LayerResult:
    """개별 레이어 평가 결과."""

    layer: str
    omega: float
    evidence: dict[str, Any] = field(default_factory=dict)
    notes: str = ""


# ── Fabrication Readiness Gate ───────────────────────────────────


@dataclass
class FabricationGate:
    """Ω 점수와 별도로 물리 생산 조건 충족 여부."""

    ready_for_tapeout: bool = False
    estimated_tapeout_months: int = 0
    blockers: list[str] = field(default_factory=list)


# ── Chip Bridge Signal ───────────────────────────────────────────


@dataclass
class ChipBridgeSignal:
    """기존 00_BRAIN 칩 엔진들과 연동할 브리지 신호."""

    npu_omega_hint: float = 0.0
    hbm_omega_hint: float = 0.0
    hbf_omega_hint: float = 0.0
    foundry_gate_status: str = "unknown"
    notes: str = ""


# ── Main Report ──────────────────────────────────────────────────


@dataclass
class MemoryChipReadinessReport:
    """통합 보고서 — Memory Chip Readiness Foundation."""

    # tier
    design_tier: DesignTier = DesignTier.accelerator

    # composite
    omega_chip: float = 0.0
    verdict: ChipVerdict = ChipVerdict.concept_only

    # per-layer
    layer_details: list[LayerResult] = field(default_factory=list)
    key_bottleneck: str = ""

    # core layer omegas (L01-L06)
    omega_stm_microarch: float = 0.0
    omega_ltm_search: float = 0.0
    omega_consolidation: float = 0.0
    omega_physical_memory: float = 0.0
    omega_host_interface: float = 0.0
    omega_process_area_power: float = 0.0

    # GP extension omegas (L07-L10)
    omega_standard_interface: float = 0.0
    omega_cache_coherency: float = 0.0
    omega_multi_tenant: float = 0.0
    omega_ecosystem_compat: float = 0.0

    # gate
    fabrication_gate: FabricationGate = field(default_factory=FabricationGate)

    # bridge
    chip_bridge: ChipBridgeSignal = field(default_factory=ChipBridgeSignal)

    def to_summary_dict(self) -> dict[str, Any]:
        """JSON-serialisable summary for dashboards & agents."""
        return {
            "design_tier": self.design_tier.value,
            "omega_chip": round(self.omega_chip, 4),
            "verdict": self.verdict.value,
            "key_bottleneck": self.key_bottleneck,
            "fabrication_gate": {
                "ready": self.fabrication_gate.ready_for_tapeout,
                "months": self.fabrication_gate.estimated_tapeout_months,
                "blockers": self.fabrication_gate.blockers,
            },
            "layers": {
                lr.layer: {"omega": round(lr.omega, 4), "notes": lr.notes}
                for lr in self.layer_details
            },
            "chip_bridge": {
                "npu_omega_hint": self.chip_bridge.npu_omega_hint,
                "hbm_omega_hint": self.chip_bridge.hbm_omega_hint,
                "hbf_omega_hint": self.chip_bridge.hbf_omega_hint,
                "foundry_gate": self.chip_bridge.foundry_gate_status,
            },
        }

    def to_edge_signal(self) -> dict[str, float | bool | str]:
        """경량 엣지/MCU/WASM 런타임용 flat signal."""
        sig: dict[str, float | bool | str] = {
            "design_tier": self.design_tier.value,
            "omega_chip": self.omega_chip,
            "verdict": self.verdict.value,
            "bottleneck": self.key_bottleneck,
            "gate_ready": self.fabrication_gate.ready_for_tapeout,
            "blocker_count": len(self.fabrication_gate.blockers),
            "l01_stm_microarch": self.omega_stm_microarch,
            "l02_ltm_search": self.omega_ltm_search,
            "l03_consolidation": self.omega_consolidation,
            "l04_physical_memory": self.omega_physical_memory,
            "l05_host_interface": self.omega_host_interface,
            "l06_process_area_power": self.omega_process_area_power,
        }
        if self.design_tier != DesignTier.accelerator:
            sig["l07_standard_interface"] = self.omega_standard_interface
            sig["l08_cache_coherency"] = self.omega_cache_coherency
            sig["l09_multi_tenant"] = self.omega_multi_tenant
            sig["l10_ecosystem_compat"] = self.omega_ecosystem_compat
        return sig
