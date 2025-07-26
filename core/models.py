"""
Core Models for Operating System Simulator
Foundational classes for Process, Memory, and Statistics
Version: 2.0 - Improved Architecture
"""

import uuid
import random
import math

# System Constants
PAGE_SIZE = 4096  # 4KB per page
FRAME_SIZE = PAGE_SIZE  # Frame size equals page size

class Process:
    """
    Enhanced Process class with realistic virtual memory simulation
    """
    _id_counter = 0
    
    def __init__(self, name, burst_time, process_size_kb):
        # Basic process information
        self.process_id = f"P{Process._id_counter}"
        Process._id_counter += 1
        self.name = name
        self.burst_time_total = burst_time
        self.burst_time_remaining = burst_time
        
        # Memory management
        process_size_bytes = process_size_kb * 1024
        self.process_size_kb = process_size_kb
        self.num_pages = math.ceil(process_size_bytes / PAGE_SIZE)
        
        # Page table: {page_number: [frame_number, valid_bit]}
        # valid_bit: 0 = not in memory, 1 = in memory
        self.page_table = {i: [None, 0] for i in range(self.num_pages)}
        
        # Generate realistic page access sequence
        # Processes tend to access pages with some locality of reference
        self.page_access_sequence = self._generate_page_access_sequence()
        self.access_step = 0
        
        # Process state and instructions
        self.status = 'ready'  # ready, running, terminated
        self.instructions = []
        
        # Compatibility with old interface
        self.remaining_time = burst_time
        self.pages_needed = self.num_pages
    
    def _generate_page_access_sequence(self):
        """Generate page access sequence with locality of reference"""
        sequence = []
        current_page = 0
        
        for _ in range(self.burst_time_total):
            # 70% chance to access nearby pages (locality of reference)
            # 30% chance to access random page
            if random.random() < 0.7 and self.num_pages > 1:
                # Access nearby page
                nearby_pages = []
                for offset in [-1, 0, 1]:
                    page = current_page + offset
                    if 0 <= page < self.num_pages:
                        nearby_pages.append(page)
                current_page = random.choice(nearby_pages)
            else:
                # Random access
                current_page = random.randint(0, self.num_pages - 1)
            
            sequence.append(current_page)
        
        return sequence
    
    def get_next_page_to_access(self):
        """Get next page to access from sequence"""
        if self.access_step < len(self.page_access_sequence):
            page = self.page_access_sequence[self.access_step]
            self.access_step += 1
            return page
        return None
    
    def add_instruction(self, instruction):
        """Add instruction to process"""
        self.instructions.append(instruction)
    
    def execute_instruction(self):
        """Execute one instruction"""
        if self.instructions:
            instruction = self.instructions.pop(0)
            print(f"    Executing: {instruction}")
            return True
        return False
    
    def get_pages_count(self):
        """Get number of pages needed (compatibility)"""
        return self.num_pages
    
    @classmethod
    def reset_id_counter(cls):
        """Reset ID counter for testing"""
        cls._id_counter = 0
    
    # Properties for backward compatibility
    @property
    def pid(self):
        return self.process_id
    
    @property
    def besar_proses(self):
        return self.process_size_kb
    
    @property
    def burst_time(self):
        return self.burst_time_total
    
    def __str__(self):
        return (f"Process(id={self.process_id}, name={self.name}, "
                f"pages={self.num_pages}, remaining={self.burst_time_remaining}s)")
    
    def __repr__(self):
        return self.__str__()


class PhysicalMemory:
    """
    Physical Memory representation with frame management
    """
    def __init__(self, total_frames):
        self.total_frames = total_frames
        self.frames = [None] * total_frames
    
    def is_full(self):
        """Check if all frames are occupied"""
        return None not in self.frames
    
    def get_empty_frame_index(self):
        """Get index of first empty frame"""
        try:
            return self.frames.index(None)
        except ValueError:
            return -1
    
    def get_used_frames_count(self):
        """Get number of used frames"""
        return len([f for f in self.frames if f is not None])
    
    def get_free_frames_count(self):
        """Get number of free frames"""
        return len([f for f in self.frames if f is None])
    
    def __str__(self):
        used = self.get_used_frames_count()
        return f"PhysicalMemory(total={self.total_frames}, used={used}, free={self.total_frames-used})"


class Statistics:
    """
    Statistics tracking for system performance
    """
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all statistics"""
        self.total_accesses = 0
        self.page_hits = 0
        self.page_faults = 0
        self.context_switches = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.completed_processes = 0
    
    def increment_hits(self):
        """Record a page hit"""
        self.total_accesses += 1
        self.page_hits += 1
    
    def increment_faults(self):
        """Record a page fault"""
        self.total_accesses += 1
        self.page_faults += 1
    
    def increment_context_switches(self):
        """Record a context switch"""
        self.context_switches += 1
    
    def add_process_completion(self, waiting_time, turnaround_time):
        """Record process completion times"""
        self.total_waiting_time += waiting_time
        self.total_turnaround_time += turnaround_time
        self.completed_processes += 1
    
    def get_hit_ratio(self):
        """Calculate hit ratio"""
        if self.total_accesses == 0:
            return 0.0
        return self.page_hits / self.total_accesses
    
    def get_average_waiting_time(self):
        """Calculate average waiting time"""
        if self.completed_processes == 0:
            return 0.0
        return self.total_waiting_time / self.completed_processes
    
    def get_average_turnaround_time(self):
        """Calculate average turnaround time"""
        if self.completed_processes == 0:
            return 0.0
        return self.total_turnaround_time / self.completed_processes
    
    def display_report(self):
        """Display comprehensive statistics report"""
        print("\n" + "="*50)
        print("           SYSTEM PERFORMANCE REPORT")
        print("="*50)
        
        # Memory Statistics
        print("Memory Management:")
        print(f"  Total Memory Accesses: {self.total_accesses}")
        print(f"  Page Hits: {self.page_hits}")
        print(f"  Page Faults: {self.page_faults}")
        print(f"  Hit Ratio: {self.get_hit_ratio():.2%}")
        
        # CPU Scheduling Statistics
        print(f"\nCPU Scheduling:")
        print(f"  Context Switches: {self.context_switches}")
        print(f"  Completed Processes: {self.completed_processes}")
        if self.completed_processes > 0:
            print(f"  Average Waiting Time: {self.get_average_waiting_time():.2f}s")
            print(f"  Average Turnaround Time: {self.get_average_turnaround_time():.2f}s")
        
        print("="*50)
    
    def __str__(self):
        hit_ratio = self.get_hit_ratio() * 100
        return (f"Statistics(Accesses={self.total_accesses}, "
                f"Hits={self.page_hits}, Faults={self.page_faults}, "
                f"HitRatio={hit_ratio:.1f}%)")
