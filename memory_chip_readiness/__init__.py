"""Memory Chip Readiness Foundation.

STM/LTM/Consolidation 메모리 로직 → 실리콘 준비도 스크리닝 엔진.
DesignTier: accelerator(전문) / general_purpose(범용) / hybrid.
"""

from .cli import cli_main
from .contracts import (
    BusProtocol,
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
    MemoryStandard,
    MemoryTech,
    MultiTenantProfile,
    PhysicalMemoryProfile,
    ProcessAreaPowerProfile,
    ProcessNode,
    StandardInterfaceProfile,
    STMMicroarchProfile,
)
from .foundation import analyze
from .presets import analyze_preset, list_presets
from .version import __version__

__all__ = [
    "__version__",
    # enums
    "BusProtocol",
    "ChipVerdict",
    "DesignTier",
    "MemoryStandard",
    "MemoryTech",
    "ProcessNode",
    # profiles (inputs) — core
    "STMMicroarchProfile",
    "LTMSearchAccelProfile",
    "ConsolidationSchedulerProfile",
    "PhysicalMemoryProfile",
    "HostInterfaceProfile",
    "ProcessAreaPowerProfile",
    # profiles (inputs) — GP extension
    "StandardInterfaceProfile",
    "CacheCoherencyProfile",
    "MultiTenantProfile",
    "EcosystemCompatProfile",
    # outputs
    "MemoryChipReadinessReport",
    "LayerResult",
    "FabricationGate",
    "ChipBridgeSignal",
    # functions
    "analyze",
    "analyze_preset",
    "list_presets",
    "cli_main",
]
