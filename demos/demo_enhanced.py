"""
Enhanced OS Simulator Demo
Showcases integration of best features from aiss:
- Hex address translation
- Interactive controls (pause/resume/step)
- Real-time execution with delays
- UUID process identification
- Memory cleanup
- Comprehensive statistics
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Process, MemoryManager, CPUScheduler

def demo_enhanced_features():
    """Demonstrate all enhanced features integrated from aiss"""
    
    print("="*70)
    print("    ENHANCED OS SIMULATOR v2.1 DEMONSTRATION")
    print("    Integration of Best Features from aiss")
    print("="*70)
    
    # Reset Process ID counter for consistent demo
    Process.reset_id_counter()
    
    # Create enhanced processes with UUID support
    print("\\n1. CREATING PROCESSES WITH UUID SUPPORT")
    print("-" * 50)
    
    process_a = Process("WebServer", 8, 12)  # 8s burst, 12KB memory
    process_b = Process("Database", 6, 16)   # 6s burst, 16KB memory
    
    print(f"Created: {process_a}")
    print(f"Created: {process_b}")
    
    # Add realistic instructions
    web_instructions = [
        "Initialize web server",
        "Load configuration",
        "Bind to port 80",
        "Accept connections",
        "Process HTTP request",
        "Query database",
        "Generate response",
        "Send to client"
    ]
    
    db_instructions = [
        "Initialize database",
        "Load schema",
        "Create indexes",
        "Process query",
        "Return results",
        "Update statistics"
    ]
    
    for instruction in web_instructions:
        process_a.add_instruction(instruction)
    
    for instruction in db_instructions:
        process_b.add_instruction(instruction)
    
    # Add hex instructions for realistic memory access
    hex_addresses_a = ["0x1000", "0x1200", "0x2000", "0x2100", "0x1500", "0x3000", "0x1800", "0x2500"]
    hex_addresses_b = ["0x4000", "0x4100", "0x5000", "0x4200", "0x6000", "0x5500"]
    
    for hex_addr in hex_addresses_a:
        process_a.add_hex_instruction(hex_addr)
    
    for hex_addr in hex_addresses_b:
        process_b.add_hex_instruction(hex_addr)
    
    print(f"\\nProcess A hex addresses: {process_a.hex_instructions}")
    print(f"Process B hex addresses: {process_b.hex_instructions}")
    
    # Create enhanced memory manager
    print("\\n\\n2. ENHANCED MEMORY MANAGER WITH HEX ADDRESS SUPPORT")
    print("-" * 50)
    
    memory_manager = MemoryManager(total_frames=6, algorithm='LRU')
    memory_manager.register_process(process_a)
    memory_manager.register_process(process_b)
    
    # Test hex address translation
    print("\\nTesting hex address translation:")
    for hex_addr in ["0x1000", "0x1200", "0x4000"]:
        result = memory_manager.translate_hex_address(process_a, hex_addr)
        print(f"  {hex_addr} → Physical: {result if result else 'Page fault needed'}")
    
    # Create enhanced CPU scheduler
    print("\\n\\n3. ENHANCED CPU SCHEDULER WITH REAL-TIME EXECUTION")
    print("-" * 50)
    
    scheduler = CPUScheduler(algorithm='RR', time_quantum=3)
    scheduler.add_process(process_a)
    scheduler.add_process(process_b)
    
    # Set faster execution for demo (normally 1.0s)
    scheduler.set_execution_delay(0.5)  # 0.5 seconds per instruction
    
    print("\\nScheduler configured:")
    print(f"  Algorithm: Round Robin")
    print(f"  Time Quantum: 3s")
    print(f"  Execution Delay: 0.5s per instruction")
    print(f"  Interactive Controls: Available")
    
    # Demonstrate interactive controls
    print("\\n\\n4. INTERACTIVE CONTROL DEMONSTRATION")
    print("-" * 50)
    
    print("Available controls:")
    print("  - scheduler.pause_simulation() / scheduler.resume_simulation()")
    print("  - scheduler.enable_step_mode() / scheduler.disable_step_mode()")
    print("  - memory_manager.pause_simulation() / memory_manager.resume_simulation()")
    
    # Run simulation with interactive features
    print("\\n\\n5. RUNNING ENHANCED SIMULATION")
    print("-" * 50)
    
    print("Starting real-time simulation with hex address support...")
    print("(Note: Using faster 0.5s delay for demo purposes)")
    
    # Option to enable step mode for detailed observation
    user_input = input("\\nEnable step-by-step mode? (y/n): ").lower().strip()
    if user_input == 'y':
        scheduler.enable_step_mode()
        print("Step mode enabled. Press Enter for each instruction.")
    
    # Run the enhanced simulation
    result = scheduler.run_realtime_simulation(memory_manager)
    
    # Display comprehensive results
    print("\\n\\n6. ENHANCED SIMULATION RESULTS")
    print("-" * 50)
    
    print(f"\\nExecution Summary:")
    print(f"  Total Execution Time: {result['total_time']}s")
    print(f"  Real-time Duration: {result['simulation_duration']:.2f}s")
    print(f"  Context Switches: {result['context_switches']}")
    print(f"  Average Waiting Time: {result['average_waiting_time']:.2f}s")
    print(f"  Average Turnaround Time: {result['average_turnaround_time']:.2f}s")
    
    print(f"\\nMemory Performance:")
    print(f"  Overall Hit Ratio: {result['overall_hit_ratio']:.2f}%")
    print(f"  Total Memory Accesses: {len(result['memory_accesses'])}")
    
    # Show hex execution log sample
    if result['hex_execution_log']:
        print(f"\\nHex Address Execution Log (sample):")
        for i, log in enumerate(result['hex_execution_log'][:8]):
            status_symbol = "✓" if log['status'] == 'HIT' else "⚠"
            print(f"  [{log['time']:2d}s] {log['process']}: {log['hex_address']} → {log['physical_address']} {status_symbol}")
    
    # Display final memory status
    print("\\n\\n7. FINAL MEMORY STATUS")
    print("-" * 50)
    memory_manager.display_memory_status()
    
    # Demonstrate memory cleanup (already done automatically)
    print("\\n\\n8. MEMORY CLEANUP DEMONSTRATION")
    print("-" * 50)
    print("Memory cleanup was performed automatically after process completion.")
    print("All frames have been deallocated and returned to the free pool.")
    
    # Process statistics
    print("\\n\\n9. INDIVIDUAL PROCESS STATISTICS")
    print("-" * 50)
    
    for process in [process_a, process_b]:
        print(f"\\nProcess: {process.name} (UUID: {process.process_id})")
        print(f"  Page Hits: {process.page_hits}")
        print(f"  Page Faults: {process.page_faults}")
        print(f"  Hit Ratio: {process.get_hit_ratio():.2f}%")
        print(f"  Final State: {process.state}")
        print(f"  Memory Allocated: {process.is_allocated}")
    
    print("\\n\\n" + "="*70)
    print("    ENHANCED DEMONSTRATION COMPLETED")
    print("    Key Features Demonstrated:")
    print("    ✓ UUID process identification")
    print("    ✓ Hex address translation")
    print("    ✓ Real-time execution simulation")
    print("    ✓ Interactive controls (pause/resume/step)")
    print("    ✓ Automatic memory cleanup")
    print("    ✓ Comprehensive statistics tracking")
    print("    ✓ Enhanced memory management")
    print("="*70)

def demo_comparison():
    """Quick comparison between original and enhanced features"""
    
    print("\\n\\n" + "="*70)
    print("    FEATURE COMPARISON: Original vs Enhanced")
    print("="*70)
    
    comparison_table = [
        ("Feature", "Original v2.0", "Enhanced v2.1"),
        ("-" * 30, "-" * 15, "-" * 15),
        ("Process ID", "P0, P1, P2", "UUID + Simple ID"),
        ("Memory Access", "Page numbers only", "Hex addresses + Pages"),
        ("Execution", "Instant", "Real-time with delays"),
        ("Controls", "Run only", "Pause/Resume/Step"),
        ("Memory Cleanup", "Manual", "Automatic"),
        ("Address Translation", "Not supported", "Full hex support"),
        ("Statistics", "Basic", "Comprehensive"),
        ("Integration", "Separate components", "Fully integrated")
    ]
    
    for row in comparison_table:
        print(f"{row[0]:<30} {row[1]:<15} {row[2]:<15}")
    
    print("\\n✅ Enhanced version provides all original features plus aiss integrations!")

if __name__ == "__main__":
    demo_enhanced_features()
    demo_comparison()
