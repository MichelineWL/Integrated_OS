# Operating System Simulator v2.0

**Improved Architecture** - A comprehensive simulation of operating system components including CPU scheduling and memory management with virtual memory support.

## 🚀 Features

### CPU Scheduling
- **FCFS (First Come First Serve)**: Non-preemptive scheduling
- **Round Robin**: Preemptive scheduling with configurable time quantum
- Real-time execution simulation with accurate timing
- Context switching statistics
- Process completion analytics

### Memory Management
- **Virtual Memory**: Page-based memory management
- **FIFO Page Replacement**: First-In-First-Out algorithm
- **LRU Page Replacement**: Least Recently Used algorithm
- Page hit/fault statistics
- Memory utilization tracking
- Locality of reference simulation

### System Features
- Interactive menu-driven interface
- Configurable system parameters
- Comprehensive testing suite
- Demonstration scenarios
- Statistical analysis and reporting
- Process lifecycle management

## 📁 Project Structure

```
improved_os/
├── core/                      # Core system components
│   ├── __init__.py           # Package initialization
│   ├── models.py             # Process, Memory, Statistics classes
│   ├── memory_manager.py     # Virtual memory system
│   ├── cpu_scheduler.py      # CPU scheduling algorithms
│   └── config.py             # System configuration
├── tests/                     # Test suite
│   └── test_all.py           # Comprehensive tests
├── demos/                     # Demonstration scripts
│   ├── demo_round_robin.py   # RR scheduling demo
│   └── demo_memory.py        # Memory management demo
├── main.py                   # Main application
└── README.md                 # This file
```

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.7 or higher
- No external dependencies required

### Quick Start

1. **Clone or download the project**
2. **Navigate to the project directory**
3. **Run the main application:**
   ```bash
   python main.py
   ```

### Running Tests
```bash
python tests/test_all.py
```

### Running Demos
```bash
# Round Robin demonstration
python demos/demo_round_robin.py

# Memory management demonstration
python demos/demo_memory.py
```

## 📖 Usage Guide

### Creating Processes
1. Select option 1 from the main menu
2. Enter process name, burst time, and memory size
3. Add instructions for the process

### CPU Scheduling Simulation
1. Create one or more processes
2. Configure scheduler (option 4)
3. Run FCFS (option 5) or Round Robin (option 6)

### Memory Management
1. Configure memory manager (option 3)
2. Choose FIFO or LRU algorithm
3. Set number of memory frames
4. Run simulations to see page replacement in action

### Custom Simulations
Use option 7 to run simulations with custom parameters without changing global settings.

## 🎯 Key Improvements Over v1.0

### Architecture
- **Modular Design**: Separated concerns into distinct modules
- **Type Hints**: Improved code readability and IDE support
- **Comprehensive Testing**: Full test coverage for all components
- **Better Error Handling**: Robust error management

### Memory Management
- **Virtual Memory**: Complete virtual memory implementation
- **Page Replacement**: FIFO and LRU algorithms
- **Statistics Tracking**: Detailed memory access statistics
- **Locality Simulation**: Realistic page access patterns

### CPU Scheduling
- **Accurate Timing**: Time-based simulation instead of instruction counting
- **Context Switching**: Proper context switch handling and statistics
- **Process States**: Complete process lifecycle management
- **Performance Metrics**: Waiting time, turnaround time calculations

### User Experience
- **Interactive Interface**: Menu-driven application
- **Configuration Options**: Runtime parameter adjustment
- **Demonstration Modes**: Predefined scenarios
- **Comprehensive Reporting**: Detailed statistics and analysis

## 🧪 Example Scenarios

### Round Robin Scheduling
The classic example from your question:
- Process A: 20 seconds burst time
- Process B: 17 seconds burst time
- Time Quantum: 3 seconds

Expected execution pattern:
```
A(3s) → B(3s) → A(3s) → B(3s) → A(3s) → B(3s) → A(3s) → B(3s)
A(3s) → B(3s) → A(3s) → B(2s) → A(2s)
```

### Memory Page Replacement
Test scenario with 3 frames, 5 pages:
```
Access pattern: [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
FIFO result:    FAULT, FAULT, FAULT, FAULT, HIT, HIT, FAULT, HIT, HIT, FAULT, FAULT, FAULT
LRU result:     FAULT, FAULT, FAULT, FAULT, HIT, HIT, FAULT, HIT, HIT, FAULT, FAULT, HIT
```

## 📊 Technical Specifications

### Memory Management
- **Page Size**: 4KB (4096 bytes)
- **Frame Size**: 4KB (same as page size)
- **Default Memory**: 64KB (16 frames)
- **Supported Algorithms**: FIFO, LRU
- **Maximum Frames**: 32

### CPU Scheduling
- **Default Time Quantum**: 3 seconds
- **Supported Algorithms**: FCFS, Round Robin
- **Maximum Processes**: 10
- **Maximum Simulation Time**: 1000 seconds

### Process Model
- **Minimum Process Size**: 1KB
- **Maximum Process Size**: 32KB
- **Minimum Burst Time**: 1 second
- **Maximum Burst Time**: 30 seconds

## 🔬 Testing

The project includes comprehensive tests covering:

1. **Process Creation**: Page calculation, page table initialization
2. **FIFO Algorithm**: Correct victim selection and queue management
3. **LRU Algorithm**: Proper access order tracking
4. **FCFS Scheduling**: Sequential execution verification
5. **Round Robin**: Time quantum and preemption logic
6. **Integrated System**: Memory and CPU interaction

Run all tests:
```bash
python tests/test_all.py
```

Expected output: All tests should pass with detailed verification messages.

## 🎮 Interactive Demonstrations

### Built-in Demos
1. **Round Robin Comparison**: Your specific scenario (A=20s, B=17s, Q=3s)
2. **FCFS vs RR**: Performance comparison
3. **Memory Algorithms**: FIFO vs LRU comparison
4. **Locality Effects**: How access patterns affect hit ratios

### Menu Option 10
Access all demonstrations through the main application menu for interactive exploration.

## 🔧 Configuration

### Memory Manager
- **Total Frames**: 4-32 frames
- **Algorithm**: FIFO or LRU
- **Statistics**: Hit ratio, fault count

### CPU Scheduler
- **Algorithm**: FCFS or Round Robin
- **Time Quantum**: 1-10 seconds (RR only)
- **Statistics**: Context switches, waiting times

### Process Creation
- **Name**: Custom or auto-generated
- **Burst Time**: 1-30 seconds
- **Size**: 1-32 KB
- **Instructions**: Custom or default

## 🎯 Learning Objectives

This simulator helps understand:

1. **CPU Scheduling Algorithms**
   - How FCFS provides fair but potentially inefficient scheduling
   - How Round Robin provides fairness through time sharing
   - The impact of time quantum on performance

2. **Memory Management**
   - Virtual memory concepts and page tables
   - Page replacement algorithm trade-offs
   - The importance of locality of reference

3. **System Integration**
   - How CPU and memory management interact
   - Performance measurement and optimization
   - Resource allocation and utilization

## 🤝 Comparison with Friend's Code

### Advantages of This Implementation
- **Better Architecture**: Clear separation of concerns
- **More Features**: Comprehensive statistics, multiple demos
- **User Friendly**: Interactive menu system
- **Educational**: Clear demonstration of concepts
- **Robust**: Comprehensive error handling and validation

### Similar Strengths
- **Modular Design**: Both use good separation
- **Type Hints**: Both have proper typing
- **Testing**: Both include test suites
- **Documentation**: Both are well documented

### Key Differentiators
- **Interactive Interface**: Menu-driven vs script-based
- **Flexibility**: Runtime configuration vs hardcoded
- **Demonstrations**: Built-in scenarios vs manual setup
- **Statistics**: Comprehensive reporting vs basic output

## 📝 License

This project is for educational purposes. Feel free to modify and extend for learning about operating systems concepts.

## 👥 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

**Happy Learning! 🎓**
#   I n t e g r a t e d _ O S  
 