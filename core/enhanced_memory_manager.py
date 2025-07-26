"""
Enhanced Memory Manager with Hex Address Support and Interactive Controls
Integrates best features from aiss: hex translation, cleanup, real-time controls
"""

import time
from typing import Dict, List, Optional, Union
from collections import deque
from .enhanced_models import Process, PhysicalMemory, PAGE_SIZE

class EnhancedMemoryManager:
    """Enhanced Memory Manager with hex address support and interactive controls"""
    
    def __init__(self, total_frames: int = 8, algorithm: str = 'FIFO'):
        self.physical_memory = PhysicalMemory(total_frames)
        self.algorithm = algorithm.upper()
        self.registered_processes: Dict[str, Process] = {}
        
        # Page replacement algorithm state
        if self.algorithm == 'FIFO':
            self.fifo_queue = deque()
        elif self.algorithm == 'LRU':
            self.lru_tracker = []
        
        # Interactive controls (from aiss)
        self.is_paused = False
        self.is_running = True
        self.step_mode = False
        
        # Statistics
        self.total_accesses = 0
        self.total_hits = 0
        self.total_faults = 0
        self.access_log = []
        
        print(f"Enhanced Memory Manager initialized: {total_frames} frames, {self.algorithm} algorithm")
    
    def register_process(self, process: Process):
        """Register a process with the memory manager"""
        self.registered_processes[process.process_id] = process
        print(f"Registered process {process.name} (UUID: {process.process_id}) with {process.num_pages} pages")
    
    def translate_hex_address(self, process: Process, hex_addr: str) -> Optional[int]:
        """
        Translate hex virtual address to physical address (from aiss)
        Returns physical address or None if page fault
        """
        try:
            virtual_address = int(hex_addr, 16)
            page_number = virtual_address // PAGE_SIZE
            offset = virtual_address % PAGE_SIZE
            
            # Check if page is in memory
            if page_number in process.page_table:
                # Page hit
                frame_number = process.page_table[page_number]
                physical_address = frame_number * PAGE_SIZE + offset
                
                # Update LRU tracker if needed
                if self.algorithm == 'LRU':
                    self._update_lru_tracker(frame_number)
                
                return physical_address
            else:
                # Page fault - will be handled by access_page
                return None
                
        except ValueError:
            print(f"Invalid hex address format: {hex_addr}")
            return None
    
    def access_page(self, process: Process, page_number: int) -> Dict:
        """Access a page with enhanced tracking and controls"""
        # Check for pause/step controls
        self._check_interactive_controls()
        
        self.total_accesses += 1
        
        # Log access
        access_info = {
            'process_id': process.process_id,
            'process_name': process.name,
            'page_number': page_number,
            'time': time.time()
        }
        
        if page_number in process.page_table:
            # Page hit
            frame_number = process.page_table[page_number]
            self.total_hits += 1
            
            # Update algorithm-specific tracking
            if self.algorithm == 'LRU':
                self._update_lru_tracker(frame_number)
            
            result = {
                'status': 'HIT',
                'frame': frame_number,
                'page_number': page_number,
                'process_id': process.process_id,
                'evicted_page_info': None
            }
        else:
            # Page fault
            self.total_faults += 1
            frame_number = self._allocate_page(process, page_number)
            
            if frame_number is not None:
                result = {
                    'status': 'FAULT',
                    'frame': frame_number,
                    'page_number': page_number,
                    'process_id': process.process_id,
                    'evicted_page_info': None
                }
            else:
                # Need to evict a page
                evicted_info = self._run_page_replacement()
                frame_number = self._allocate_page(process, page_number)
                
                result = {
                    'status': 'FAULT',
                    'frame': frame_number,
                    'page_number': page_number,
                    'process_id': process.process_id,
                    'evicted_page_info': evicted_info
                }
        
        # Add to access log
        access_info.update(result)
        self.access_log.append(access_info)
        
        return result
    
    def access_hex_address(self, process: Process, hex_addr: str) -> Dict:
        """
        Access memory using hex address (from aiss integration)
        Returns access result with physical address if successful
        """
        # Parse hex address
        try:
            virtual_address = int(hex_addr, 16)
            page_number = virtual_address // PAGE_SIZE
            offset = virtual_address % PAGE_SIZE
        except ValueError:
            return {
                'status': 'ERROR',
                'error': f'Invalid hex address: {hex_addr}',
                'physical_address': None
            }
        
        # Access the page
        page_result = self.access_page(process, page_number)
        
        # Calculate physical address if successful
        if page_result['status'] in ['HIT', 'FAULT'] and page_result['frame'] is not None:
            physical_address = page_result['frame'] * PAGE_SIZE + offset
            page_result['virtual_address'] = hex_addr
            page_result['physical_address'] = f"0x{physical_address:04X}"
            page_result['offset'] = offset
        else:
            page_result['virtual_address'] = hex_addr
            page_result['physical_address'] = None
            page_result['offset'] = offset
        
        return page_result
    
    def deallocate_process(self, process: Process):
        """
        Deallocate all memory used by a process (from aiss)
        Enhanced with proper cleanup and statistics
        """
        if process.process_id not in self.registered_processes:
            print(f"Process {process.name} not registered with memory manager")
            return
        
        print(f"\n{'='*50}")
        print(f"    DEALLOCATING PROCESS: {process.name}")
        print(f"    UUID: {process.process_id}")
        print(f"{'='*50}")
        
        frames_freed = []
        pages_freed = []
        
        # Free all frames allocated to this process
        for page_num, frame_num in list(process.page_table.items()):
            success = self.physical_memory.deallocate_frame(frame_num, process.process_id, page_num)
            if success:
                frames_freed.append(frame_num)
                pages_freed.append(page_num)
                
                # Remove from algorithm-specific tracking
                if self.algorithm == 'FIFO' and frame_num in self.fifo_queue:
                    self.fifo_queue.remove(frame_num)
                elif self.algorithm == 'LRU' and frame_num in self.lru_tracker:
                    self.lru_tracker.remove(frame_num)
                
                print(f"  → Freed frame {frame_num} (Page {page_num})")
        
        # Clear process page table
        process.page_table.clear()
        
        # Remove from registered processes
        del self.registered_processes[process.process_id]
        
        print(f"Process cleanup complete:")
        print(f"  - Freed {len(frames_freed)} frames: {frames_freed}")
        print(f"  - Freed {len(pages_freed)} pages: {pages_freed}")
        print(f"  - Process hit ratio: {process.get_hit_ratio():.2f}%")
        
        return {
            'frames_freed': frames_freed,
            'pages_freed': pages_freed,
            'hit_ratio': process.get_hit_ratio()
        }
    
    # Interactive Controls (from aiss)
    def pause_simulation(self):
        """Pause the simulation"""
        self.is_paused = True
        print("\\n[PAUSED] Memory simulation paused. Call resume_simulation() to continue.")
    
    def resume_simulation(self):
        """Resume the simulation"""
        self.is_paused = False
        print("\\n[RESUMED] Memory simulation resumed.")
    
    def enable_step_mode(self):
        """Enable step-by-step execution"""
        self.step_mode = True
        print("\\n[STEP MODE] Enabled. Press Enter for each memory access.")
    
    def disable_step_mode(self):
        """Disable step-by-step execution"""
        self.step_mode = False
        print("\\n[CONTINUOUS MODE] Step mode disabled.")
    
    def _check_interactive_controls(self):
        """Check and handle interactive controls"""
        while self.is_paused:
            time.sleep(0.1)
        
        if self.step_mode:
            input("Press Enter to continue...")
    
    # Page Replacement Algorithms (enhanced)
    def _allocate_page(self, process: Process, page_number: int) -> Optional[int]:
        """Allocate a frame for the given page"""
        frame_number = self.physical_memory.allocate_frame(process.process_id, page_number)
        
        if frame_number is not None:
            process.page_table[page_number] = frame_number
            
            # Update algorithm-specific tracking
            if self.algorithm == 'FIFO':
                self.fifo_queue.append(frame_number)
            elif self.algorithm == 'LRU':
                self.lru_tracker.append(frame_number)
        
        return frame_number
    
    def _run_page_replacement(self) -> Optional[Dict]:
        """Run page replacement algorithm"""
        if self.algorithm == 'FIFO':
            return self._run_fifo_replacement()
        elif self.algorithm == 'LRU':
            return self._run_lru_replacement()
        return None
    
    def _run_fifo_replacement(self) -> Optional[Dict]:
        """FIFO page replacement"""
        if not self.fifo_queue:
            return None
        
        # Get the oldest frame
        frame_to_evict = self.fifo_queue.popleft()
        frame_info = self.physical_memory.get_frame_info(frame_to_evict)
        
        if frame_info:
            # Remove from process page table
            process_id = frame_info['process_id']
            page_number = frame_info['page_number']
            
            if process_id in self.registered_processes:
                process = self.registered_processes[process_id]
                if page_number in process.page_table:
                    del process.page_table[page_number]
            
            # Free the frame
            self.physical_memory.deallocate_frame(frame_to_evict, process_id, page_number)
            
            return {
                'evicted_frame': frame_to_evict,
                'process_id': process_id,
                'page_number': page_number
            }
        
        return None
    
    def _run_lru_replacement(self) -> Optional[Dict]:
        """LRU page replacement"""
        if not self.lru_tracker:
            return None
        
        # Get the least recently used frame
        frame_to_evict = self.lru_tracker.pop(0)
        frame_info = self.physical_memory.get_frame_info(frame_to_evict)
        
        if frame_info:
            # Remove from process page table
            process_id = frame_info['process_id']
            page_number = frame_info['page_number']
            
            if process_id in self.registered_processes:
                process = self.registered_processes[process_id]
                if page_number in process.page_table:
                    del process.page_table[page_number]
            
            # Free the frame
            self.physical_memory.deallocate_frame(frame_to_evict, process_id, page_number)
            
            return {
                'evicted_frame': frame_to_evict,
                'process_id': process_id,
                'page_number': page_number
            }
        
        return None
    
    def _update_lru_tracker(self, frame_number: int):
        """Update LRU tracker"""
        if frame_number in self.lru_tracker:
            self.lru_tracker.remove(frame_number)
        self.lru_tracker.append(frame_number)
    
    # Enhanced Display and Statistics
    def display_memory_status(self):
        """Display comprehensive memory status"""
        print(f"\\n{'='*50}")
        print(f"    ENHANCED MEMORY STATUS ({self.algorithm} Algorithm)")
        print(f"{'='*50}")
        
        # Physical memory status
        usage = self.physical_memory.get_memory_usage()
        print(f"Physical Memory:")
        print(f"  Total Frames: {usage['total_frames']}")
        print(f"  Used Frames:  {usage['used_frames']}")
        print(f"  Free Frames:  {usage['free_frames']}")
        print(f"  Usage:        {usage['usage_percentage']:.1f}%")
        
        # Memory access statistics
        hit_ratio = (self.total_hits / self.total_accesses * 100) if self.total_accesses > 0 else 0
        print(f"\\nMemory Access Statistics:")
        print(f"  Total Accesses: {self.total_accesses}")
        print(f"  Page Hits:      {self.total_hits}")
        print(f"  Page Faults:    {self.total_faults}")
        print(f"  Hit Ratio:      {hit_ratio:.2f}%")
        
        # Frame allocation details
        print(f"\\nFrame Allocation:")
        for frame_num in range(self.physical_memory.total_frames):
            if frame_num in self.physical_memory.frames:
                info = self.physical_memory.frames[frame_num]
                process_name = "Unknown"
                if info['process_id'] in self.registered_processes:
                    process_name = self.registered_processes[info['process_id']].name
                print(f"  Frame {frame_num:2d}: {info['process_id']} ({process_name}), Page {info['page_number']}")
            else:
                print(f"  Frame {frame_num:2d}: [FREE]")
        
        # Algorithm-specific info
        if self.algorithm == 'FIFO':
            print(f"\\nFIFO Queue: {list(self.fifo_queue)}")
        elif self.algorithm == 'LRU':
            print(f"\\nLRU Tracker: {self.lru_tracker}")
        
        print(f"{'='*50}")
    
    def get_statistics(self) -> Dict:
        """Get comprehensive memory statistics"""
        hit_ratio = (self.total_hits / self.total_accesses * 100) if self.total_accesses > 0 else 0
        
        return {
            'total_accesses': self.total_accesses,
            'total_hits': self.total_hits,
            'total_faults': self.total_faults,
            'hit_ratio': hit_ratio,
            'memory_usage': self.physical_memory.get_memory_usage(),
            'algorithm': self.algorithm,
            'active_processes': len(self.registered_processes)
        }
