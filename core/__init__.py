"""
Core Package for Operating System Simulator
Enhanced Architecture - Version 2.1
Integrates best features from aiss: hex addresses, interactive controls, real-time execution
"""

# Original models (preserved for compatibility)
from .models import Process as OriginalProcess, PhysicalMemory as OriginalPhysicalMemory, Statistics as OriginalStatistics
from .memory_manager import MemoryManager as OriginalMemoryManager, PhysicalMemory_Legacy
from .cpu_scheduler import CPUScheduler as OriginalCPUScheduler

# Enhanced models with new features
from .enhanced_models import Process, PhysicalMemory, Statistics
from .enhanced_memory_manager import EnhancedMemoryManager as MemoryManager
from .enhanced_cpu_scheduler import EnhancedCPUScheduler as CPUScheduler

from .config import *

__version__ = "2.1.0"
__author__ = "OS Simulator Team - Enhanced Edition"

# Export main classes
__all__ = [
    # Enhanced Core Models (primary)
    'Process',
    'PhysicalMemory', 
    'Statistics',
    # Enhanced Managers (primary)
    'MemoryManager',
    'CPUScheduler',
    
    # Original/Legacy classes (for compatibility)
    'OriginalProcess',
    'OriginalPhysicalMemory',
    'OriginalStatistics',
    'OriginalMemoryManager',
    'OriginalCPUScheduler',
    'PhysicalMemory_Legacy',
    
    # Configuration
    'PAGE_SIZE',
    'FRAME_SIZE',
    'DEFAULT_TIME_QUANTUM',
    'SUPPORTED_ALGORITHMS',
    'SUPPORTED_REPLACEMENT_ALGORITHMS',
    'get_system_info',
    'validate_configuration'
]

def get_version():
    """Get package version"""
    return __version__

def get_system_status():
    """Get comprehensive system status"""
    config_errors = validate_configuration()
    
    return {
        'version': __version__,
        'configuration_valid': len(config_errors) == 0,
        'configuration_errors': config_errors,
        'system_info': get_system_info()
    }
