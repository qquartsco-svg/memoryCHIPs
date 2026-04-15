"""Memory Chip Readiness Foundation — orchestrator.

10개 레이어(Core 6 + GP Extension 4)를 DesignTier에 따라 통합하여
Ω_chip 점수·판정·게이트를 산출하는 핵심 엔진.
"""

from __future__ import annotations

from typing import Optional

from .cache_coherency import assess_cache_coherency
from .consolidation_scheduler import assess_consolidation
from .contracts import (
    CacheCoherencyProfile,
    ChipBridgeSignal,
    ChipVerdict,
    ConsolidationSchedulerProfile,
    DesignTier,
    EcosystemCompatProfile,
    FabricationGate,
    HostInterfaceProfile,
    LayerResult,
    LTMSearchAccelProfile,
    MemoryChipReadinessReport,
    MultiTenantProfile,
    PhysicalMemoryProfile,
    ProcessAreaPowerProfile,
    StandardInterfaceProfile,
    STMMicroarchProfile,
)
from .ecosystem_compat import assess_ecosystem_compat
from .host_interface import assess_host_interface
from .ltm_search_accel import assess_ltm_search
from .multi_tenant import assess_multi_tenant
from .physical_memory import assess_physical_memory
from .process_area_power import assess_process_area_power
from .standard_interface import assess_standard_interface
from .stm_microarch import assess_stm_microarch

# ── tier-based weight tables (each sums to 1.00) ────────────────

_WEIGHTS_ACCELERATOR: dict[str, float] = {
    "stm_microarch": 0.20,
    "ltm_search_accel": 0.22,
    "consolidation_scheduler": 0.13,
    "physical_memory": 0.18,
    "host_interface": 0.12,
    "process_area_power": 0.15,
}

_WEIGHTS_GENERAL_PURPOSE: dict[str, float] = {
    "stm_microarch": 0.10,
    "ltm_search_accel": 0.10,
    "consolidation_scheduler": 0.06,
    "physical_memory": 0.12,
    "host_interface": 0.08,
    "process_area_power": 0.12,
    "standard_interface": 0.16,
    "cache_coherency": 0.10,
    "multi_tenant": 0.08,
    "ecosystem_compat": 0.08,
}

_WEIGHTS_HYBRID: dict[str, float] = {
    "stm_microarch": 0.14,
    "ltm_search_accel": 0.15,
    "consolidation_scheduler": 0.08,
    "physical_memory": 0.14,
    "host_interface": 0.09,
    "process_area_power": 0.12,
    "standard_interface": 0.10,
    "cache_coherency": 0.07,
    "multi_tenant": 0.05,
    "ecosystem_compat": 0.06,
}


def _get_weights(tier: DesignTier) -> dict[str, float]:
    if tier == DesignTier.general_purpose:
        return _WEIGHTS_GENERAL_PURPOSE
    if tier == DesignTier.hybrid:
        return _WEIGHTS_HYBRID
    return _WEIGHTS_ACCELERATOR


def _verdict(omega: float) -> ChipVerdict:
    if omega >= 0.85:
        return ChipVerdict.tapeout_ready
    if omega >= 0.70:
        return ChipVerdict.silicon_candidate
    if omega >= 0.50:
        return ChipVerdict.rtl_ready
    if omega >= 0.30:
        return ChipVerdict.architecture_defined
    return ChipVerdict.concept_only


def _fabrication_gate(
    *,
    omega_chip: float,
    layers: list[LayerResult],
    pap: ProcessAreaPowerProfile,
    host: HostInterfaceProfile,
    tier: DesignTier,
) -> FabricationGate:
    """Ω 점수와 별도로 테이프아웃 물리 조건 충족 여부."""
    blockers: list[str] = []

    if omega_chip < 0.70:
        blockers.append("overall_omega_below_0.70")

    layer_map = {lr.layer: lr.omega for lr in layers}

    if layer_map.get("stm_microarch", 0) < 0.40:
        blockers.append("stm_microarch_immature")
    if layer_map.get("ltm_search_accel", 0) < 0.35:
        blockers.append("ltm_search_accel_immature")
    if layer_map.get("process_area_power", 0) < 0.40:
        blockers.append("process_signoff_incomplete")

    if not pap.foundry_pdk_available:
        blockers.append("no_foundry_pdk")
    if not pap.dft_scan_chain:
        blockers.append("no_dft_scan_chain")
    if not host.register_map_defined:
        blockers.append("no_register_map")

    # GP-specific gate conditions
    if tier != DesignTier.accelerator:
        if layer_map.get("standard_interface", 0) < 0.30:
            blockers.append("standard_interface_not_defined")
        if layer_map.get("cache_coherency", 0) < 0.20:
            blockers.append("cache_coherency_missing")

    months = 36
    if omega_chip >= 0.85:
        months = 6
    elif omega_chip >= 0.70:
        months = 12
    elif omega_chip >= 0.50:
        months = 18
    elif omega_chip >= 0.30:
        months = 24

    return FabricationGate(
        ready_for_tapeout=(len(blockers) == 0),
        estimated_tapeout_months=months,
        blockers=blockers,
    )


def _chip_bridge(
    layers: list[LayerResult],
    omega_chip: float,
) -> ChipBridgeSignal:
    """기존 칩 엔진들과 연동할 힌트 신호 생성."""
    layer_map = {lr.layer: lr.omega for lr in layers}
    ltm_omega = layer_map.get("ltm_search_accel", 0.0)
    phys_omega = layer_map.get("physical_memory", 0.0)

    return ChipBridgeSignal(
        npu_omega_hint=round(ltm_omega * 0.8 + omega_chip * 0.2, 4),
        hbm_omega_hint=round(phys_omega, 4),
        hbf_omega_hint=round(phys_omega * 0.7 + ltm_omega * 0.3, 4),
        foundry_gate_status="pass" if omega_chip >= 0.70 else "pending",
        notes="auto-generated bridge from memory-chip-readiness",
    )


def analyze(
    *,
    tier: DesignTier = DesignTier.accelerator,
    stm: Optional[STMMicroarchProfile] = None,
    ltm: Optional[LTMSearchAccelProfile] = None,
    consolidation: Optional[ConsolidationSchedulerProfile] = None,
    physical: Optional[PhysicalMemoryProfile] = None,
    host: Optional[HostInterfaceProfile] = None,
    process: Optional[ProcessAreaPowerProfile] = None,
    standard: Optional[StandardInterfaceProfile] = None,
    cache: Optional[CacheCoherencyProfile] = None,
    multi_tenant: Optional[MultiTenantProfile] = None,
    ecosystem: Optional[EcosystemCompatProfile] = None,
) -> MemoryChipReadinessReport:
    """Run memory-chip readiness analysis. Layer count depends on tier."""

    stm_p = stm or STMMicroarchProfile()
    ltm_p = ltm or LTMSearchAccelProfile()
    consol_p = consolidation or ConsolidationSchedulerProfile()
    phys_p = physical or PhysicalMemoryProfile()
    host_p = host or HostInterfaceProfile()
    proc_p = process or ProcessAreaPowerProfile()

    results: list[LayerResult] = [
        assess_stm_microarch(stm_p),
        assess_ltm_search(ltm_p),
        assess_consolidation(consol_p),
        assess_physical_memory(phys_p),
        assess_host_interface(host_p),
        assess_process_area_power(proc_p),
    ]

    # GP extension layers
    if tier != DesignTier.accelerator:
        std_p = standard or StandardInterfaceProfile()
        cache_p = cache or CacheCoherencyProfile()
        mt_p = multi_tenant or MultiTenantProfile()
        eco_p = ecosystem or EcosystemCompatProfile()

        results.extend([
            assess_standard_interface(std_p),
            assess_cache_coherency(cache_p),
            assess_multi_tenant(mt_p),
            assess_ecosystem_compat(eco_p),
        ])

    weights = _get_weights(tier)
    omega_chip = sum(
        weights.get(lr.layer, 0.0) * lr.omega for lr in results
    )
    omega_chip = max(0.0, min(1.0, omega_chip))

    bottleneck = min(results, key=lambda r: r.omega)
    verdict = _verdict(omega_chip)

    gate = _fabrication_gate(
        omega_chip=omega_chip,
        layers=results,
        pap=proc_p,
        host=host_p,
        tier=tier,
    )

    if not gate.ready_for_tapeout and verdict == ChipVerdict.tapeout_ready:
        verdict = ChipVerdict.silicon_candidate

    bridge = _chip_bridge(results, omega_chip)
    layer_omegas = {lr.layer: lr.omega for lr in results}

    return MemoryChipReadinessReport(
        design_tier=tier,
        omega_chip=round(omega_chip, 4),
        verdict=verdict,
        layer_details=results,
        key_bottleneck=bottleneck.layer,
        omega_stm_microarch=round(layer_omegas.get("stm_microarch", 0.0), 4),
        omega_ltm_search=round(layer_omegas.get("ltm_search_accel", 0.0), 4),
        omega_consolidation=round(layer_omegas.get("consolidation_scheduler", 0.0), 4),
        omega_physical_memory=round(layer_omegas.get("physical_memory", 0.0), 4),
        omega_host_interface=round(layer_omegas.get("host_interface", 0.0), 4),
        omega_process_area_power=round(layer_omegas.get("process_area_power", 0.0), 4),
        omega_standard_interface=round(layer_omegas.get("standard_interface", 0.0), 4),
        omega_cache_coherency=round(layer_omegas.get("cache_coherency", 0.0), 4),
        omega_multi_tenant=round(layer_omegas.get("multi_tenant", 0.0), 4),
        omega_ecosystem_compat=round(layer_omegas.get("ecosystem_compat", 0.0), 4),
        fabrication_gate=gate,
        chip_bridge=bridge,
    )
