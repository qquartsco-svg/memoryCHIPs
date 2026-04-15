"""Memory Chip Readiness Foundation — comprehensive tests (v0.2.0)."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest

from memory_chip_readiness.contracts import (
    BusProtocol,
    CacheCoherencyProfile,
    ChipVerdict,
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
from memory_chip_readiness.foundation import analyze
from memory_chip_readiness.presets import analyze_preset, list_presets

_CWD = "/Users/jazzin/Desktop/00_BRAIN/_staging/Memory_Chip_Readiness_Foundation"


# ── Contracts ────────────────────────────────────────────────────


class TestContracts(unittest.TestCase):
    def test_stm_defaults(self) -> None:
        p = STMMicroarchProfile()
        self.assertEqual(p.max_slots, 64)

    def test_ltm_defaults(self) -> None:
        p = LTMSearchAccelProfile()
        self.assertEqual(p.vector_dim, 128)

    def test_consolidation_defaults(self) -> None:
        self.assertFalse(ConsolidationSchedulerProfile().eligibility_fsm)

    def test_physical_defaults(self) -> None:
        self.assertEqual(PhysicalMemoryProfile().stm_tech, MemoryTech.sram)

    def test_host_defaults(self) -> None:
        self.assertEqual(HostInterfaceProfile().bus_protocol, BusProtocol.axi4)

    def test_process_defaults(self) -> None:
        self.assertEqual(ProcessAreaPowerProfile().process_node, ProcessNode.nm28)

    def test_standard_defaults(self) -> None:
        self.assertEqual(StandardInterfaceProfile().memory_standard, MemoryStandard.none)

    def test_cache_defaults(self) -> None:
        self.assertEqual(CacheCoherencyProfile().coherency_protocol, "none")

    def test_multi_tenant_defaults(self) -> None:
        self.assertFalse(MultiTenantProfile().memory_protection_unit)

    def test_ecosystem_defaults(self) -> None:
        self.assertFalse(EcosystemCompatProfile().kernel_driver_available)

    def test_design_tier_values(self) -> None:
        self.assertEqual(DesignTier.accelerator.value, "accelerator")
        self.assertEqual(DesignTier.general_purpose.value, "general_purpose")
        self.assertEqual(DesignTier.hybrid.value, "hybrid")

    def test_chip_verdict_values(self) -> None:
        self.assertEqual(ChipVerdict.tapeout_ready.value, "tapeout_ready")
        self.assertEqual(ChipVerdict.concept_only.value, "concept_only")


# ── Core Layer Modules ───────────────────────────────────────────


class TestCoreLayerModules(unittest.TestCase):
    def test_stm_empty_low(self) -> None:
        from memory_chip_readiness.stm_microarch import assess_stm_microarch

        r = assess_stm_microarch(STMMicroarchProfile())
        self.assertLessEqual(r.omega, 0.3)
        self.assertEqual(r.layer, "stm_microarch")

    def test_stm_full_high(self) -> None:
        from memory_chip_readiness.stm_microarch import assess_stm_microarch

        p = STMMicroarchProfile(
            eviction_policy_defined=True, decay_engine_fsm=True,
            ttl_timer_hw=True, query_filter_block=True,
            namespace_support=True, priority_queue_hw=True,
            cycle_budget_put=2, cycle_budget_get=2,
            sram_compiler_validated=True, rtl_coverage_pct=90,
        )
        r = assess_stm_microarch(p)
        self.assertGreater(r.omega, 0.7)

    def test_ltm_empty_low(self) -> None:
        from memory_chip_readiness.ltm_search_accel import assess_ltm_search

        r = assess_ltm_search(LTMSearchAccelProfile())
        self.assertLessEqual(r.omega, 0.30)

    def test_consolidation_empty_low(self) -> None:
        from memory_chip_readiness.consolidation_scheduler import assess_consolidation

        r = assess_consolidation(ConsolidationSchedulerProfile())
        self.assertLessEqual(r.omega, 0.1)

    def test_physical_empty_very_low(self) -> None:
        """Default profile has no capacity and is unvalidated → near-zero omega."""
        from memory_chip_readiness.physical_memory import assess_physical_memory

        r = assess_physical_memory(PhysicalMemoryProfile())
        self.assertLessEqual(r.omega, 0.12)

    def test_physical_validated_high(self) -> None:
        from memory_chip_readiness.physical_memory import assess_physical_memory

        p = PhysicalMemoryProfile(
            stm_capacity_kb=32, ltm_capacity_mb=64,
            ecc_support=True, wear_leveling=True,
            thermal_guard=True, memory_bist=True,
            retention_hours=8760, endurance_cycles=1_000_000,
            tech_validated=True,
        )
        r = assess_physical_memory(p)
        self.assertGreater(r.omega, 0.7)

    def test_host_empty_low(self) -> None:
        from memory_chip_readiness.host_interface import assess_host_interface

        r = assess_host_interface(HostInterfaceProfile())
        self.assertLessEqual(r.omega, 0.2)

    def test_process_empty_low(self) -> None:
        from memory_chip_readiness.process_area_power import assess_process_area_power

        r = assess_process_area_power(ProcessAreaPowerProfile())
        self.assertLessEqual(r.omega, 0.2)


# ── GP Extension Layer Modules ───────────────────────────────────


class TestGPLayerModules(unittest.TestCase):
    def test_standard_interface_none_low(self) -> None:
        from memory_chip_readiness.standard_interface import assess_standard_interface

        r = assess_standard_interface(StandardInterfaceProfile())
        self.assertLessEqual(r.omega, 0.1)
        self.assertEqual(r.layer, "standard_interface")

    def test_standard_interface_ddr5_high(self) -> None:
        from memory_chip_readiness.standard_interface import assess_standard_interface

        p = StandardInterfaceProfile(
            memory_standard=MemoryStandard.ddr5,
            jedec_compliance_level=0.9, channel_count=4,
            data_rate_mtps=6400, phy_ip_validated=True,
            signal_integrity_sim=True, timing_margin_pct=15,
            init_sequence_defined=True, refresh_logic=True,
            rtl_coverage_pct=70,
        )
        r = assess_standard_interface(p)
        self.assertGreater(r.omega, 0.7)

    def test_cache_coherency_none_low(self) -> None:
        from memory_chip_readiness.cache_coherency import assess_cache_coherency

        r = assess_cache_coherency(CacheCoherencyProfile())
        self.assertLessEqual(r.omega, 0.15)
        self.assertEqual(r.layer, "cache_coherency")

    def test_cache_coherency_mesi_high(self) -> None:
        from memory_chip_readiness.cache_coherency import assess_cache_coherency

        p = CacheCoherencyProfile(
            coherency_protocol="mesi", snoop_filter=True,
            tlb_entries=256, virtual_address_bits=48,
            mmu_hw_walker=True, cache_line_bytes=64,
            multi_level_cache=True, atomic_ops_support=True,
            rtl_coverage_pct=70,
        )
        r = assess_cache_coherency(p)
        self.assertGreater(r.omega, 0.7)

    def test_multi_tenant_empty_low(self) -> None:
        from memory_chip_readiness.multi_tenant import assess_multi_tenant

        r = assess_multi_tenant(MultiTenantProfile())
        self.assertLessEqual(r.omega, 0.1)
        self.assertEqual(r.layer, "multi_tenant")

    def test_multi_tenant_full_high(self) -> None:
        from memory_chip_readiness.multi_tenant import assess_multi_tenant

        p = MultiTenantProfile(
            memory_protection_unit=True, process_isolation_hw=True,
            max_tenants=16, qos_arbiter=True,
            capacity_scalable=True, die_stacking_support=True,
            channel_bonding=True, bandwidth_partitioning=True,
            error_containment=True, rtl_coverage_pct=80,
        )
        r = assess_multi_tenant(p)
        self.assertGreater(r.omega, 0.8)

    def test_ecosystem_empty_low(self) -> None:
        from memory_chip_readiness.ecosystem_compat import assess_ecosystem_compat

        r = assess_ecosystem_compat(EcosystemCompatProfile())
        self.assertLessEqual(r.omega, 0.05)
        self.assertEqual(r.layer, "ecosystem_compat")

    def test_ecosystem_full_high(self) -> None:
        from memory_chip_readiness.ecosystem_compat import assess_ecosystem_compat

        p = EcosystemCompatProfile(
            kernel_driver_available=True, linux_support=True,
            rtos_support=True, memory_allocator_compat=True,
            numa_aware=True, hotplug_support=True,
            ras_features=True, monitoring_counters=True,
            documentation_complete=True, sdk_available=True,
        )
        r = assess_ecosystem_compat(p)
        self.assertEqual(r.omega, 1.0)


# ── Foundation — Accelerator ─────────────────────────────────────


class TestFoundationAccelerator(unittest.TestCase):
    def test_default_analysis(self) -> None:
        rpt = analyze()
        self.assertEqual(rpt.design_tier, DesignTier.accelerator)
        self.assertGreaterEqual(rpt.omega_chip, 0.0)
        self.assertEqual(len(rpt.layer_details), 6)

    def test_default_low_omega(self) -> None:
        rpt = analyze()
        self.assertLess(rpt.omega_chip, 0.3)
        self.assertEqual(rpt.verdict, ChipVerdict.concept_only)

    def test_gate_blocked_default(self) -> None:
        rpt = analyze()
        self.assertFalse(rpt.fabrication_gate.ready_for_tapeout)

    def test_bottleneck_valid(self) -> None:
        rpt = analyze()
        valid = {lr.layer for lr in rpt.layer_details}
        self.assertIn(rpt.key_bottleneck, valid)

    def test_bridge_generated(self) -> None:
        rpt = analyze()
        self.assertIn(rpt.chip_bridge.foundry_gate_status, ("pass", "pending"))


# ── Foundation — General Purpose ─────────────────────────────────


class TestFoundationGP(unittest.TestCase):
    def test_gp_default_has_10_layers(self) -> None:
        rpt = analyze(tier=DesignTier.general_purpose)
        self.assertEqual(rpt.design_tier, DesignTier.general_purpose)
        self.assertEqual(len(rpt.layer_details), 10)

    def test_gp_default_low(self) -> None:
        rpt = analyze(tier=DesignTier.general_purpose)
        self.assertLess(rpt.omega_chip, 0.3)

    def test_gp_extra_blockers(self) -> None:
        rpt = analyze(tier=DesignTier.general_purpose)
        self.assertIn("standard_interface_not_defined", rpt.fabrication_gate.blockers)
        self.assertIn("cache_coherency_missing", rpt.fabrication_gate.blockers)

    def test_hybrid_has_10_layers(self) -> None:
        rpt = analyze(tier=DesignTier.hybrid)
        self.assertEqual(rpt.design_tier, DesignTier.hybrid)
        self.assertEqual(len(rpt.layer_details), 10)

    def test_gp_edge_signal_has_gp_fields(self) -> None:
        rpt = analyze(tier=DesignTier.general_purpose)
        sig = rpt.to_edge_signal()
        self.assertIn("l07_standard_interface", sig)
        self.assertIn("l08_cache_coherency", sig)
        self.assertIn("l09_multi_tenant", sig)
        self.assertIn("l10_ecosystem_compat", sig)

    def test_accel_edge_signal_no_gp_fields(self) -> None:
        rpt = analyze(tier=DesignTier.accelerator)
        sig = rpt.to_edge_signal()
        self.assertNotIn("l07_standard_interface", sig)

    def test_summary_dict_has_tier(self) -> None:
        rpt = analyze(tier=DesignTier.general_purpose)
        d = rpt.to_summary_dict()
        self.assertEqual(d["design_tier"], "general_purpose")

    def test_gp_gate_downgrade_when_std_missing(self) -> None:
        """GP tier with no standard_interface → gate blocked & verdict downgraded."""
        from memory_chip_readiness.contracts import (
            ConsolidationSchedulerProfile,
            HostInterfaceProfile,
            LTMSearchAccelProfile,
            PhysicalMemoryProfile,
            ProcessAreaPowerProfile,
            STMMicroarchProfile,
        )

        rpt = analyze(
            tier=DesignTier.general_purpose,
            stm=STMMicroarchProfile(
                eviction_policy_defined=True, decay_engine_fsm=True,
                ttl_timer_hw=True, query_filter_block=True,
                sram_compiler_validated=True, rtl_coverage_pct=90,
            ),
            ltm=LTMSearchAccelProfile(
                similarity_engine_type="dot_product", vector_dim=256,
                top_k_hw=True, max_wells=4096, rtl_coverage_pct=80,
            ),
            consolidation=ConsolidationSchedulerProfile(
                eligibility_fsm=True, dma_controller=True, merge_arbiter=True,
                rtl_coverage_pct=70,
            ),
            physical=PhysicalMemoryProfile(
                stm_tech=MemoryTech.sram, stm_capacity_kb=128,
                ltm_capacity_mb=512, ecc_support=True, tech_validated=True,
            ),
            host=HostInterfaceProfile(
                bus_protocol=BusProtocol.axi4, bus_width_bits=128,
                dma_channels=4, register_map_defined=True, bandwidth_gbps=25.0,
            ),
            process=ProcessAreaPowerProfile(
                process_node=ProcessNode.nm7, foundry_pdk_available=True,
                dft_scan_chain=True, signoff_drc_clean=True,
            ),
            # standard/cache left as defaults → GP blockers trigger
        )
        self.assertIn("standard_interface_not_defined", rpt.fabrication_gate.blockers)
        self.assertIn("cache_coherency_missing", rpt.fabrication_gate.blockers)
        self.assertFalse(rpt.fabrication_gate.ready_for_tapeout)
        # verdict must not be tapeout_ready when gate is blocked
        from memory_chip_readiness.contracts import ChipVerdict
        self.assertNotEqual(rpt.verdict, ChipVerdict.tapeout_ready)


# ── Presets ──────────────────────────────────────────────────────


class TestPresets(unittest.TestCase):
    def test_list_presets_count(self) -> None:
        presets = list_presets()
        self.assertEqual(len(presets), 8)

    def test_accel_presets_exist(self) -> None:
        presets = list_presets()
        for name in [
            "FPGA_STM_Prototype", "EdgeAI_Memory_Coprocessor",
            "Robot_Memory_SoC", "Concept_BrainChip", "Spaceship_MemoryUnit",
        ]:
            self.assertIn(name, presets)

    def test_gp_presets_exist(self) -> None:
        presets = list_presets()
        self.assertIn("GP_DDR5_Compatible", presets)
        self.assertIn("GP_CXL_Datacenter", presets)
        self.assertIn("Hybrid_SmartMemory_Module", presets)

    def test_fpga_prototype_low(self) -> None:
        rpt = analyze_preset("FPGA_STM_Prototype")
        self.assertEqual(rpt.design_tier, DesignTier.accelerator)
        self.assertLess(rpt.omega_chip, 0.5)

    def test_edge_ai_mid(self) -> None:
        rpt = analyze_preset("EdgeAI_Memory_Coprocessor")
        self.assertGreater(rpt.omega_chip, 0.6)

    def test_robot_soc_high(self) -> None:
        rpt = analyze_preset("Robot_Memory_SoC")
        self.assertGreater(rpt.omega_chip, 0.7)

    def test_concept_brainchip_low(self) -> None:
        rpt = analyze_preset("Concept_BrainChip")
        self.assertLess(rpt.omega_chip, 0.3)

    def test_gp_ddr5_has_10_layers(self) -> None:
        rpt = analyze_preset("GP_DDR5_Compatible")
        self.assertEqual(rpt.design_tier, DesignTier.general_purpose)
        self.assertEqual(len(rpt.layer_details), 10)
        self.assertGreater(rpt.omega_chip, 0.6)

    def test_gp_cxl_datacenter(self) -> None:
        rpt = analyze_preset("GP_CXL_Datacenter")
        self.assertEqual(rpt.design_tier, DesignTier.general_purpose)
        self.assertGreater(rpt.omega_chip, 0.5)

    def test_hybrid_smart_memory(self) -> None:
        rpt = analyze_preset("Hybrid_SmartMemory_Module")
        self.assertEqual(rpt.design_tier, DesignTier.hybrid)
        self.assertEqual(len(rpt.layer_details), 10)
        self.assertGreater(rpt.omega_chip, 0.5)

    def test_unknown_preset_raises(self) -> None:
        with self.assertRaises(KeyError):
            analyze_preset("NonExistent")


# ── Serialization ────────────────────────────────────────────────


class TestSerialization(unittest.TestCase):
    def test_to_summary_dict(self) -> None:
        rpt = analyze_preset("EdgeAI_Memory_Coprocessor")
        d = rpt.to_summary_dict()
        self.assertIn("omega_chip", d)
        self.assertIn("design_tier", d)
        json_str = json.dumps(d, ensure_ascii=False)
        self.assertIsInstance(json_str, str)

    def test_to_edge_signal_flat(self) -> None:
        rpt = analyze_preset("Robot_Memory_SoC")
        sig = rpt.to_edge_signal()
        for v in sig.values():
            self.assertIsInstance(v, (float, bool, str, int))


# ── CLI ──────────────────────────────────────────────────────────


class TestCLI(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "memory_chip_readiness", *args],
            capture_output=True, text=True, cwd=_CWD,
        )

    def test_version(self) -> None:
        r = self._run("--version")
        self.assertEqual(r.returncode, 0)
        self.assertIn("memory-chip-readiness", r.stdout)

    def test_list_presets(self) -> None:
        r = self._run("list-presets")
        self.assertEqual(r.returncode, 0)
        self.assertIn("GP_DDR5_Compatible", r.stdout)

    def test_analyze_json(self) -> None:
        r = self._run("analyze", "EdgeAI_Memory_Coprocessor", "--json")
        self.assertEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertEqual(d["design_tier"], "accelerator")

    def test_analyze_gp_json(self) -> None:
        r = self._run("analyze", "GP_DDR5_Compatible", "--json")
        self.assertEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertEqual(d["design_tier"], "general_purpose")
        self.assertIn("standard_interface", d["layers"])

    def test_analyze_edge(self) -> None:
        r = self._run("analyze", "Hybrid_SmartMemory_Module", "--edge")
        self.assertEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertIn("l07_standard_interface", d)

    def test_gate_test_tier_override(self) -> None:
        r = self._run(
            "gate-test", "FPGA_STM_Prototype",
            "--tier", "general_purpose", "--json",
        )
        self.assertEqual(r.returncode, 0)
        d = json.loads(r.stdout)
        self.assertEqual(d["design_tier"], "general_purpose")


# ── Weight Integrity ─────────────────────────────────────────────


class TestWeightIntegrity(unittest.TestCase):
    def test_weight_sums_to_one(self) -> None:
        from memory_chip_readiness.foundation import (
            _WEIGHTS_ACCELERATOR,
            _WEIGHTS_GENERAL_PURPOSE,
            _WEIGHTS_HYBRID,
        )

        self.assertAlmostEqual(sum(_WEIGHTS_ACCELERATOR.values()), 1.0, places=9)
        self.assertAlmostEqual(sum(_WEIGHTS_GENERAL_PURPOSE.values()), 1.0, places=9)
        self.assertAlmostEqual(sum(_WEIGHTS_HYBRID.values()), 1.0, places=9)

    def test_weight_keys_match_layers(self) -> None:
        from memory_chip_readiness.foundation import (
            _WEIGHTS_ACCELERATOR,
            _WEIGHTS_GENERAL_PURPOSE,
            _WEIGHTS_HYBRID,
        )

        accel_expected = {
            "stm_microarch", "ltm_search_accel", "consolidation_scheduler",
            "physical_memory", "host_interface", "process_area_power",
        }
        gp_expected = accel_expected | {
            "standard_interface", "cache_coherency", "multi_tenant", "ecosystem_compat",
        }
        self.assertEqual(set(_WEIGHTS_ACCELERATOR.keys()), accel_expected)
        self.assertEqual(set(_WEIGHTS_GENERAL_PURPOSE.keys()), gp_expected)
        self.assertEqual(set(_WEIGHTS_HYBRID.keys()), gp_expected)

    def test_no_negative_weights(self) -> None:
        from memory_chip_readiness.foundation import (
            _WEIGHTS_ACCELERATOR,
            _WEIGHTS_GENERAL_PURPOSE,
            _WEIGHTS_HYBRID,
        )

        for wmap in (_WEIGHTS_ACCELERATOR, _WEIGHTS_GENERAL_PURPOSE, _WEIGHTS_HYBRID):
            for k, v in wmap.items():
                self.assertGreater(v, 0.0, msg=f"Weight {k}={v} must be positive")


if __name__ == "__main__":
    unittest.main()
