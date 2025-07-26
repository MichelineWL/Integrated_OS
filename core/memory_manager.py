"""
Memory Manager - Virtual Memory System with Page Replacement
Implements FIFO and LRU page replacement algorithms
"""

from collections import deque
from .models import PhysicalMemory, Statistics

class MemoryManager:
    """
    Advanced Memory Manager with virtual memory and page replacement
    """
    def __init__(self, total_frames=16, algorithm='FIFO'):
        if algorithm.upper() not in ['FIFO', 'LRU']:
            raise ValueError("Algorithm must be 'FIFO' or 'LRU'")
        
        self.physical_memory = PhysicalMemory(total_frames)
        self.algorithm = algorithm.upper()
        self.statistics = Statistics()
        
        # Process registry
        self.processes = {}
        
        # Page replacement algorithm data structures
        self.fifo_queue = deque()  # For FIFO: tracks frame insertion order
        self.lru_tracker = []      # For LRU: tracks frame access order
    
    def register_process(self, process):
        """Register a process with the memory manager"""
        self.processes[process.process_id] = process
        print(f"Registered process {process.name} with {process.num_pages} pages")
    
    def can_allocate_pages(self, pages_needed):
        """Check if we can allocate the required number of pages"""
        return self.physical_memory.get_free_frames_count() >= pages_needed
    
    def access_page(self, process, page_number):
        """
        Main memory access function - handles page hits and faults
        
        Returns:
            dict: Result of memory access operation
        """
        # Check if page is already in memory (Page Hit)
        page_entry = process.page_table.get(page_number)
        if page_entry and page_entry[1] == 1:  # valid bit == 1
            frame_number = page_entry[0]
            
            # Update LRU tracker for hits
            if self.algorithm == 'LRU':
                self._update_lru_tracker(frame_number)
            
            self.statistics.increment_hits()
            return {
                "status": "HIT",
                "process_id": process.process_id,
                "page_number": page_number,
                "frame_number": frame_number,
                "evicted_page_info": None
            }
        
        # Page Fault occurred
        self.statistics.increment_faults()
        
        # Check if we have free frames
        if not self.physical_memory.is_full():
            # Load page into empty frame
            target_frame = self.physical_memory.get_empty_frame_index()
            self._load_page_to_frame(process, page_number, target_frame)
            
            return {
                "status": "FAULT",
                "process_id": process.process_id,
                "page_number": page_number,
                "loaded_into_frame": target_frame,
                "evicted_page_info": None
            }
        else:
            # Memory is full - need page replacement
            if self.algorithm == 'FIFO':
                victim_frame = self._run_fifo_replacement()
            else:  # LRU
                victim_frame = self._run_lru_replacement()
            
            # Get information about the page being evicted
            evicted_info = None
            if self.physical_memory.frames[victim_frame]:
                evicted_info = self.physical_memory.frames[victim_frame].copy()
            
            # Evict the old page
            self._evict_page_from_frame(victim_frame)
            
            # Load the new page
            self._load_page_to_frame(process, page_number, victim_frame)
            
            return {
                "status": "FAULT",
                "process_id": process.process_id,
                "page_number": page_number,
                "loaded_into_frame": victim_frame,
                "evicted_page_info": evicted_info
            }
    
    def _load_page_to_frame(self, process, page_number, frame_number):
        """Load a page into a specific frame"""
        # Update physical memory
        self.physical_memory.frames[frame_number] = {
            "process_id": process.process_id,
            "page_number": page_number
        }
        
        # Update process page table
        process.page_table[page_number][0] = frame_number  # frame number
        process.page_table[page_number][1] = 1            # valid bit
        
        # Update algorithm-specific data structures
        if self.algorithm == 'FIFO' and frame_number not in self.fifo_queue:
            self.fifo_queue.append(frame_number)
        
        if self.algorithm == 'LRU':
            self._update_lru_tracker(frame_number)
    
    def _evict_page_from_frame(self, frame_number):
        """Evict a page from a specific frame"""
        page_info = self.physical_memory.frames[frame_number]
        if not page_info:
            return
        
        process_id = page_info['process_id']
        page_number = page_info['page_number']
        
        # Update the evicted process's page table
        old_process = self.processes.get(process_id)
        if old_process and page_number in old_process.page_table:
            old_process.page_table[page_number][0] = None  # clear frame number
            old_process.page_table[page_number][1] = 0     # clear valid bit
        
        # Clear the frame
        self.physical_memory.frames[frame_number] = None
    
    def _update_lru_tracker(self, accessed_frame):
        """Update LRU tracker - move accessed frame to end (most recent)"""
        if accessed_frame in self.lru_tracker:
            self.lru_tracker.remove(accessed_frame)
        self.lru_tracker.append(accessed_frame)
    
    def _run_fifo_replacement(self):
        """FIFO page replacement - return oldest frame"""
        if not self.fifo_queue:
            raise RuntimeError("FIFO queue is empty during replacement")
        victim_frame = self.fifo_queue.popleft()
        return victim_frame
    
    def _run_lru_replacement(self):
        """LRU page replacement - return least recently used frame"""
        if not self.lru_tracker:
            raise RuntimeError("LRU tracker is empty during replacement")
        victim_frame = self.lru_tracker.pop(0)  # Remove least recently used
        return victim_frame
    
    def deallocate_process_frames(self, process_id):
        """Deallocate all frames used by a specific process"""
        frames_to_free = []
        
        # Find all frames used by this process
        for i, frame_content in enumerate(self.physical_memory.frames):
            if frame_content and frame_content.get('process_id') == process_id:
                frames_to_free.append(i)
        
        # Free each frame
        for frame_num in frames_to_free:
            # Remove from algorithm trackers
            if frame_num in self.fifo_queue:
                self.fifo_queue.remove(frame_num)
            if frame_num in self.lru_tracker:
                self.lru_tracker.remove(frame_num)
            
            # Evict the page
            self._evict_page_from_frame(frame_num)
        
        print(f"Deallocated {len(frames_to_free)} frames for process {process_id}")
    
    def get_memory_statistics(self):
        """Get current memory statistics"""
        return {
            "total_frames": self.physical_memory.total_frames,
            "used_frames": self.physical_memory.get_used_frames_count(),
            "free_frames": self.physical_memory.get_free_frames_count(),
            "total_accesses": self.statistics.total_accesses,
            "page_hits": self.statistics.page_hits,
            "page_faults": self.statistics.page_faults,
            "hit_ratio": self.statistics.get_hit_ratio()
        }
    
    def display_memory_status(self):
        """Display comprehensive memory status"""
        stats = self.get_memory_statistics()
        
        print(f"\n{'='*50}")
        print(f"    MEMORY STATUS ({self.algorithm} Algorithm)")
        print(f"{'='*50}")
        
        # Memory usage
        print(f"Physical Memory:")
        print(f"  Total Frames: {stats['total_frames']}")
        print(f"  Used Frames:  {stats['used_frames']}")
        print(f"  Free Frames:  {stats['free_frames']}")
        print(f"  Usage:        {stats['used_frames']/stats['total_frames']*100:.1f}%")
        
        # Access statistics
        if stats['total_accesses'] > 0:
            print(f"\nMemory Access Statistics:")
            print(f"  Total Accesses: {stats['total_accesses']}")
            print(f"  Page Hits:      {stats['page_hits']}")
            print(f"  Page Faults:    {stats['page_faults']}")
            print(f"  Hit Ratio:      {stats['hit_ratio']:.2%}")
        
        # Frame allocation details
        print(f"\nFrame Allocation:")
        for i, frame_content in enumerate(self.physical_memory.frames):
            if frame_content:
                pid = frame_content['process_id']
                page = frame_content['page_number']
                print(f"  Frame {i:2d}: {pid}, Page {page}")
            else:
                print(f"  Frame {i:2d}: [FREE]")
        
        # Algorithm-specific information
        if self.algorithm == 'FIFO' and self.fifo_queue:
            print(f"\nFIFO Queue: {list(self.fifo_queue)}")
        elif self.algorithm == 'LRU' and self.lru_tracker:
            print(f"\nLRU Tracker: {self.lru_tracker} (Left=Oldest, Right=Newest)")
        
        print(f"{'='*50}")
    
    def reset_statistics(self):
        """Reset memory access statistics"""
        self.statistics.reset()
        print("Memory statistics reset")


# Legacy compatibility
class PhysicalMemory_Legacy:
    """Legacy PhysicalMemory class for backward compatibility"""
    def __init__(self, total_memory_kb=64, frame_size_kb=4):
        self.frame_size = frame_size_kb
        self.total_frames = total_memory_kb // frame_size_kb
        self.frames = [None] * self.total_frames
        self.free_frames = list(range(self.total_frames))
    
    def allocate_frame(self, process_id, page_number):
        if not self.free_frames:
            return None
        frame_number = self.free_frames.pop(0)
        self.frames[frame_number] = (process_id, page_number)
        return frame_number
    
    def deallocate_frame(self, frame_number):
        if 0 <= frame_number < self.total_frames and self.frames[frame_number] is not None:
            self.frames[frame_number] = None
            self.free_frames.append(frame_number)
            self.free_frames.sort()
    
    def can_allocate_pages(self, pages_needed):
        return len(self.free_frames) >= pages_needed
    
    def get_available_frames(self):
        return len(self.free_frames)
    
    def deallocate_process_frames(self, process_id):
        frames_to_free = []
        for i, frame_content in enumerate(self.frames):
            if frame_content is not None and frame_content[0] == process_id:
                frames_to_free.append(i)
        for frame_num in frames_to_free:
            self.deallocate_frame(frame_num)
    
    def display_memory_status(self):
        print(f"\n=== Physical Memory Status ===")
        print(f"Total frames: {self.total_frames}")
        print(f"Free frames: {len(self.free_frames)}")
        print(f"Used frames: {self.total_frames - len(self.free_frames)}")
        print("\nFrame allocation:")
        for i, frame_content in enumerate(self.frames):
            if frame_content is not None:
                process_id, page_num = frame_content
                print(f"Frame {i}: Process {process_id}, Page {page_num}")
            else:
                print(f"Frame {i}: [FREE]")
        print("=" * 30)
