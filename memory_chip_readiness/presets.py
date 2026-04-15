"""Memory Chip Readiness Foundation — preset scenarios (8종).

각 프리셋은 가상 설계 시나리오이며 실제 특정 칩 제품과 무관하다.
Accelerator(전문) 5종 + General-Purpose(범용) 2종 + Hybrid 1종.
"""

from __future__ import annotations

from typing import Any

from .contracts import (
    BusProtocol,
    CacheCoherencyProfile,
    ConsolidationSchedulerProfile,
    DesignTier,
    EcosystemCompatProfile,
    HostInterfaceProfile,
    LTMSearchAccelProfile,
    MemoryStandard,
    MemoryTech,
    MultiTenantProfile,
    PhysicalMemoryProfile,
    ProcessAreaPowerProfile,
    ProcessNode,
    StandardInterfaceProfile,
    STMMicroarchProfile,
)
from .foundation import MemoryChipReadinessReport, analyze

_REGISTRY: dict[str, dict[str, Any]] = {}


def _register(name: str, **kwargs: Any) -> None:
    _REGISTRY[name] = kwargs


def list_presets() -> list[str]:
    """등록된 프리셋 이름 목록."""
    return sorted(_REGISTRY.keys())


def analyze_preset(name: str) -> MemoryChipReadinessReport:
    """프리셋 이름으로 즉시 분석 실행."""
    if name not in _REGISTRY:
        raise KeyError(f"Unknown preset: {name!r}. Available: {list_presets()}")
    return analyze(**_REGISTRY[name])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ACCELERATOR TIER (전문 메모리 가속기) — 5종
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_register(
    "FPGA_STM_Prototype",
    tier=DesignTier.accelerator,
    stm=STMMicroarchProfile(
        max_slots=32, slot_width_bits=128,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        strength_bits=8, cycle_budget_put=4, cycle_budget_get=2,
        rtl_coverage_pct=30.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=64, similarity_engine_type="dot_product",
        max_wells=256,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, rtl_coverage_pct=10.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, stm_capacity_kb=4,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=32, dma_channels=1,
    ),
    process=ProcessAreaPowerProfile(process_node=ProcessNode.nm28),
)

_register(
    "EdgeAI_Memory_Coprocessor",
    tier=DesignTier.accelerator,
    stm=STMMicroarchProfile(
        max_slots=64, slot_width_bits=256,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        namespace_support=True, priority_queue_hw=True,
        strength_bits=16, cycle_budget_put=3, cycle_budget_get=2,
        sram_compiler_validated=True, rtl_coverage_pct=65.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=128, similarity_engine_type="dot_product",
        top_k_hw=True, max_wells=2048,
        external_storage_interface=True, episodic_log_engine=True,
        fixed_point_precision="int8", index_cache_kb=64,
        search_latency_target_ns=200, rtl_coverage_pct=45.0,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, dma_controller=True,
        strength_threshold_hw=True, merge_arbiter=True,
        interrupt_driven=True, max_consolidation_per_cycle=2,
        pipeline_stages=3, rtl_coverage_pct=40.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.nand_flash,
        stm_capacity_kb=32, ltm_capacity_mb=64,
        ecc_support=True, wear_leveling=True,
        retention_hours=8760, endurance_cycles=100_000,
        thermal_guard=True, memory_bist=True, tech_validated=True,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=64,
        dma_channels=2, interrupt_lines=2,
        register_map_defined=True, driver_api_spec=True,
        bandwidth_gbps=3.2, latency_target_ns=100,
        firmware_hal_ready=True,
    ),
    process=ProcessAreaPowerProfile(
        process_node=ProcessNode.nm14,
        target_area_mm2=4.0, estimated_area_mm2=3.8,
        target_power_mw=200, estimated_power_mw=180,
        clock_freq_mhz=500,
        dft_scan_chain=True, dft_mbist=True,
        signoff_drc_clean=True, signoff_lvs_clean=True,
        foundry_pdk_available=True, yield_estimate_pct=85.0,
        package_type="bga",
    ),
)

_register(
    "Robot_Memory_SoC",
    tier=DesignTier.accelerator,
    stm=STMMicroarchProfile(
        max_slots=128, slot_width_bits=512,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        namespace_support=True, priority_queue_hw=True,
        strength_bits=16, cycle_budget_put=2, cycle_budget_get=1,
        sram_compiler_validated=True, rtl_coverage_pct=80.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=256, similarity_engine_type="cosine",
        top_k_hw=True, max_wells=8192,
        external_storage_interface=True, episodic_log_engine=True,
        cam_lookup_support=True, fixed_point_precision="fp16",
        index_cache_kb=256, search_latency_target_ns=80,
        rtl_coverage_pct=60.0,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, dma_controller=True,
        strength_threshold_hw=True, compression_engine=True,
        merge_arbiter=True, interrupt_driven=True,
        max_consolidation_per_cycle=4, pipeline_stages=5,
        power_gating_support=True, rtl_coverage_pct=55.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.mram,
        stm_capacity_kb=64, ltm_capacity_mb=256,
        ecc_support=True, wear_leveling=True,
        retention_hours=87600, endurance_cycles=10_000_000,
        thermal_guard=True, memory_bist=True, tech_validated=True,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=128,
        dma_channels=4, interrupt_lines=4,
        register_map_defined=True, driver_api_spec=True,
        bandwidth_gbps=8.0, latency_target_ns=50,
        firmware_hal_ready=True, protocol_compliance_tested=True,
    ),
    process=ProcessAreaPowerProfile(
        process_node=ProcessNode.nm7,
        target_area_mm2=8.0, estimated_area_mm2=7.5,
        target_power_mw=500, estimated_power_mw=480,
        clock_freq_mhz=1000,
        dft_scan_chain=True, dft_mbist=True,
        signoff_drc_clean=True, signoff_lvs_clean=True,
        foundry_pdk_available=True, yield_estimate_pct=78.0,
        package_type="fcbga",
    ),
)

_register(
    "Concept_BrainChip",
    tier=DesignTier.accelerator,
    stm=STMMicroarchProfile(
        max_slots=256, slot_width_bits=1024,
        eviction_policy_defined=True, strength_bits=8,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=512, similarity_engine_type="cosine", max_wells=16384,
    ),
    consolidation=ConsolidationSchedulerProfile(eligibility_fsm=True),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.hbm,
    ),
)

_register(
    "Spaceship_MemoryUnit",
    tier=DesignTier.accelerator,
    stm=STMMicroarchProfile(
        max_slots=32, slot_width_bits=128,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        namespace_support=True, strength_bits=8,
        cycle_budget_put=6, cycle_budget_get=4,
        sram_compiler_validated=True, rtl_coverage_pct=50.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=64, similarity_engine_type="dot_product",
        top_k_hw=True, max_wells=512,
        external_storage_interface=True, episodic_log_engine=True,
        fixed_point_precision="int8", index_cache_kb=16,
        search_latency_target_ns=500, rtl_coverage_pct=35.0,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, dma_controller=True,
        strength_threshold_hw=True, merge_arbiter=True,
        power_gating_support=True, max_consolidation_per_cycle=1,
        pipeline_stages=2, rtl_coverage_pct=30.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.mram,
        stm_capacity_kb=4, ltm_capacity_mb=16,
        ecc_support=True, wear_leveling=True,
        retention_hours=87600, endurance_cycles=100_000_000,
        thermal_guard=True, memory_bist=True, tech_validated=True,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=32,
        dma_channels=1, interrupt_lines=2,
        register_map_defined=True, driver_api_spec=True,
        bandwidth_gbps=1.6, latency_target_ns=200,
        firmware_hal_ready=True,
    ),
    process=ProcessAreaPowerProfile(
        process_node=ProcessNode.nm65,
        target_area_mm2=6.0, estimated_area_mm2=5.5,
        target_power_mw=100, estimated_power_mw=85,
        clock_freq_mhz=200,
        dft_scan_chain=True, dft_mbist=True,
        signoff_drc_clean=True, signoff_lvs_clean=True,
        foundry_pdk_available=True, yield_estimate_pct=92.0,
        package_type="cqfp",
    ),
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GENERAL-PURPOSE TIER (범용 메모리) — 2종
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_register(
    "GP_DDR5_Compatible",
    tier=DesignTier.general_purpose,
    stm=STMMicroarchProfile(
        max_slots=64, slot_width_bits=256,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        namespace_support=True, priority_queue_hw=True,
        strength_bits=16, cycle_budget_put=2, cycle_budget_get=1,
        sram_compiler_validated=True, rtl_coverage_pct=75.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=128, similarity_engine_type="dot_product",
        top_k_hw=True, max_wells=4096,
        external_storage_interface=True, episodic_log_engine=True,
        cam_lookup_support=True, fixed_point_precision="int8",
        index_cache_kb=128, search_latency_target_ns=100,
        rtl_coverage_pct=55.0,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, dma_controller=True,
        strength_threshold_hw=True, merge_arbiter=True,
        interrupt_driven=True, max_consolidation_per_cycle=4,
        pipeline_stages=4, rtl_coverage_pct=50.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.dram,
        stm_capacity_kb=64, ltm_capacity_mb=1024,
        ecc_support=True, wear_leveling=False,
        retention_hours=87600, endurance_cycles=100_000_000,
        thermal_guard=True, memory_bist=True, tech_validated=True,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=128,
        dma_channels=4, interrupt_lines=4,
        register_map_defined=True, driver_api_spec=True,
        bandwidth_gbps=51.2, latency_target_ns=20,
        firmware_hal_ready=True, protocol_compliance_tested=True,
    ),
    process=ProcessAreaPowerProfile(
        process_node=ProcessNode.nm7,
        target_area_mm2=12.0, estimated_area_mm2=11.0,
        target_power_mw=800, estimated_power_mw=750,
        clock_freq_mhz=2400,
        dft_scan_chain=True, dft_mbist=True,
        signoff_drc_clean=True, signoff_lvs_clean=True,
        foundry_pdk_available=True, yield_estimate_pct=75.0,
        package_type="fcbga",
    ),
    standard=StandardInterfaceProfile(
        memory_standard=MemoryStandard.ddr5,
        jedec_compliance_level=0.85,
        channel_count=2, data_rate_mtps=6400, burst_length=16,
        phy_ip_validated=True, timing_margin_pct=12.0,
        signal_integrity_sim=True, init_sequence_defined=True,
        refresh_logic=True, rtl_coverage_pct=60.0,
    ),
    cache=CacheCoherencyProfile(
        coherency_protocol="mesi",
        snoop_filter=True, tlb_entries=128,
        page_size_kb=4, virtual_address_bits=48,
        mmu_hw_walker=True, cache_line_bytes=64,
        multi_level_cache=True, atomic_ops_support=True,
        rtl_coverage_pct=55.0,
    ),
    multi_tenant=MultiTenantProfile(
        memory_protection_unit=True, process_isolation_hw=True,
        max_tenants=8, qos_arbiter=True,
        capacity_scalable=True, die_stacking_support=False,
        channel_bonding=True, bandwidth_partitioning=True,
        error_containment=True, rtl_coverage_pct=45.0,
    ),
    ecosystem=EcosystemCompatProfile(
        kernel_driver_available=True, linux_support=True,
        rtos_support=True, memory_allocator_compat=True,
        numa_aware=True, hotplug_support=False,
        ras_features=True, monitoring_counters=True,
        documentation_complete=True, sdk_available=True,
    ),
)

_register(
    "GP_CXL_Datacenter",
    tier=DesignTier.general_purpose,
    stm=STMMicroarchProfile(
        max_slots=128, slot_width_bits=512,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        namespace_support=True, priority_queue_hw=True,
        strength_bits=16, cycle_budget_put=2, cycle_budget_get=1,
        sram_compiler_validated=True, rtl_coverage_pct=70.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=256, similarity_engine_type="cosine",
        top_k_hw=True, max_wells=16384,
        external_storage_interface=True, episodic_log_engine=True,
        cam_lookup_support=True, fixed_point_precision="fp16",
        index_cache_kb=512, search_latency_target_ns=50,
        rtl_coverage_pct=50.0,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, dma_controller=True,
        strength_threshold_hw=True, compression_engine=True,
        merge_arbiter=True, interrupt_driven=True,
        max_consolidation_per_cycle=8, pipeline_stages=6,
        power_gating_support=True, rtl_coverage_pct=45.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.hbm,
        stm_capacity_kb=128, ltm_capacity_mb=4096,
        ecc_support=True, thermal_guard=True,
        memory_bist=True, tech_validated=True,
        retention_hours=87600, endurance_cycles=100_000_000,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=256,
        dma_channels=8, interrupt_lines=8,
        register_map_defined=True, driver_api_spec=True,
        bandwidth_gbps=128.0, latency_target_ns=15,
        firmware_hal_ready=True, protocol_compliance_tested=True,
    ),
    process=ProcessAreaPowerProfile(
        process_node=ProcessNode.nm5,
        target_area_mm2=20.0, estimated_area_mm2=19.0,
        target_power_mw=2000, estimated_power_mw=1850,
        clock_freq_mhz=2000,
        dft_scan_chain=True, dft_mbist=True,
        signoff_drc_clean=True, signoff_lvs_clean=True,
        foundry_pdk_available=True, yield_estimate_pct=65.0,
        package_type="fcbga",
    ),
    standard=StandardInterfaceProfile(
        memory_standard=MemoryStandard.cxl_mem,
        jedec_compliance_level=0.75,
        channel_count=8, data_rate_mtps=8400, burst_length=16,
        phy_ip_validated=True, timing_margin_pct=10.0,
        signal_integrity_sim=True, init_sequence_defined=True,
        refresh_logic=True, rtl_coverage_pct=50.0,
    ),
    cache=CacheCoherencyProfile(
        coherency_protocol="chi",
        snoop_filter=True, tlb_entries=256,
        page_size_kb=4, virtual_address_bits=52,
        mmu_hw_walker=True, cache_line_bytes=64,
        multi_level_cache=True, atomic_ops_support=True,
        rtl_coverage_pct=45.0,
    ),
    multi_tenant=MultiTenantProfile(
        memory_protection_unit=True, process_isolation_hw=True,
        max_tenants=32, qos_arbiter=True,
        capacity_scalable=True, die_stacking_support=True,
        channel_bonding=True, bandwidth_partitioning=True,
        error_containment=True, rtl_coverage_pct=40.0,
    ),
    ecosystem=EcosystemCompatProfile(
        kernel_driver_available=True, linux_support=True,
        rtos_support=False, memory_allocator_compat=True,
        numa_aware=True, hotplug_support=True,
        ras_features=True, monitoring_counters=True,
        documentation_complete=True, sdk_available=True,
    ),
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HYBRID TIER (가속기 + 범용 호환) — 1종
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_register(
    "Hybrid_SmartMemory_Module",
    tier=DesignTier.hybrid,
    stm=STMMicroarchProfile(
        max_slots=64, slot_width_bits=256,
        eviction_policy_defined=True, decay_engine_fsm=True,
        ttl_timer_hw=True, query_filter_block=True,
        namespace_support=True, priority_queue_hw=True,
        strength_bits=16, cycle_budget_put=3, cycle_budget_get=2,
        sram_compiler_validated=True, rtl_coverage_pct=60.0,
    ),
    ltm=LTMSearchAccelProfile(
        vector_dim=128, similarity_engine_type="dot_product",
        top_k_hw=True, max_wells=4096,
        external_storage_interface=True, episodic_log_engine=True,
        fixed_point_precision="int8", index_cache_kb=64,
        search_latency_target_ns=150, rtl_coverage_pct=45.0,
    ),
    consolidation=ConsolidationSchedulerProfile(
        eligibility_fsm=True, dma_controller=True,
        strength_threshold_hw=True, merge_arbiter=True,
        interrupt_driven=True, max_consolidation_per_cycle=2,
        pipeline_stages=3, rtl_coverage_pct=40.0,
    ),
    physical=PhysicalMemoryProfile(
        stm_tech=MemoryTech.sram, ltm_tech=MemoryTech.dram,
        stm_capacity_kb=32, ltm_capacity_mb=512,
        ecc_support=True, thermal_guard=True,
        memory_bist=True, tech_validated=True,
        retention_hours=87600, endurance_cycles=100_000_000,
    ),
    host=HostInterfaceProfile(
        bus_protocol=BusProtocol.axi4, bus_width_bits=128,
        dma_channels=4, interrupt_lines=4,
        register_map_defined=True, driver_api_spec=True,
        bandwidth_gbps=25.6, latency_target_ns=30,
        firmware_hal_ready=True, protocol_compliance_tested=True,
    ),
    process=ProcessAreaPowerProfile(
        process_node=ProcessNode.nm7,
        target_area_mm2=10.0, estimated_area_mm2=9.5,
        target_power_mw=600, estimated_power_mw=550,
        clock_freq_mhz=1200,
        dft_scan_chain=True, dft_mbist=True,
        signoff_drc_clean=True, signoff_lvs_clean=True,
        foundry_pdk_available=True, yield_estimate_pct=76.0,
        package_type="fcbga",
    ),
    standard=StandardInterfaceProfile(
        memory_standard=MemoryStandard.lpddr5,
        jedec_compliance_level=0.70,
        channel_count=4, data_rate_mtps=5500, burst_length=16,
        phy_ip_validated=True, timing_margin_pct=10.0,
        signal_integrity_sim=True, init_sequence_defined=True,
        refresh_logic=True, rtl_coverage_pct=45.0,
    ),
    cache=CacheCoherencyProfile(
        coherency_protocol="amba_ace",
        snoop_filter=True, tlb_entries=64,
        page_size_kb=4, virtual_address_bits=48,
        mmu_hw_walker=True, cache_line_bytes=64,
        multi_level_cache=True, atomic_ops_support=True,
        rtl_coverage_pct=40.0,
    ),
    multi_tenant=MultiTenantProfile(
        memory_protection_unit=True, process_isolation_hw=True,
        max_tenants=4, qos_arbiter=True,
        capacity_scalable=True, bandwidth_partitioning=True,
        error_containment=True, rtl_coverage_pct=35.0,
    ),
    ecosystem=EcosystemCompatProfile(
        kernel_driver_available=True, linux_support=True,
        rtos_support=True, memory_allocator_compat=True,
        numa_aware=False, ras_features=True,
        monitoring_counters=True, documentation_complete=True,
        sdk_available=True,
    ),
)
