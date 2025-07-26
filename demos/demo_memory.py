"""
Demo: Memory Page Replacement Algorithms
Compares FIFO vs LRU page replacement algorithms
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Process, MemoryManager

def demo_page_replacement_comparison():
    """Compare FIFO vs LRU page replacement"""
    print("="*60)
    print("    PAGE REPLACEMENT ALGORITHMS COMPARISON")
    print("="*60)
    
    # Test scenario: 4 pages, 3 frames, specific access pattern
    access_pattern = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    
    print(f"Test scenario:")
    print(f"  Process pages: 5 (numbered 1-5)")
    print(f"  Memory frames: 3")
    print(f"  Access pattern: {access_pattern}")
    print()
    
    # Test FIFO
    print("--- FIFO Algorithm ---")
    Process.reset_id_counter()
    
    fifo_process = Process("TestProcess", 15, 20)  # 20KB = 5 pages
    fifo_memory = MemoryManager(total_frames=3, algorithm='FIFO')
    fifo_memory.register_process(fifo_process)
    
    fifo_results = []
    for i, page in enumerate(access_pattern):
        page_index = page - 1  # Convert to 0-based indexing
        result = fifo_memory.access_page(fifo_process, page_index)
        fifo_results.append(result['status'])
        
        print(f"Access {i+1:2d}: Page {page} → {result['status']:5s}", end="")
        
        if result['evicted_page_info']:
            evicted = result['evicted_page_info']
            evicted_page = evicted['page_number'] + 1  # Convert back to 1-based
            print(f" (Evicted Page {evicted_page})", end="")
        
        print(f" | Frames: {[f['page_number']+1 if f else None for f in fifo_memory.physical_memory.frames]}")
    
    fifo_stats = fifo_memory.get_memory_statistics()
    print(f"\nFIFO Results:")
    print(f"  Page Hits: {fifo_stats['page_hits']}")
    print(f"  Page Faults: {fifo_stats['page_faults']}")
    print(f"  Hit Ratio: {fifo_stats['hit_ratio']:.2%}")
    
    # Test LRU
    print(f"\n--- LRU Algorithm ---")
    Process.reset_id_counter()
    
    lru_process = Process("TestProcess", 15, 20)  # Same as FIFO test
    lru_memory = MemoryManager(total_frames=3, algorithm='LRU')
    lru_memory.register_process(lru_process)
    
    lru_results = []
    for i, page in enumerate(access_pattern):
        page_index = page - 1  # Convert to 0-based indexing
        result = lru_memory.access_page(lru_process, page_index)
        lru_results.append(result['status'])
        
        print(f"Access {i+1:2d}: Page {page} → {result['status']:5s}", end="")
        
        if result['evicted_page_info']:
            evicted = result['evicted_page_info']
            evicted_page = evicted['page_number'] + 1  # Convert back to 1-based
            print(f" (Evicted Page {evicted_page})", end="")
        
        print(f" | Frames: {[f['page_number']+1 if f else None for f in lru_memory.physical_memory.frames]}")
        print(f"         LRU order: {[f+1 for f in lru_memory.lru_tracker]}")
    
    lru_stats = lru_memory.get_memory_statistics()
    print(f"\nLRU Results:")
    print(f"  Page Hits: {lru_stats['page_hits']}")
    print(f"  Page Faults: {lru_stats['page_faults']}")
    print(f"  Hit Ratio: {lru_stats['hit_ratio']:.2%}")
    
    # Comparison
    print(f"\n--- COMPARISON ---")
    print(f"Access Pattern: {access_pattern}")
    print(f"FIFO Results:   {fifo_results}")
    print(f"LRU Results:    {lru_results}")
    print()
    print(f"FIFO - Hits: {fifo_stats['page_hits']}, Faults: {fifo_stats['page_faults']}, Hit Ratio: {fifo_stats['hit_ratio']:.2%}")
    print(f"LRU  - Hits: {lru_stats['page_hits']}, Faults: {lru_stats['page_faults']}, Hit Ratio: {lru_stats['hit_ratio']:.2%}")
    
    if lru_stats['hit_ratio'] > fifo_stats['hit_ratio']:
        print("🏆 LRU performs better for this access pattern")
    elif fifo_stats['hit_ratio'] > lru_stats['hit_ratio']:
        print("🏆 FIFO performs better for this access pattern")
    else:
        print("🤝 Both algorithms perform equally for this access pattern")

def demo_locality_of_reference():
    """Demonstrate how locality of reference affects page replacement"""
    print("\n" + "="*60)
    print("    LOCALITY OF REFERENCE DEMONSTRATION")
    print("="*60)
    
    # Test with high locality (sequential access)
    sequential_pattern = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5, 4, 5, 4, 5]
    
    # Test with low locality (random access)
    random_pattern = [1, 5, 2, 4, 3, 1, 5, 2, 4, 3, 1, 5, 2, 4, 3]
    
    patterns = [
        ("Sequential (High Locality)", sequential_pattern),
        ("Random (Low Locality)", random_pattern)
    ]
    
    for pattern_name, pattern in patterns:
        print(f"\n--- {pattern_name} ---")
        print(f"Access pattern: {pattern}")
        
        for algorithm in ['FIFO', 'LRU']:
            Process.reset_id_counter()
            process = Process("TestProcess", 15, 20)
            memory = MemoryManager(total_frames=3, algorithm=algorithm)
            memory.register_process(process)
            
            for page in pattern:
                page_index = page - 1
                memory.access_page(process, page_index)
            
            stats = memory.get_memory_statistics()
            print(f"{algorithm}: Hits={stats['page_hits']}, Faults={stats['page_faults']}, Hit Ratio={stats['hit_ratio']:.2%}")

if __name__ == "__main__":
    demo_page_replacement_comparison()
    demo_locality_of_reference()
