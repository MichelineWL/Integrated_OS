"""
Enhanced CPU Scheduler with Real-time Execution and Interactive Controls
Integrates best features from aiss: real-time delays, pause/resume, hex address support
"""

import time
from collections import deque
from typing import List, Dict, Optional
from .enhanced_models import Process, Statistics
from .enhanced_memory_manager import EnhancedMemoryManager

class EnhancedCPUScheduler:
    """Enhanced CPU Scheduler with real-time execution and interactive controls"""
    
    def __init__(self, algorithm: str = 'FCFS', time_quantum: int = 3):
        self.algorithm = algorithm.upper()
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.completed_processes = []
        self.statistics = Statistics()
        
        # Time tracking
        self.total_time = 0
        self.process_start_times = {}
        self.process_completion_times = {}
        
        # Interactive controls (from aiss)
        self.is_running = False
        self.is_paused = False
        self.step_mode = False
        self.execution_delay = 1.0  # seconds per instruction
        
        # Enhanced tracking
        self.current_process = None
        self.quantum_remaining = 0
        self.context_switches = 0
        
        print(f"Enhanced CPU Scheduler initialized: {self.algorithm} algorithm")
        if algorithm == 'RR':
            print(f"Time quantum: {self.time_quantum}s")
    
    def add_process(self, process: Process):
        """Add a process to the ready queue"""
        self.ready_queue.append(process)
        self.statistics.total_processes += 1
        process.state = "READY"
        print(f"Process {process.name} (UUID: {process.process_id}) added to {self.algorithm} queue")
    
    def set_execution_delay(self, delay: float):
        """Set delay between instruction executions (real-time simulation)"""
        self.execution_delay = delay
        print(f"Execution delay set to {delay}s per instruction")
    
    def pause_simulation(self):
        """Pause the simulation (from aiss)"""
        self.is_paused = True
        print("\\n[PAUSED] CPU simulation paused. Call resume_simulation() to continue.")
    
    def resume_simulation(self):
        """Resume the simulation (from aiss)"""
        self.is_paused = False
        print("\\n[RESUMED] CPU simulation resumed.")
    
    def enable_step_mode(self):
        """Enable step-by-step execution"""
        self.step_mode = True
        print("\\n[STEP MODE] Enabled. Press Enter for each instruction.")
    
    def disable_step_mode(self):
        """Disable step-by-step execution"""
        self.step_mode = False
        print("\\n[CONTINUOUS MODE] Step mode disabled.")
    
    def _check_interactive_controls(self):
        """Check and handle interactive controls"""
        while self.is_paused:
            time.sleep(0.1)
        
        if self.step_mode:
            input("Press Enter to execute next instruction...")
    
    def _execute_with_delay(self):
        """Execute with real-time delay"""
        if self.execution_delay > 0:
            time.sleep(self.execution_delay)
    
    def run_realtime_simulation(self, memory_manager: Optional[EnhancedMemoryManager] = None) -> Dict:
        """
        Run complete simulation with real-time execution and enhanced features
        Integrates hex address support and interactive controls
        """
        print(f"\\n{'='*60}")
        print(f"    ENHANCED {self.algorithm} SCHEDULING SIMULATION")
        if self.algorithm == 'RR':
            print(f"    Time Quantum: {self.time_quantum}s")
        print(f"    Real-time Execution: {self.execution_delay}s per instruction")
        print(f"{'='*60}")
        
        self.is_running = True
        self.statistics.reset()
        self.statistics.simulation_start_time = time.time()
        
        # Initialize processes
        for process in list(self.ready_queue):
            process.reset_for_simulation()
            self.process_start_times[process.process_id] = 0
        
        # Execution logs
        execution_log = []
        memory_access_log = []
        hex_execution_log = []
        
        # Run simulation
        if self.algorithm == 'FCFS':
            result = self._run_fcfs_realtime(memory_manager, execution_log, memory_access_log, hex_execution_log)
        elif self.algorithm == 'RR':
            result = self._run_rr_realtime(memory_manager, execution_log, memory_access_log, hex_execution_log)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        self.statistics.simulation_end_time = time.time()
        
        # Enhanced result with comprehensive data
        enhanced_result = {
            'execution_order': execution_log,
            'hex_execution_log': hex_execution_log,
            'memory_accesses': memory_access_log,
            'total_time': self.total_time,
            'completed_processes': len(self.completed_processes),
            'average_waiting_time': self.statistics.get_average_waiting_time(),
            'average_turnaround_time': self.statistics.get_average_turnaround_time(),
            'context_switches': self.statistics.context_switches,
            'overall_hit_ratio': self.statistics.get_overall_hit_ratio(),
            'simulation_duration': self.statistics.simulation_end_time - self.statistics.simulation_start_time
        }
        
        # Clean up process memory if memory manager provided
        if memory_manager:
            print(f"\\n{'='*60}")
            print(f"    MEMORY CLEANUP PHASE")
            print(f"{'='*60}")
            for process in self.completed_processes:
                memory_manager.deallocate_process(process)
        
        self._display_enhanced_summary(enhanced_result)
        return enhanced_result
    
    def _run_fcfs_realtime(self, memory_manager, execution_log, memory_access_log, hex_execution_log) -> Dict:
        """Run FCFS with real-time execution and enhanced features"""
        print(f"\\n{'='*60}")
        print(f"    FCFS SCHEDULING SIMULATION STARTED")
        print(f"{'='*60}")
        
        while self.ready_queue and self.is_running:
            current_process = self.ready_queue.popleft()
            current_process.state = "RUNNING"
            self.current_process = current_process
            
            print(f"  → {current_process.name} started execution")
            
            while (current_process.remaining_time > 0 and 
                   current_process.current_instruction < len(current_process.instructions) and 
                   self.is_running):
                
                self._check_interactive_controls()
                
                # Display current state
                instruction_display = ""
                if current_process.current_instruction < len(current_process.instructions):
                    instruction_display = f"\\n    Executing: {current_process.instructions[current_process.current_instruction]}"
                
                print(f"[Time {self.total_time:3d}] {current_process.name} (Remaining: {current_process.remaining_time}s){instruction_display}")
                
                # Memory access with hex address support
                if memory_manager:
                    # Get current hex address
                    hex_addr = current_process.get_current_hex_address()
                    page_result = memory_manager.access_hex_address(current_process, hex_addr)
                    
                    print(f"    Address: {hex_addr} → Page {current_process.get_current_page()}: {page_result['status']}", end="")
                    if page_result['frame'] is not None:
                        print(f" → Frame {page_result['frame']}")
                        if page_result['physical_address']:
                            print(f"    Physical: {page_result['physical_address']}")
                    else:
                        print(" → Failed")
                    
                    memory_access_log.append(page_result)
                    hex_execution_log.append({
                        'time': self.total_time,
                        'process': current_process.simple_id,
                        'hex_address': hex_addr,
                        'physical_address': page_result.get('physical_address'),
                        'status': page_result['status']
                    })
                    
                    if page_result['evicted_page_info']:
                        evicted = page_result['evicted_page_info']
                        print(f"    Evicted: Process {evicted['process_id']}, Page {evicted['page_number']}")
                
                # Execute instruction
                current_process.execute_instruction()
                execution_log.append(current_process.simple_id)
                
                # Update time and state
                self.total_time += 1
                self._execute_with_delay()
            
            # Process completed
            current_process.state = "TERMINATED"
            self.completed_processes.append(current_process)
            self.process_completion_times[current_process.process_id] = self.total_time
            self.statistics.record_process_completion(current_process, self.total_time)
            
            # Calculate and display completion stats
            arrival_time = self.process_start_times.get(current_process.process_id, 0)
            turnaround_time = self.total_time - arrival_time
            waiting_time = turnaround_time - current_process.burst_time_total
            
            print(f"  ✓ {current_process.name} completed (Turnaround: {turnaround_time}s, Waiting: {waiting_time}s)")
        
        # Final time increment
        if self.is_running:
            print(f"[Time {self.total_time:3d}] CPU IDLE")
            self.total_time += 1
        
        return {'algorithm': 'FCFS'}
    
    def _run_rr_realtime(self, memory_manager, execution_log, memory_access_log, hex_execution_log) -> Dict:
        """Run Round Robin with real-time execution and enhanced features"""
        print(f"\\n{'='*60}")
        print(f"    RR SCHEDULING SIMULATION STARTED")
        print(f"    Time Quantum: {self.time_quantum}")
        print(f"{'='*60}")
        
        # Initialize remaining times
        for process in list(self.ready_queue):
            process.remaining_time = process.burst_time_total
        
        while self.ready_queue and self.is_running:
            current_process = self.ready_queue.popleft()
            current_process.state = "RUNNING"
            self.current_process = current_process
            self.quantum_remaining = self.time_quantum
            
            print(f"  → {current_process.name} started/resumed execution")
            
            # Execute for time quantum or until completion
            while (self.quantum_remaining > 0 and 
                   current_process.remaining_time > 0 and 
                   current_process.current_instruction < len(current_process.instructions) and 
                   self.is_running):
                
                self._check_interactive_controls()
                
                # Display current state
                instruction_display = ""
                if current_process.current_instruction < len(current_process.instructions):
                    instruction_display = f"\\n    Executing: {current_process.instructions[current_process.current_instruction]}"
                
                print(f"[Time {self.total_time:3d}] {current_process.name} (Remaining: {current_process.remaining_time}s) [Quantum: {self.quantum_remaining}]{instruction_display}")
                
                # Memory access with hex address support
                if memory_manager:
                    hex_addr = current_process.get_current_hex_address()
                    page_result = memory_manager.access_hex_address(current_process, hex_addr)
                    
                    print(f"    Address: {hex_addr} → Page {current_process.get_current_page()}: {page_result['status']}", end="")
                    if page_result['frame'] is not None:
                        print(f" → Frame {page_result['frame']}")
                    else:
                        print(" → Failed")
                    
                    memory_access_log.append(page_result)
                    hex_execution_log.append({
                        'time': self.total_time,
                        'process': current_process.simple_id,
                        'hex_address': hex_addr,
                        'physical_address': page_result.get('physical_address'),
                        'status': page_result['status']
                    })
                    
                    if page_result['evicted_page_info']:
                        evicted = page_result['evicted_page_info']
                        print(f"    Evicted: Process {evicted['process_id']}, Page {evicted['page_number']}")
                
                # Execute instruction
                current_process.execute_instruction()
                execution_log.append(current_process.simple_id)
                
                # Update counters
                self.quantum_remaining -= 1
                self.total_time += 1
                self._execute_with_delay()
            
            # Check process state
            if current_process.remaining_time <= 0 or current_process.current_instruction >= len(current_process.instructions):
                # Process completed
                current_process.state = "TERMINATED"
                self.completed_processes.append(current_process)
                self.process_completion_times[current_process.process_id] = self.total_time
                self.statistics.record_process_completion(current_process, self.total_time)
                
                arrival_time = self.process_start_times.get(current_process.process_id, 0)
                turnaround_time = self.total_time - arrival_time
                waiting_time = turnaround_time - current_process.burst_time_total
                
                print(f"  ✓ {current_process.name} completed (Turnaround: {turnaround_time}s, Waiting: {waiting_time}s)")
            else:
                # Quantum expired, preempt process
                current_process.state = "READY"
                self.ready_queue.append(current_process)
                self.statistics.context_switches += 1
                print(f"  → {current_process.name} preempted (quantum expired)")
        
        # Final time increment
        if self.is_running:
            print(f"[Time {self.total_time:3d}] CPU IDLE")
            self.total_time += 1
        
        return {'algorithm': 'RR'}
    
    def _display_enhanced_summary(self, result: Dict):
        """Display comprehensive simulation summary"""
        print(f"\\n{'='*60}")
        print(f"    {self.algorithm} SCHEDULING SIMULATION COMPLETED")
        print(f"    Total Execution Time: {result['total_time']}")
        print(f"{'='*60}")
        
        # Process completion summary
        print(f"\\nProcess Completion Summary:")
        for i, process in enumerate(self.completed_processes, 1):
            arrival = self.process_start_times.get(process.process_id, 0)
            completion = self.process_completion_times.get(process.process_id, 0)
            turnaround = completion - arrival
            waiting = turnaround - process.burst_time_total
            print(f"{i}. {process.name}: Arrival={arrival}, Completion={completion}, "
                  f"Turnaround={turnaround}, Waiting={waiting}")
        
        # Performance statistics
        print(f"\\nScheduling Performance:")
        print(f"  Average Waiting Time: {result['average_waiting_time']:.2f}s")
        print(f"  Average Turnaround Time: {result['average_turnaround_time']:.2f}s")
        if self.algorithm == 'RR':
            print(f"  Total Context Switches: {result['context_switches']}")
        
        # Memory statistics if available
        if result['memory_accesses']:
            print(f"\\nMemory Performance:")
            print(f"  Overall Hit Ratio: {result['overall_hit_ratio']:.2f}%")
            print(f"  Total Memory Accesses: {len(result['memory_accesses'])}")
        
        # Execution analysis
        if result['hex_execution_log']:
            print(f"\\nHex Address Execution Sample (first 5):")
            for i, log_entry in enumerate(result['hex_execution_log'][:5]):
                print(f"  [{log_entry['time']}s] {log_entry['process']}: {log_entry['hex_address']} → {log_entry['physical_address']} ({log_entry['status']})")
        
        print(f"\\nSimulation completed in {result['simulation_duration']:.2f} seconds real-time.")
    
    def get_current_state(self) -> Dict:
        """Get current scheduler state for monitoring"""
        return {
            'algorithm': self.algorithm,
            'current_time': self.total_time,
            'current_process': self.current_process.name if self.current_process else None,
            'ready_queue_size': len(self.ready_queue),
            'completed_processes': len(self.completed_processes),
            'is_running': self.is_running,
            'is_paused': self.is_paused,
            'quantum_remaining': self.quantum_remaining if self.algorithm == 'RR' else None
        }
