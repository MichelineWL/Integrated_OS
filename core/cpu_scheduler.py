"""
CPU Scheduler - Process Scheduling with FCFS and Round Robin
Implements accurate time-based scheduling algorithms
"""

from collections import deque
from .models import Statistics

class CPUScheduler:
    """
    Advanced CPU Scheduler with proper time quantum management
    """
    def __init__(self, algorithm='FCFS', time_quantum=3):
        if algorithm.upper() not in ['FCFS', 'RR']:
            raise ValueError("Algorithm must be 'FCFS' or 'RR'")
        
        self.algorithm = algorithm.upper()
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.statistics = Statistics()
        
        # Scheduler state
        self.current_process = None
        self.quantum_counter = 0
        self.total_time = 0
        
        # Process tracking
        self.completed_processes = []
        self.process_start_times = {}
        self.process_completion_times = {}
    
    def add_process(self, process):
        """Add process to ready queue"""
        process.status = 'ready'
        self.ready_queue.append(process)
        
        # Record arrival time (for statistics)
        if process.process_id not in self.process_start_times:
            self.process_start_times[process.process_id] = self.total_time
        
        print(f"Process {process.name} added to {self.algorithm} queue")
    
    def select_next_process(self):
        """
        Select next process based on scheduling algorithm
        
        Returns:
            Process object or None if no process available
        """
        if self.algorithm == 'FCFS':
            return self._select_fcfs()
        elif self.algorithm == 'RR':
            return self._select_rr()
        return None
    
    def tick(self):
        """Update scheduler state each time unit"""
        self.total_time += 1
        
        if self.algorithm == 'RR' and self.quantum_counter > 0:
            self.quantum_counter -= 1
    
    def _select_fcfs(self):
        """First Come First Serve selection logic"""
        # If no current process or current process finished
        if (self.current_process is None or 
            self.current_process.burst_time_remaining <= 0):
            
            # Handle process completion
            if self.current_process and self.current_process.burst_time_remaining <= 0:
                self._complete_process(self.current_process)
            
            # Select next process from ready queue
            if self.ready_queue:
                self.current_process = self.ready_queue.popleft()
                self.current_process.status = 'running'
                print(f"  → {self.current_process.name} started execution")
            else:
                self.current_process = None
        
        return self.current_process
    
    def _select_rr(self):
        """Round Robin selection logic"""
        quantum_expired = self.quantum_counter <= 0
        process_finished = (self.current_process is not None and 
                           self.current_process.burst_time_remaining <= 0)
        
        need_new_process = (self.current_process is None or 
                           quantum_expired or process_finished)
        
        if need_new_process:
            # Handle process completion
            if process_finished:
                self._complete_process(self.current_process)
            
            # Handle quantum expiration (preemption)
            elif self.current_process and quantum_expired and not process_finished:
                print(f"  → {self.current_process.name} preempted (quantum expired)")
                self.current_process.status = 'ready'
                self.ready_queue.append(self.current_process)
                self.statistics.increment_context_switches()
            
            # Select next process
            if self.ready_queue:
                self.current_process = self.ready_queue.popleft()
                self.current_process.status = 'running'
                self.quantum_counter = self.time_quantum
                
                if not process_finished:  # Only print if it's a new process or context switch
                    print(f"  → {self.current_process.name} started/resumed execution")
            else:
                self.current_process = None
        
        return self.current_process
    
    def _complete_process(self, process):
        """Handle process completion"""
        process.status = 'terminated'
        self.completed_processes.append(process)
        self.process_completion_times[process.process_id] = self.total_time
        
        # Calculate process times for statistics
        arrival_time = self.process_start_times.get(process.process_id, 0)
        turnaround_time = self.total_time - arrival_time
        waiting_time = turnaround_time - process.burst_time_total
        
        self.statistics.add_process_completion(waiting_time, turnaround_time)
        
        print(f"  ✓ {process.name} completed (Turnaround: {turnaround_time}s, Waiting: {waiting_time}s)")
    
    def run_complete_simulation(self, memory_manager=None):
        """
        Run complete scheduling simulation until all processes finish
        
        Args:
            memory_manager: Optional memory manager for memory access simulation
            
        Returns:
            dict: Simulation results including execution order and statistics
        """
        print(f"\n{'='*60}")
        print(f"    {self.algorithm} SCHEDULING SIMULATION STARTED")
        if self.algorithm == 'RR':
            print(f"    Time Quantum: {self.time_quantum}")
        print(f"{'='*60}")
        
        execution_log = []
        memory_access_log = []
        
        # Continue until no processes remain
        while self.ready_queue or self.current_process:
            # Select process for this time slice
            current_process = self.select_next_process()
            
            if current_process:
                execution_log.append(current_process.process_id)
                
                print(f"[Time {self.total_time:3d}] {current_process.name} "
                      f"(Remaining: {current_process.burst_time_remaining}s)", end="")
                
                if self.algorithm == 'RR':
                    print(f" [Quantum: {self.quantum_counter}]", end="")
                print()
                
                # Simulate memory access if memory manager provided
                if memory_manager:
                    page_to_access = current_process.get_next_page_to_access()
                    if page_to_access is not None:
                        result = memory_manager.access_page(current_process, page_to_access)
                        memory_access_log.append({
                            'time': self.total_time,
                            'process': current_process.process_id,
                            'page': page_to_access,
                            'result': result['status']
                        })
                        
                        if result['status'] == 'FAULT':
                            print(f"    Page {page_to_access}: FAULT → Frame {result['loaded_into_frame']}")
                            if result['evicted_page_info']:
                                evicted = result['evicted_page_info']
                                print(f"    Evicted: {evicted['process_id']}, Page {evicted['page_number']}")
                        else:
                            print(f"    Page {page_to_access}: HIT → Frame {result['frame_number']}")
                
                # Execute one unit of work
                current_process.burst_time_remaining -= 1
                
                # Execute instruction if available
                if current_process.instructions:
                    current_process.execute_instruction()
            else:
                print(f"[Time {self.total_time:3d}] CPU IDLE")
            
            # Update scheduler state
            self.tick()
        
        # Simulation completed
        print(f"\n{'='*60}")
        print(f"    {self.algorithm} SCHEDULING SIMULATION COMPLETED")
        print(f"    Total Execution Time: {self.total_time}")
        print(f"{'='*60}")
        
        # Display process completion summary
        print(f"\nProcess Completion Summary:")
        for i, process in enumerate(self.completed_processes, 1):
            arrival = self.process_start_times.get(process.process_id, 0)
            completion = self.process_completion_times.get(process.process_id, 0)
            turnaround = completion - arrival
            waiting = turnaround - process.burst_time_total
            print(f"{i}. {process.name}: Arrival={arrival}, Completion={completion}, "
                  f"Turnaround={turnaround}, Waiting={waiting}")
        
        # Display scheduling statistics
        if self.completed_processes:
            avg_waiting = self.statistics.get_average_waiting_time()
            avg_turnaround = self.statistics.get_average_turnaround_time()
            print(f"\nScheduling Performance:")
            print(f"  Average Waiting Time: {avg_waiting:.2f}s")
            print(f"  Average Turnaround Time: {avg_turnaround:.2f}s")
            if self.algorithm == 'RR':
                print(f"  Total Context Switches: {self.statistics.context_switches}")
        
        return {
            'execution_order': execution_log,
            'total_time': self.total_time,
            'memory_accesses': memory_access_log,
            'completed_processes': len(self.completed_processes),
            'average_waiting_time': self.statistics.get_average_waiting_time(),
            'average_turnaround_time': self.statistics.get_average_turnaround_time(),
            'context_switches': self.statistics.context_switches
        }
    
    def step_simulation(self, memory_manager=None):
        """
        Run one step of simulation (for interactive/step-by-step execution)
        
        Returns:
            dict: Current step information
        """
        current_process = self.select_next_process()
        step_info = {
            'time': self.total_time,
            'current_process': current_process.process_id if current_process else None,
            'ready_queue': [p.process_id for p in self.ready_queue],
            'completed': len(self.completed_processes)
        }
        
        if current_process:
            # Memory access simulation
            if memory_manager:
                page_to_access = current_process.get_next_page_to_access()
                if page_to_access is not None:
                    result = memory_manager.access_page(current_process, page_to_access)
                    step_info['memory_access'] = {
                        'page': page_to_access,
                        'result': result['status'],
                        'frame': result.get('loaded_into_frame') or result.get('frame_number')
                    }
            
            # Execute work
            current_process.burst_time_remaining -= 1
            
            if current_process.instructions:
                current_process.execute_instruction()
        
        self.tick()
        return step_info
    
    def is_simulation_complete(self):
        """Check if simulation is complete"""
        return len(self.ready_queue) == 0 and self.current_process is None
    
    def reset(self):
        """Reset scheduler to initial state"""
        self.ready_queue.clear()
        self.current_process = None
        self.quantum_counter = 0
        self.total_time = 0
        self.completed_processes.clear()
        self.process_start_times.clear()
        self.process_completion_times.clear()
        self.statistics.reset()
        print(f"{self.algorithm} scheduler reset")
    
    def get_scheduler_status(self):
        """Get current scheduler status"""
        return {
            'algorithm': self.algorithm,
            'time_quantum': self.time_quantum if self.algorithm == 'RR' else None,
            'current_time': self.total_time,
            'current_process': self.current_process.process_id if self.current_process else None,
            'ready_queue_size': len(self.ready_queue),
            'completed_processes': len(self.completed_processes),
            'quantum_remaining': self.quantum_counter if self.algorithm == 'RR' else None
        }
