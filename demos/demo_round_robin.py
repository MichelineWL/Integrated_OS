"""
Demo: Round Robin Scheduling
Demonstrates RR scheduling with Process A (20s) and Process B (17s)
Time Quantum: 3s
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Process, MemoryManager, CPUScheduler

def demo_round_robin_detailed():
    """Detailed Round Robin demonstration"""
    print("="*60)
    print("    ROUND ROBIN SCHEDULING DEMONSTRATION")
    print("    Process A: 20s burst time")
    print("    Process B: 17s burst time")
    print("    Time Quantum: 3s")
    print("="*60)
    
    # Reset process counter
    Process.reset_id_counter()
    
    # Create processes exactly as specified
    process_a = Process("Process_A", 20, 8)  # 20s burst, 8KB size
    process_b = Process("Process_B", 17, 6)  # 17s burst, 6KB size
    
    # Add some realistic instructions
    instructions_a = [
        "Initialize variables",
        "Load data from memory", 
        "Perform calculations",
        "Process data array",
        "Update counters",
        "Check conditions",
        "Write results"
    ]
    
    instructions_b = [
        "Open input file",
        "Read file contents",
        "Parse data",
        "Transform data",
        "Generate output",
        "Close file"
    ]
    
    for instruction in instructions_a:
        process_a.add_instruction(instruction)
    
    for instruction in instructions_b:
        process_b.add_instruction(instruction)
    
    print(f"Process A: {process_a}")
    print(f"Process B: {process_b}")
    
    # Setup memory manager
    memory_manager = MemoryManager(total_frames=8, algorithm='FIFO')
    memory_manager.register_process(process_a)
    memory_manager.register_process(process_b)
    
    # Setup Round Robin scheduler
    scheduler = CPUScheduler(algorithm='RR', time_quantum=3)
    scheduler.add_process(process_a)
    scheduler.add_process(process_b)
    
    print("\nExpected Round Robin execution pattern:")
    print("A(3s) → B(3s) → A(3s) → B(3s) → A(3s) → B(3s) → A(3s) → B(3s)")
    print("A(3s) → B(3s) → A(3s) → B(2s) → A(2s)")
    print("Total expected time: 37s")
    
    # Run simulation
    result = scheduler.run_complete_simulation(memory_manager)
    
    print(f"\nSimulation Results:")
    print(f"Total execution time: {result['total_time']}s")
    print(f"Context switches: {result['context_switches']}")
    print(f"Average waiting time: {result['average_waiting_time']:.2f}s")
    print(f"Average turnaround time: {result['average_turnaround_time']:.2f}s")
    
    # Analyze execution pattern
    execution_order = result['execution_order']
    print(f"\nExecution sequence analysis:")
    print(f"Process A executed {execution_order.count('P0')} time units")
    print(f"Process B executed {execution_order.count('P1')} time units")
    
    # Show time quantum effectiveness
    current_process = None
    quantum_usage = []
    current_quantum = 0
    
    for process_id in execution_order:
        if process_id != current_process:
            if current_process is not None:
                quantum_usage.append((current_process, current_quantum))
            current_process = process_id
            current_quantum = 1
        else:
            current_quantum += 1
    
    if current_process is not None:
        quantum_usage.append((current_process, current_quantum))
    
    print(f"\nTime quantum usage analysis:")
    for process_id, quantum_used in quantum_usage:
        process_name = "Process_A" if process_id == "P0" else "Process_B"
        print(f"{process_name}: {quantum_used} time units")
    
    # Display memory statistics
    memory_manager.display_memory_status()
    
    return result

if __name__ == "__main__":
    demo_round_robin_detailed()
