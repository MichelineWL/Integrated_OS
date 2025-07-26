"""
System Configuration
Contains all system constants and configuration parameters
"""

# Memory Configuration
PAGE_SIZE = 4096        # 4KB per page
FRAME_SIZE = PAGE_SIZE  # Frame size equals page size
DEFAULT_MEMORY_SIZE = 64  # KB
DEFAULT_FRAME_COUNT = 16  # 64KB / 4KB

# CPU Scheduling Configuration
DEFAULT_TIME_QUANTUM = 3  # seconds
SUPPORTED_ALGORITHMS = ['FCFS', 'RR']

# Memory Management Configuration
SUPPORTED_REPLACEMENT_ALGORITHMS = ['FIFO', 'LRU']
DEFAULT_REPLACEMENT_ALGORITHM = 'FIFO'

# Process Configuration
MIN_PROCESS_SIZE = 1    # KB
MAX_PROCESS_SIZE = 32   # KB
MIN_BURST_TIME = 1      # seconds
MAX_BURST_TIME = 30     # seconds

# Simulation Configuration
ENABLE_MEMORY_SIMULATION = True
ENABLE_DETAILED_LOGGING = True
ENABLE_STATISTICS = True

# Display Configuration
CONSOLE_WIDTH = 60
SEPARATOR_CHAR = '='

# Color codes for terminal output (if supported)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# System limits
MAX_PROCESSES = 10
MAX_SIMULATION_TIME = 1000  # seconds

def get_system_info():
    """Get system configuration information"""
    return {
        'page_size': PAGE_SIZE,
        'frame_size': FRAME_SIZE,
        'default_memory_size': DEFAULT_MEMORY_SIZE,
        'default_frame_count': DEFAULT_FRAME_COUNT,
        'default_time_quantum': DEFAULT_TIME_QUANTUM,
        'supported_cpu_algorithms': SUPPORTED_ALGORITHMS,
        'supported_memory_algorithms': SUPPORTED_REPLACEMENT_ALGORITHMS,
        'max_processes': MAX_PROCESSES,
        'max_simulation_time': MAX_SIMULATION_TIME
    }

def validate_configuration():
    """Validate system configuration"""
    errors = []
    
    if PAGE_SIZE <= 0:
        errors.append("PAGE_SIZE must be positive")
    
    if DEFAULT_TIME_QUANTUM <= 0:
        errors.append("DEFAULT_TIME_QUANTUM must be positive")
    
    if MAX_PROCESSES <= 0:
        errors.append("MAX_PROCESSES must be positive")
    
    return errors
