"""
Comprehensive Test Suite for Operating System Simulator
Tests all major components and algorithms
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Process, MemoryManager, CPUScheduler, PAGE_SIZE

def test_process_creation():
    """Test Process class functionality"""
    print("\n" + "="*50)
    print("  TEST 1: Process Creation and Page Calculation")
    print("="*50)
    
    Process.reset_id_counter()
    
    # Test various process sizes
    test_cases = [
        ("Small Process", 5, 4),    # 4KB = 1 page
        ("Medium Process", 8, 10),  # 10KB = 3 pages
        ("Large Process", 12, 20),  # 20KB = 5 pages
    ]
    
    for name, burst_time, size_kb in test_cases:
        process = Process(name, burst_time, size_kb)
        expected_pages = (size_kb * 1024 + PAGE_SIZE - 1) // PAGE_SIZE  # Ceiling division
        
        print(f"Process: {process}")
        print(f"  Expected pages: {expected_pages}, Actual pages: {process.num_pages}")
        print(f"  Page table size: {len(process.page_table)}")
        print(f"  Access sequence length: {len(process.page_access_sequence)}")
        
        assert process.num_pages == expected_pages, f"Page calculation error for {name}"
        assert len(process.page_table) == expected_pages, f"Page table size error for {name}"
        assert len(process.page_access_sequence) == burst_time, f"Access sequence error for {name}"
    
    print("✅ Process creation tests PASSED")

def test_memory_fifo():
    """Test FIFO page replacement algorithm"""
    print("\n" + "="*50)
    print("  TEST 2: FIFO Page Replacement Algorithm")
    print("="*50)
    
    Process.reset_id_counter()
    
    # Create memory manager with small frame count to force replacement
    memory = MemoryManager(total_frames=3, algorithm='FIFO')
    
    # Create test process
    process = Process("TestProcess", 10, 16)  # 16KB = 4 pages, but only 3 frames
    memory.register_process(process)
    
    print(f"Process has {process.num_pages} pages, memory has 3 frames")
    
    # Access pages to trigger FIFO replacement
    page_sequence = [0, 1, 2, 0, 3, 1]  # Page 3 should evict page 0 (FIFO)
    expected_results = ['FAULT', 'FAULT', 'FAULT', 'HIT', 'FAULT', 'HIT']
    
    results = []
    for i, page in enumerate(page_sequence):
        result = memory.access_page(process, page)
        results.append(result['status'])
        print(f"Access {i+1}: Page {page} → {result['status']}")
        
        if result['evicted_page_info']:
            evicted = result['evicted_page_info']
            print(f"  Evicted: Process {evicted['process_id']}, Page {evicted['page_number']}")
    
    print(f"Expected: {expected_results}")
    print(f"Actual:   {results}")
    
    # Verify FIFO behavior
    assert results == expected_results, "FIFO algorithm behavior incorrect"
    
    print("✅ FIFO page replacement tests PASSED")

def test_memory_lru():
    """Test LRU page replacement algorithm"""
    print("\n" + "="*50)
    print("  TEST 3: LRU Page Replacement Algorithm")
    print("="*50)
    
    Process.reset_id_counter()
    
    # Create memory manager with LRU
    memory = MemoryManager(total_frames=3, algorithm='LRU')
    
    # Create test process
    process = Process("TestProcess", 10, 16)  # 4 pages, 3 frames
    memory.register_process(process)
    
    # Access pattern designed to test LRU
    page_sequence = [0, 1, 2, 0, 3, 1]  # Test LRU behavior
    
    results = []
    for i, page in enumerate(page_sequence):
        result = memory.access_page(process, page)
        results.append(result['status'])
        print(f"Access {i+1}: Page {page} → {result['status']}")
        print(f"  LRU tracker: {memory.lru_tracker}")
        
        if result['evicted_page_info']:
            evicted = result['evicted_page_info']
            print(f"  Evicted: Process {evicted['process_id']}, Page {evicted['page_number']}")
    
    # LRU Analysis:
    # 1. Access 0: FAULT → frames=[0], LRU=[0]
    # 2. Access 1: FAULT → frames=[0,1], LRU=[0,1] 
    # 3. Access 2: FAULT → frames=[0,1,2], LRU=[0,1,2]
    # 4. Access 0: HIT → LRU=[1,2,0] (0 moved to end)
    # 5. Access 3: FAULT → evict frame 1 (least recently used), LRU=[2,0,1]
    # 6. Access 1: FAULT → evict frame 2 (least recently used), LRU=[0,1,2]
    expected_results = ['FAULT', 'FAULT', 'FAULT', 'HIT', 'FAULT', 'FAULT']
    
    print(f"Expected: {expected_results}")
    print(f"Actual:   {results}")
    
    assert results == expected_results, "LRU algorithm behavior incorrect"
    
    print("✅ LRU page replacement tests PASSED")

def test_fcfs_scheduler():
    """Test FCFS scheduling algorithm"""
    print("\n" + "="*50)
    print("  TEST 4: FCFS CPU Scheduling")
    print("="*50)
    
    Process.reset_id_counter()
    
    # Create test processes
    p1 = Process("Process_A", 3, 4)
    p2 = Process("Process_B", 4, 4)
    p3 = Process("Process_C", 2, 4)
    
    # Add some instructions
    for p in [p1, p2, p3]:
        for i in range(2):
            p.add_instruction(f"{p.name}_instruction_{i+1}")
    
    # Create FCFS scheduler
    scheduler = CPUScheduler(algorithm='FCFS')
    scheduler.add_process(p1)
    scheduler.add_process(p2)
    scheduler.add_process(p3)
    
    # Run simulation
    result = scheduler.run_complete_simulation()
    
    # Verify FCFS order: P0 should run completely, then P1, then P2
    expected_order = ['P0', 'P0', 'P0', 'P1', 'P1', 'P1', 'P1', 'P2', 'P2']
    
    print(f"Expected execution order: {expected_order}")
    print(f"Actual execution order:   {result['execution_order']}")
    
    assert result['execution_order'] == expected_order, "FCFS execution order incorrect"
    assert result['total_time'] == 10, "FCFS total time incorrect"
    
    print("✅ FCFS scheduling tests PASSED")

def test_round_robin_scheduler():
    """Test Round Robin scheduling algorithm"""
    print("\n" + "="*50)
    print("  TEST 5: Round Robin CPU Scheduling")
    print("="*50)
    
    Process.reset_id_counter()
    
    # Create test processes with specific burst times
    p1 = Process("Process_A", 5, 4)  # 5 time units
    p2 = Process("Process_B", 4, 4)  # 4 time units
    
    # Add instructions
    for p in [p1, p2]:
        for i in range(3):
            p.add_instruction(f"{p.name}_instruction_{i+1}")
    
    # Create Round Robin scheduler with quantum = 3
    scheduler = CPUScheduler(algorithm='RR', time_quantum=3)
    scheduler.add_process(p1)
    scheduler.add_process(p2)
    
    # Run simulation
    result = scheduler.run_complete_simulation()
    
    # Expected: P0(3), P1(3), P0(2), P1(1)
    expected_order = ['P0', 'P0', 'P0', 'P1', 'P1', 'P1', 'P0', 'P0', 'P1']
    
    print(f"Expected execution order: {expected_order}")
    print(f"Actual execution order:   {result['execution_order']}")
    
    assert result['execution_order'] == expected_order, "Round Robin execution order incorrect"
    assert result['total_time'] == 10, "Round Robin total time incorrect"
    assert result['context_switches'] > 0, "Round Robin should have context switches"
    
    print("✅ Round Robin scheduling tests PASSED")

def test_integrated_system():
    """Test integrated memory management and CPU scheduling"""
    print("\n" + "="*50)
    print("  TEST 6: Integrated System Test")
    print("="*50)
    
    Process.reset_id_counter()
    
    # Create memory manager
    memory = MemoryManager(total_frames=8, algorithm='FIFO')
    
    # Create processes
    p1 = Process("Process_A", 6, 8)   # 8KB = 2 pages
    p2 = Process("Process_B", 5, 12)  # 12KB = 3 pages
    
    # Register processes with memory manager
    memory.register_process(p1)
    memory.register_process(p2)
    
    # Add instructions
    for p in [p1, p2]:
        for i in range(3):
            p.add_instruction(f"{p.name}_instruction_{i+1}")
    
    # Create Round Robin scheduler
    scheduler = CPUScheduler(algorithm='RR', time_quantum=3)
    scheduler.add_process(p1)
    scheduler.add_process(p2)
    
    # Run integrated simulation
    result = scheduler.run_complete_simulation(memory_manager=memory)
    
    # Verify basic functionality
    assert result['total_time'] == 12, "Integrated system total time incorrect"
    assert len(result['memory_accesses']) > 0, "No memory accesses recorded"
    assert result['completed_processes'] == 2, "Not all processes completed"
    
    # Display memory statistics
    memory.display_memory_status()
    
    print("✅ Integrated system tests PASSED")

def run_all_tests():
    """Run all test suites"""
    print("="*60)
    print("    OPERATING SYSTEM SIMULATOR - TEST SUITE")
    print("="*60)
    
    try:
        test_process_creation()
        test_memory_fifo()
        test_memory_lru()
        test_fcfs_scheduler()
        test_round_robin_scheduler()
        test_integrated_system()
        
        print("\n" + "="*60)
        print("    🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
