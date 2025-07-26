"""
Enhanced Process Model with Hex Address Support and UUID
Integrates best features from aiss into improved_os architecture
"""

import uuid
import random
import time
from typing import List, Dict, Optional, Union

# Configuration constants
PAGE_SIZE = 4096  # 4KB per page
KB = 1024

class Process:
    """Enhanced Process class with UUID, hex addresses, and cleanup"""
    
    _id_counter = 0
    
    def __init__(self, name: str, burst_time: int, size_kb: int):
        # UUID-based identification (from aiss)
        self.process_id = str(uuid.uuid4())[:8]  # 8-character unique ID
        self.simple_id = f"P{Process._id_counter}"  # Keep simple ID for compatibility
        Process._id_counter += 1
        
        # Basic process attributes
        self.name = name
        self.burst_time = burst_time
        self.burst_time_total = burst_time
        self.remaining_time = burst_time
        self.size_kb = size_kb
        self.size_bytes = size_kb * KB
        
        # Memory management
        self.num_pages = (self.size_bytes + PAGE_SIZE - 1) // PAGE_SIZE
        self.page_table: Dict[int, int] = {}  # page_number -> frame_number
        
        # Enhanced instruction support
        self.instructions: List[str] = []  # Named instructions
        self.hex_instructions: List[str] = []  # Hex address instructions (from aiss)
        self.current_instruction = 0
        
        # Generate realistic page access sequence
        self.page_access_sequence = self._generate_page_access_sequence()
        self.hex_address_sequence = self._generate_hex_address_sequence()
        
        # Statistics
        self.page_faults = 0
        self.page_hits = 0
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        
        # State management
        self.state = "READY"  # READY, RUNNING, WAITING, TERMINATED
        self.is_allocated = True
    
    def _generate_page_access_sequence(self) -> List[int]:
        """Generate realistic page access pattern"""
        sequence = []
        for i in range(self.burst_time):
            if i < 3:
                # Initial pages (startup)
                page = i % min(self.num_pages, 3)
            elif i < self.burst_time * 0.7:
                # Working set (80% locality)
                if random.random() < 0.8:
                    page = random.randint(0, min(self.num_pages - 1, 2))
                else:
                    page = random.randint(0, self.num_pages - 1)
            else:
                # Cleanup phase
                page = random.randint(0, self.num_pages - 1)
            sequence.append(page)
        return sequence
    
    def _generate_hex_address_sequence(self) -> List[str]:
        """Generate hex addresses corresponding to page access sequence"""
        hex_sequence = []
        for page_num in self.page_access_sequence:
            # Generate random offset within page
            offset = random.randint(0, PAGE_SIZE - 1)
            virtual_address = page_num * PAGE_SIZE + offset
            hex_addr = f"0x{virtual_address:04X}"
            hex_sequence.append(hex_addr)
        return hex_sequence
    
    def add_instruction(self, instruction: str):
        """Add named instruction"""
        self.instructions.append(instruction)
    
    def add_hex_instruction(self, hex_addr: str):
        """Add hex address instruction (from aiss)"""
        self.hex_instructions.append(hex_addr)
    
    def translate_address(self, hex_addr: str) -> Optional[int]:
        """
        Translate virtual hex address to physical address (from aiss)
        Returns physical address or None if page fault needs handling
        """
        try:
            virtual_address = int(hex_addr, 16)
            page_number = virtual_address // PAGE_SIZE
            offset = virtual_address % PAGE_SIZE
            
            if page_number not in self.page_table:
                # Page fault - needs to be handled by memory manager
                self.page_faults += 1
                return None
            else:
                # Page hit
                self.page_hits += 1
                frame_number = self.page_table[page_number]
                physical_address = frame_number * PAGE_SIZE + offset
                return physical_address
                
        except ValueError:
            print(f"Invalid hex address: {hex_addr}")
            return None
    
    def execute_instruction(self) -> bool:
        """Execute one instruction and return True if more instructions available"""
        if self.current_instruction >= len(self.instructions):
            return False
            
        instruction = self.instructions[self.current_instruction]
        print(f"    Executing: {instruction}")
        self.current_instruction += 1
        self.remaining_time -= 1
        return self.current_instruction < len(self.instructions)
    
    def execute_hex_instruction(self) -> Optional[str]:
        """Execute hex instruction and return the hex address used"""
        if self.current_instruction >= len(self.hex_address_sequence):
            return None
            
        hex_addr = self.hex_address_sequence[self.current_instruction]
        self.current_instruction += 1
        self.remaining_time -= 1
        return hex_addr
    
    def get_current_page(self) -> int:
        """Get current page being accessed"""
        if self.current_instruction < len(self.page_access_sequence):
            return self.page_access_sequence[self.current_instruction]
        return 0
    
    def get_current_hex_address(self) -> str:
        """Get current hex address being accessed"""
        if self.current_instruction < len(self.hex_address_sequence):
            return self.hex_address_sequence[self.current_instruction]
        return "0x0000"
    
    def deallocate_memory(self, memory_manager):
        """Clean up process memory (from aiss)"""
        print(f"Process [{self.name}] cleaning up memory...")
        frames_freed = []
        
        for page_num, frame_num in list(self.page_table.items()):
            memory_manager.deallocate_frame(frame_num, self.process_id, page_num)
            frames_freed.append(frame_num)
            print(f"  → Freed frame {frame_num} (Page {page_num})")
        
        self.page_table.clear()
        self.state = "TERMINATED"
        self.is_allocated = False
        
        print(f"Process [{self.name}] memory cleanup complete. Freed {len(frames_freed)} frames.")
        return frames_freed
    
    def get_hit_ratio(self) -> float:
        """Calculate page hit ratio"""
        total_accesses = self.page_hits + self.page_faults
        if total_accesses == 0:
            return 0.0
        return (self.page_hits / total_accesses) * 100
    
    def reset_for_simulation(self):
        """Reset process state for new simulation"""
        self.remaining_time = self.burst_time_total
        self.current_instruction = 0
        self.page_faults = 0
        self.page_hits = 0
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.state = "READY"
    
    @classmethod
    def reset_id_counter(cls):
        """Reset the ID counter for testing"""
        cls._id_counter = 0
    
    def __str__(self):
        return (f"Process(id={self.simple_id}, uuid={self.process_id}, "
                f"name={self.name}, pages={self.num_pages}, remaining={self.remaining_time}s)")
    
    def __repr__(self):
        return self.__str__()


class PhysicalMemory:
    """Enhanced Physical Memory with cleanup support"""
    
    def __init__(self, total_frames: int):
        self.total_frames = total_frames
        self.frames = {}  # frame_number -> {'process_id': str, 'page_number': int, 'allocated_time': float}
        self.free_frames = set(range(total_frames))
        self.allocated_frames = set()
        
    def allocate_frame(self, process_id: str, page_number: int) -> Optional[int]:
        """Allocate a frame for a specific process and page"""
        if not self.free_frames:
            return None
            
        frame_number = self.free_frames.pop()
        self.allocated_frames.add(frame_number)
        
        self.frames[frame_number] = {
            'process_id': process_id,
            'page_number': page_number,
            'allocated_time': time.time()
        }
        
        return frame_number
    
    def deallocate_frame(self, frame_number: int, process_id: str, page_number: int):
        """Deallocate a specific frame (from aiss)"""
        if frame_number in self.frames:
            frame_info = self.frames[frame_number]
            if frame_info['process_id'] == process_id and frame_info['page_number'] == page_number:
                del self.frames[frame_number]
                self.allocated_frames.discard(frame_number)
                self.free_frames.add(frame_number)
                return True
        return False
    
    def get_frame_info(self, frame_number: int) -> Optional[Dict]:
        """Get information about a specific frame"""
        return self.frames.get(frame_number)
    
    def get_process_frames(self, process_id: str) -> List[int]:
        """Get all frames allocated to a specific process"""
        return [frame_num for frame_num, info in self.frames.items() 
                if info['process_id'] == process_id]
    
    def is_frame_free(self, frame_number: int) -> bool:
        """Check if a frame is free"""
        return frame_number in self.free_frames
    
    def get_memory_usage(self) -> Dict:
        """Get current memory usage statistics"""
        return {
            'total_frames': self.total_frames,
            'used_frames': len(self.allocated_frames),
            'free_frames': len(self.free_frames),
            'usage_percentage': (len(self.allocated_frames) / self.total_frames) * 100
        }


class Statistics:
    """Enhanced statistics tracking"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all statistics"""
        self.total_processes = 0
        self.completed_processes = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.total_page_faults = 0
        self.total_page_hits = 0
        self.context_switches = 0
        self.simulation_start_time = None
        self.simulation_end_time = None
        self.process_completion_order = []
    
    def record_process_completion(self, process: Process, completion_time: int):
        """Record process completion statistics"""
        self.completed_processes += 1
        
        arrival_time = 0  # Assuming all processes arrive at time 0
        turnaround_time = completion_time - arrival_time
        waiting_time = turnaround_time - process.burst_time_total
        
        self.total_turnaround_time += turnaround_time
        self.total_waiting_time += waiting_time
        self.total_page_faults += process.page_faults
        self.total_page_hits += process.page_hits
        
        self.process_completion_order.append({
            'process_id': process.process_id,
            'name': process.name,
            'completion_time': completion_time,
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time,
            'page_faults': process.page_faults,
            'page_hits': process.page_hits,
            'hit_ratio': process.get_hit_ratio()
        })
    
    def get_average_waiting_time(self) -> float:
        """Calculate average waiting time"""
        if self.completed_processes == 0:
            return 0.0
        return self.total_waiting_time / self.completed_processes
    
    def get_average_turnaround_time(self) -> float:
        """Calculate average turnaround time"""
        if self.completed_processes == 0:
            return 0.0
        return self.total_turnaround_time / self.completed_processes
    
    def get_overall_hit_ratio(self) -> float:
        """Calculate overall page hit ratio"""
        total_accesses = self.total_page_hits + self.total_page_faults
        if total_accesses == 0:
            return 0.0
        return (self.total_page_hits / total_accesses) * 100
    
    def print_summary(self):
        """Print comprehensive statistics summary"""
        print(f"\n{'='*50}")
        print(f"    SIMULATION STATISTICS SUMMARY")
        print(f"{'='*50}")
        print(f"Total Processes: {self.total_processes}")
        print(f"Completed Processes: {self.completed_processes}")
        print(f"Average Waiting Time: {self.get_average_waiting_time():.2f}s")
        print(f"Average Turnaround Time: {self.get_average_turnaround_time():.2f}s")
        print(f"Total Context Switches: {self.context_switches}")
        print(f"Overall Hit Ratio: {self.get_overall_hit_ratio():.2f}%")
        print(f"Total Page Faults: {self.total_page_faults}")
        print(f"Total Page Hits: {self.total_page_hits}")
