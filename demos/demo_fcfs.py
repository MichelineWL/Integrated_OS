"""
Enhanced FCFS Scheduling Demonstration
This demo shows First Come First Served scheduling with enhanced features:
- UUID process identification
- Hex address translation
- Real-time execution
- Automatic memory cleanup
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Process, MemoryManager, CPUScheduler

def main():
    print("="*60)
    print("    ENHANCED FCFS SCHEDULING DEMONSTRATION")
    print("    Process A: 20s burst time")
    print("    Process B: 17s burst time")
    print("    Features: UUID IDs, Hex addresses, Real-time execution")
    print("="*60)
    
    # Reset Process ID counter
    Process.reset_id_counter()
    
    # Create processes with same specifications as Round Robin demo
    process_a = Process("Process_A", 20, 8)  # 20s burst, 8KB memory
    process_b = Process("Process_B", 17, 8)  # 17s burst, 8KB memory
    
    print(f"Process A: {process_a}")
    print(f"Process B: {process_b}")
    
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
    
    # Create memory manager
    memory_manager = MemoryManager(total_frames=8, algorithm='FIFO')
    memory_manager.register_process(process_a)
    memory_manager.register_process(process_b)
    
    # Create FCFS scheduler
    scheduler = CPUScheduler(algorithm='FCFS')
    scheduler.add_process(process_a)
    scheduler.add_process(process_b)
    
    print("\nFCFS Execution Pattern:")
    print("Process A runs completely (20s), then Process B runs completely (17s)")
    print("Total expected time: 37s (no preemption, no context switches)")
    
    # Set faster execution for demo (enhanced feature)
    scheduler.set_execution_delay(0.2)  # 0.2 seconds per instruction for demo
    
    # Run enhanced simulation
    result = scheduler.run_realtime_simulation(memory_manager)
    
    print(f"\nEnhanced Simulation Results:")
    print(f"Total execution time: {result['total_time']}s")
    print(f"Real-time duration: {result['simulation_duration']:.2f}s")
    print(f"Context switches: {result['context_switches']}")
    print(f"Average waiting time: {result['average_waiting_time']:.2f}s")
    print(f"Average turnaround time: {result['average_turnaround_time']:.2f}s")
    print(f"Memory hit ratio: {result['overall_hit_ratio']:.2f}%")
    
    print(f"\nExecution sequence analysis:")
    print(f"Process A executed {result['execution_order'].count('P0')} time units")
    print(f"Process B executed {result['execution_order'].count('P1')} time units")
    
    # Show hex execution sample
    if result['hex_execution_log']:
        print(f"\nHex Address Execution Sample:")
        for i, log in enumerate(result['hex_execution_log'][:6]):
            status_symbol = "✓" if log['status'] == 'HIT' else "⚠"
            print(f"  [{log['time']:2d}s] {log['process']}: {log['hex_address']} → {log['physical_address']} {status_symbol}")
    
    print(f"\nComparison with Round Robin:")
    print(f"FCFS - Average waiting time: {result['average_waiting_time']:.2f}s")
    print(f"RR   - Average waiting time: 17.50s")
    print(f"FCFS - Context switches: {result['context_switches']}")
    print(f"RR   - Context switches: 11")
    print(f"FCFS - Memory hit ratio: {result['overall_hit_ratio']:.2f}%")
    
    # Display memory status
    memory_manager.display_memory_status()

if __name__ == "__main__":
    main()
