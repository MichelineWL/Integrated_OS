#!/usr/bin/env python3
"""
Operating System Simulator - Main Application
Improved Architecture Version 2.0

Interactive menu-driven application for demonstrating:
- CPU Scheduling (FCFS, Round Robin)
- Memory Management (FIFO, LRU page replacement)
- Integrated system simulation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import (
    Process, MemoryManager, CPUScheduler, 
    get_system_info, validate_configuration,
    DEFAULT_TIME_QUANTUM, SUPPORTED_ALGORITHMS, SUPPORTED_REPLACEMENT_ALGORITHMS
)

class OSSimulator:
    """Main Operating System Simulator Application"""
    
    def __init__(self):
        self.processes = []
        self.memory_manager = None
        self.cpu_scheduler = None
        self.current_memory_algorithm = 'FIFO'
        self.current_cpu_algorithm = 'FCFS'
        self.time_quantum = DEFAULT_TIME_QUANTUM
        self.memory_frames = 16
        
        # Initialize default components
        self._initialize_memory_manager()
        self._initialize_cpu_scheduler()
    
    def _initialize_memory_manager(self):
        """Initialize memory manager with current settings"""
        self.memory_manager = MemoryManager(
            total_frames=self.memory_frames,
            algorithm=self.current_memory_algorithm
        )
        
        # Re-register existing processes
        for process in self.processes:
            self.memory_manager.register_process(process)
    
    def _initialize_cpu_scheduler(self):
        """Initialize CPU scheduler with current settings"""
        self.cpu_scheduler = CPUScheduler(
            algorithm=self.current_cpu_algorithm,
            time_quantum=self.time_quantum
        )
    
    def display_main_menu(self):
        """Display main application menu"""
        print("\n" + "="*60)
        print("    OPERATING SYSTEM SIMULATOR v2.0")
        print("="*60)
        print("1.  Create Process")
        print("2.  List Processes")
        print("3.  Configure Memory Manager")
        print("4.  Configure CPU Scheduler")
        print("5.  Run FCFS Scheduling")
        print("6.  Run Round Robin Scheduling") 
        print("7.  Run Custom Simulation")
        print("8.  Show Memory Status")
        print("9.  Show System Statistics")
        print("10. Run Demonstration Scenarios")
        print("11. Clear All Processes")
        print("12. System Information")
        print("0.  Exit")
        print("="*60)
        print(f"Current Config: Memory={self.current_memory_algorithm}, "
              f"CPU={self.current_cpu_algorithm}, Quantum={self.time_quantum}s")
    
    def get_user_choice(self):
        """Get and validate user menu choice"""
        try:
            choice = int(input("Enter your choice (0-12): "))
            return choice
        except ValueError:
            print("❌ Invalid input! Please enter a number between 0-12.")
            return None
    
    def create_process(self):
        """Create a new process interactively"""
        print("\n--- Create New Process ---")
        
        try:
            name = input("Process name: ").strip()
            if not name:
                name = f"Process_{len(self.processes) + 1}"
            
            burst_time = int(input("Burst time (seconds): "))
            if burst_time <= 0:
                raise ValueError("Burst time must be positive")
            
            size_kb = int(input("Process size (KB): "))
            if size_kb <= 0:
                raise ValueError("Process size must be positive")
            
            # Create process
            process = Process(name, burst_time, size_kb)
            
            # Add some instructions
            num_instructions = min(5, burst_time)  # Limit instructions
            print(f"Adding {num_instructions} instructions:")
            for i in range(num_instructions):
                instruction = input(f"Instruction {i+1} (or press Enter for default): ").strip()
                if not instruction:
                    instruction = f"Task_{i+1}"
                process.add_instruction(instruction)
            
            # Add to system
            self.processes.append(process)
            self.memory_manager.register_process(process)
            
            print(f"✅ Process created: {process}")
            
        except ValueError as e:
            print(f"❌ Error creating process: {e}")
        except KeyboardInterrupt:
            print("\n❌ Process creation cancelled")
    
    def list_processes(self):
        """List all created processes"""
        print("\n--- Process List ---")
        if not self.processes:
            print("No processes created yet.")
            return
        
        for i, process in enumerate(self.processes, 1):
            status = "Ready" if process.status == 'ready' else process.status.title()
            print(f"{i:2d}. {process} - Status: {status}")
            print(f"     Instructions: {len(process.instructions)}")
            print(f"     Page table: {len([p for p in process.page_table.values() if p[1] == 1])} pages loaded")
    
    def configure_memory_manager(self):
        """Configure memory manager settings"""
        print("\n--- Memory Manager Configuration ---")
        print(f"Current: {self.current_memory_algorithm} algorithm, {self.memory_frames} frames")
        
        # Choose algorithm
        print(f"Available algorithms: {SUPPORTED_REPLACEMENT_ALGORITHMS}")
        algorithm = input("Enter algorithm (FIFO/LRU) or press Enter to keep current: ").strip().upper()
        if algorithm and algorithm in SUPPORTED_REPLACEMENT_ALGORITHMS:
            self.current_memory_algorithm = algorithm
        elif algorithm and algorithm not in SUPPORTED_REPLACEMENT_ALGORITHMS:
            print(f"❌ Invalid algorithm. Using current: {self.current_memory_algorithm}")
        
        # Choose frame count
        try:
            frames = input("Enter number of frames (4-32) or press Enter to keep current: ").strip()
            if frames:
                frames = int(frames)
                if 4 <= frames <= 32:
                    self.memory_frames = frames
                else:
                    print("❌ Frame count must be between 4-32. Using current value.")
        except ValueError:
            print("❌ Invalid frame count. Using current value.")
        
        # Reinitialize memory manager
        self._initialize_memory_manager()
        print(f"✅ Memory manager configured: {self.current_memory_algorithm}, {self.memory_frames} frames")
    
    def configure_cpu_scheduler(self):
        """Configure CPU scheduler settings"""
        print("\n--- CPU Scheduler Configuration ---")
        print(f"Current: {self.current_cpu_algorithm} algorithm, quantum={self.time_quantum}s")
        
        # Choose algorithm
        print(f"Available algorithms: {SUPPORTED_ALGORITHMS}")
        algorithm = input("Enter algorithm (FCFS/RR) or press Enter to keep current: ").strip().upper()
        if algorithm and algorithm in SUPPORTED_ALGORITHMS:
            self.current_cpu_algorithm = algorithm
        elif algorithm and algorithm not in SUPPORTED_ALGORITHMS:
            print(f"❌ Invalid algorithm. Using current: {self.current_cpu_algorithm}")
        
        # Configure time quantum for Round Robin
        if self.current_cpu_algorithm == 'RR':
            try:
                quantum = input("Enter time quantum (1-10) or press Enter to keep current: ").strip()
                if quantum:
                    quantum = int(quantum)
                    if 1 <= quantum <= 10:
                        self.time_quantum = quantum
                    else:
                        print("❌ Quantum must be between 1-10. Using current value.")
            except ValueError:
                print("❌ Invalid quantum value. Using current value.")
        
        print(f"✅ CPU scheduler configured: {self.current_cpu_algorithm}, quantum={self.time_quantum}s")
    
    def run_fcfs_scheduling(self):
        """Run FCFS scheduling simulation"""
        if not self.processes:
            print("❌ No processes available. Create some processes first.")
            return
        
        print("\n--- FCFS Scheduling Simulation ---")
        scheduler = CPUScheduler(algorithm='FCFS')
        
        # Add all processes
        for process in self.processes:
            scheduler.add_process(process)
        
        # Run simulation
        result = scheduler.run_complete_simulation(self.memory_manager)
        
        # Ask if user wants to clear processes
        choice = input("\nClear processes after simulation? (y/N): ").strip().lower()
        if choice == 'y':
            self.clear_processes()
    
    def run_round_robin_scheduling(self):
        """Run Round Robin scheduling simulation"""
        if not self.processes:
            print("❌ No processes available. Create some processes first.")
            return
        
        print(f"\n--- Round Robin Scheduling Simulation (Quantum: {self.time_quantum}s) ---")
        scheduler = CPUScheduler(algorithm='RR', time_quantum=self.time_quantum)
        
        # Add all processes
        for process in self.processes:
            scheduler.add_process(process)
        
        # Run simulation
        result = scheduler.run_complete_simulation(self.memory_manager)
        
        # Ask if user wants to clear processes
        choice = input("\nClear processes after simulation? (y/N): ").strip().lower()
        if choice == 'y':
            self.clear_processes()
    
    def run_custom_simulation(self):
        """Run simulation with custom settings"""
        if not self.processes:
            print("❌ No processes available. Create some processes first.")
            return
        
        print("\n--- Custom Simulation ---")
        
        # Choose scheduling algorithm
        print(f"Available CPU algorithms: {SUPPORTED_ALGORITHMS}")
        cpu_algo = input("CPU algorithm (FCFS/RR): ").strip().upper()
        if cpu_algo not in SUPPORTED_ALGORITHMS:
            print("❌ Invalid algorithm, using FCFS")
            cpu_algo = 'FCFS'
        
        # Configure time quantum for RR
        quantum = self.time_quantum
        if cpu_algo == 'RR':
            try:
                quantum_input = input(f"Time quantum (current: {self.time_quantum}): ").strip()
                if quantum_input:
                    quantum = int(quantum_input)
            except ValueError:
                print(f"❌ Invalid quantum, using {self.time_quantum}")
        
        # Choose memory algorithm
        print(f"Available memory algorithms: {SUPPORTED_REPLACEMENT_ALGORITHMS}")
        mem_algo = input("Memory algorithm (FIFO/LRU): ").strip().upper()
        if mem_algo not in SUPPORTED_REPLACEMENT_ALGORITHMS:
            print("❌ Invalid algorithm, using current")
            mem_algo = self.current_memory_algorithm
        
        # Create temporary memory manager if different algorithm
        memory_manager = self.memory_manager
        if mem_algo != self.current_memory_algorithm:
            memory_manager = MemoryManager(total_frames=self.memory_frames, algorithm=mem_algo)
            for process in self.processes:
                memory_manager.register_process(process)
        
        # Create scheduler and run simulation
        scheduler = CPUScheduler(algorithm=cpu_algo, time_quantum=quantum)
        for process in self.processes:
            scheduler.add_process(process)
        
        result = scheduler.run_complete_simulation(memory_manager)
        
        # Show memory status
        memory_manager.display_memory_status()
    
    def show_memory_status(self):
        """Display current memory status"""
        print("\n--- Memory Status ---")
        self.memory_manager.display_memory_status()
    
    def show_system_statistics(self):
        """Display comprehensive system statistics"""
        print("\n--- System Statistics ---")
        
        # Process statistics
        print(f"Processes created: {len(self.processes)}")
        if self.processes:
            total_pages = sum(p.num_pages for p in self.processes)
            total_size = sum(p.process_size_kb for p in self.processes)
            print(f"Total process size: {total_size} KB")
            print(f"Total pages needed: {total_pages}")
            print(f"Memory utilization: {min(100, total_pages/self.memory_frames*100):.1f}%")
        
        # Memory statistics
        memory_stats = self.memory_manager.get_memory_statistics()
        if memory_stats['total_accesses'] > 0:
            print(f"\nMemory Access Statistics:")
            print(f"  Total accesses: {memory_stats['total_accesses']}")
            print(f"  Page hits: {memory_stats['page_hits']}")
            print(f"  Page faults: {memory_stats['page_faults']}")
            print(f"  Hit ratio: {memory_stats['hit_ratio']:.2%}")
        
        # System configuration
        print(f"\nSystem Configuration:")
        print(f"  Memory frames: {self.memory_frames}")
        print(f"  Memory algorithm: {self.current_memory_algorithm}")
        print(f"  CPU algorithm: {self.current_cpu_algorithm}")
        print(f"  Time quantum: {self.time_quantum}s")
    
    def run_demonstration_scenarios(self):
        """Run predefined demonstration scenarios"""
        print("\n--- Demonstration Scenarios ---")
        print("1. Round Robin: Process A (20s) vs Process B (17s)")
        print("2. FCFS vs Round Robin Comparison")
        print("3. Memory Page Replacement Comparison")
        print("4. Memory Locality of Reference")
        
        try:
            choice = int(input("Choose demo (1-4): "))
            
            if choice == 1:
                self._demo_round_robin_comparison()
            elif choice == 2:
                self._demo_fcfs_vs_rr()
            elif choice == 3:
                self._demo_memory_algorithms()
            elif choice == 4:
                self._demo_memory_locality()
            else:
                print("❌ Invalid choice")
                
        except ValueError:
            print("❌ Invalid input")
    
    def _demo_round_robin_comparison(self):
        """Demo: Round Robin with specific processes"""
        print("\n🎯 Demo: Round Robin - Process A (20s) vs Process B (17s)")
        
        # Clear current processes
        self.processes.clear()
        Process.reset_id_counter()
        
        # Create specific processes
        process_a = Process("Process_A", 20, 8)
        process_b = Process("Process_B", 17, 6)
        
        # Add instructions
        for i in range(5):
            process_a.add_instruction(f"A_task_{i+1}")
            process_b.add_instruction(f"B_task_{i+1}")
        
        self.processes = [process_a, process_b]
        
        # Register with memory manager
        self._initialize_memory_manager()
        
        # Run Round Robin with quantum 3
        scheduler = CPUScheduler(algorithm='RR', time_quantum=3)
        scheduler.add_process(process_a)
        scheduler.add_process(process_b)
        
        result = scheduler.run_complete_simulation(self.memory_manager)
        self.memory_manager.display_memory_status()
    
    def _demo_fcfs_vs_rr(self):
        """Demo: FCFS vs Round Robin comparison"""
        print("\n🎯 Demo: FCFS vs Round Robin Comparison")
        
        # Create test processes
        processes_data = [("Short", 3, 4), ("Medium", 7, 4), ("Long", 5, 4)]
        
        for algorithm in ['FCFS', 'RR']:
            print(f"\n--- {algorithm} Scheduling ---")
            
            # Reset and create processes
            Process.reset_id_counter()
            test_processes = []
            
            for name, burst, size in processes_data:
                process = Process(name, burst, size)
                for i in range(2):
                    process.add_instruction(f"{name}_task_{i+1}")
                test_processes.append(process)
            
            # Create fresh memory manager
            memory = MemoryManager(total_frames=8, algorithm='FIFO')
            for process in test_processes:
                memory.register_process(process)
            
            # Run simulation
            scheduler = CPUScheduler(algorithm=algorithm, time_quantum=2)
            for process in test_processes:
                scheduler.add_process(process)
            
            result = scheduler.run_complete_simulation(memory)
    
    def _demo_memory_algorithms(self):
        """Demo: Memory page replacement algorithms"""
        print("\n🎯 Demo: FIFO vs LRU Page Replacement")
        
        access_pattern = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        
        for algorithm in ['FIFO', 'LRU']:
            print(f"\n--- {algorithm} Algorithm ---")
            
            Process.reset_id_counter()
            process = Process("TestProcess", 15, 20)  # 5 pages
            memory = MemoryManager(total_frames=3, algorithm=algorithm)
            memory.register_process(process)
            
            print(f"Access pattern: {access_pattern}")
            
            for i, page in enumerate(access_pattern):
                page_index = page - 1
                result = memory.access_page(process, page_index)
                print(f"Access {page}: {result['status']}")
            
            stats = memory.get_memory_statistics()
            print(f"Hit ratio: {stats['hit_ratio']:.2%}")
    
    def _demo_memory_locality(self):
        """Demo: Locality of reference effects"""
        print("\n🎯 Demo: Locality of Reference")
        
        patterns = {
            "Sequential": [1, 2, 3, 1, 2, 3, 1, 2, 3],
            "Random": [1, 5, 2, 4, 3, 1, 5, 2, 4]
        }
        
        for pattern_name, pattern in patterns.items():
            print(f"\n--- {pattern_name} Access Pattern ---")
            print(f"Pattern: {pattern}")
            
            for algorithm in ['FIFO', 'LRU']:
                Process.reset_id_counter()
                process = Process("TestProcess", 15, 20)
                memory = MemoryManager(total_frames=3, algorithm=algorithm)
                memory.register_process(process)
                
                for page in pattern:
                    memory.access_page(process, page - 1)
                
                stats = memory.get_memory_statistics()
                print(f"{algorithm}: {stats['hit_ratio']:.2%} hit ratio")
    
    def clear_processes(self):
        """Clear all processes"""
        self.processes.clear()
        Process.reset_id_counter()
        self._initialize_memory_manager()
        print("✅ All processes cleared")
    
    def show_system_information(self):
        """Display system information"""
        print("\n--- System Information ---")
        
        # Validate configuration
        config_errors = validate_configuration()
        if config_errors:
            print("⚠️  Configuration Issues:")
            for error in config_errors:
                print(f"  - {error}")
        else:
            print("✅ System configuration valid")
        
        # System info
        info = get_system_info()
        print(f"\nSystem Parameters:")
        print(f"  Page size: {info['page_size']} bytes")
        print(f"  Frame size: {info['frame_size']} bytes")
        print(f"  Default memory: {info['default_memory_size']} KB")
        print(f"  Default frames: {info['default_frame_count']}")
        print(f"  Default quantum: {info['default_time_quantum']} seconds")
        
        print(f"\nSupported Algorithms:")
        print(f"  CPU: {', '.join(info['supported_cpu_algorithms'])}")
        print(f"  Memory: {', '.join(info['supported_memory_algorithms'])}")
        
        print(f"\nLimits:")
        print(f"  Max processes: {info['max_processes']}")
        print(f"  Max simulation time: {info['max_simulation_time']} seconds")
    
    def run(self):
        """Main application loop"""
        print("🚀 Operating System Simulator v2.0 Starting...")
        
        # Validate system configuration
        config_errors = validate_configuration()
        if config_errors:
            print("⚠️  Configuration issues detected:")
            for error in config_errors:
                print(f"  - {error}")
            print()
        
        try:
            while True:
                self.display_main_menu()
                choice = self.get_user_choice()
                
                if choice == 0:
                    print("👋 Thank you for using OS Simulator v2.0!")
                    break
                elif choice == 1:
                    self.create_process()
                elif choice == 2:
                    self.list_processes()
                elif choice == 3:
                    self.configure_memory_manager()
                elif choice == 4:
                    self.configure_cpu_scheduler()
                elif choice == 5:
                    self.run_fcfs_scheduling()
                elif choice == 6:
                    self.run_round_robin_scheduling()
                elif choice == 7:
                    self.run_custom_simulation()
                elif choice == 8:
                    self.show_memory_status()
                elif choice == 9:
                    self.show_system_statistics()
                elif choice == 10:
                    self.run_demonstration_scenarios()
                elif choice == 11:
                    self.clear_processes()
                elif choice == 12:
                    self.show_system_information()
                elif choice is not None:
                    print("❌ Invalid choice. Please select 0-12.")
                
                # Pause for user to read output
                if choice not in [None, 0]:
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 OS Simulator terminated by user. Goodbye!")
        except Exception as e:
            print(f"\n💥 Unexpected error: {e}")
            print("Please report this issue to the development team.")

def main():
    """Entry point for the application"""
    app = OSSimulator()
    app.run()

if __name__ == "__main__":
    main()
