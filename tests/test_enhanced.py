"""
Comprehensive Test Suite for Enhanced OS Simulator v2.1
Tests integration of features from aiss: UUID, hex addresses, interactive controls, cleanup
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Process, MemoryManager, CPUScheduler

def test_enhanced_process_features():
    """Test enhanced process features: UUID, hex addresses, cleanup"""
    print("\\n" + "="*60)
    print("  TEST 1: Enhanced Process Features")
    print("="*60)
    
    Process.reset_id_counter()
    
    # Test UUID generation
    process1 = Process("TestProcess1", 5, 8)
    process2 = Process("TestProcess2", 3, 4)
    
    print(f"Process 1: {process1}")
    print(f"Process 2: {process2}")
    
    # Verify UUID uniqueness
    assert process1.process_id != process2.process_id, "UUIDs should be unique"
    assert len(process1.process_id) == 8, "UUID should be 8 characters"
    assert process1.simple_id == "P0", "Simple ID should be P0"
    assert process2.simple_id == "P1", "Simple ID should be P1"
    
    # Test hex address generation
    assert len(process1.hex_address_sequence) == process1.burst_time, "Hex sequence length should match burst time"
    assert len(process2.hex_address_sequence) == process2.burst_time, "Hex sequence length should match burst time"
    
    # Test hex instruction addition
    process1.add_hex_instruction("0x1000")
    process1.add_hex_instruction("0x2000")
    assert len(process1.hex_instructions) == 2, "Should have 2 hex instructions"
    assert process1.hex_instructions[0] == "0x1000", "First hex instruction should be 0x1000"
    
    # Test address translation (without memory manager - should return None for page fault)
    result = process1.translate_address("0x1000")
    assert result is None, "Should return None for page fault when page not in table"
    
    print("✅ Enhanced process features tests PASSED")

def test_hex_address_translation():
    """Test hex address translation and memory integration"""
    print("\\n" + "="*60)
    print("  TEST 2: Hex Address Translation")
    print("="*60)
    
    Process.reset_id_counter()
    
    # Create memory manager and process
    memory = MemoryManager(total_frames=4, algorithm='FIFO')
    process = Process("HexTestProcess", 6, 16)  # 16KB = 4 pages
    memory.register_process(process)
    
    print(f"Process has {process.num_pages} pages")
    
    # Test hex address access
    test_addresses = ["0x1000", "0x1100", "0x2000", "0x1200"]
    expected_pages = [1, 1, 2, 1]  # Calculated based on PAGE_SIZE=4096
    
    results = []
    for i, hex_addr in enumerate(test_addresses):
        result = memory.access_hex_address(process, hex_addr)
        results.append(result)
        expected_page = expected_pages[i]
        
        print(f"Access {i+1}: {hex_addr} → Expected Page {expected_page}, Got status {result['status']}")
        
        # Verify page calculation
        virtual_addr = int(hex_addr, 16)
        calculated_page = virtual_addr // 4096  # PAGE_SIZE
        assert calculated_page == expected_page, f"Page calculation error for {hex_addr}"
        
        # Verify physical address generation on successful access
        if result['status'] in ['HIT', 'FAULT'] and result['frame'] is not None:
            assert result['physical_address'] is not None, "Physical address should be generated"
            assert result['virtual_address'] == hex_addr, "Virtual address should match input"
    
    # Test address translation with allocated pages
    for page_num in process.page_table:
        hex_addr = f"0x{page_num * 4096:04X}"
        physical_addr = process.translate_address(hex_addr)
        assert physical_addr is not None, f"Should translate allocated page {page_num}"
    
    print("✅ Hex address translation tests PASSED")

def test_interactive_controls():
    """Test interactive control features"""
    print("\\n" + "="*60)
    print("  TEST 3: Interactive Controls")
    print("="*60)
    
    Process.reset_id_counter()
    
    # Create memory manager and scheduler
    memory = MemoryManager(total_frames=4, algorithm='LRU')
    scheduler = CPUScheduler(algorithm='FCFS')
    
    # Test initial states
    assert not memory.is_paused, "Memory should not be paused initially"
    assert not scheduler.is_paused, "Scheduler should not be paused initially"
    assert not scheduler.step_mode, "Step mode should be disabled initially"
    
    # Test pause/resume
    memory.pause_simulation()
    assert memory.is_paused, "Memory should be paused"
    
    memory.resume_simulation()
    assert not memory.is_paused, "Memory should not be paused after resume"
    
    scheduler.pause_simulation()
    assert scheduler.is_paused, "Scheduler should be paused"
    
    scheduler.resume_simulation()
    assert not scheduler.is_paused, "Scheduler should not be paused after resume"
    
    # Test step mode
    scheduler.enable_step_mode()
    assert scheduler.step_mode, "Step mode should be enabled"
    
    scheduler.disable_step_mode()
    assert not scheduler.step_mode, "Step mode should be disabled"
    
    # Test execution delay setting
    original_delay = scheduler.execution_delay
    scheduler.set_execution_delay(0.1)
    assert scheduler.execution_delay == 0.1, "Execution delay should be updated"
    
    print("✅ Interactive controls tests PASSED")

def test_memory_cleanup():
    """Test automatic memory cleanup and deallocation"""
    print("\\n" + "="*60)
    print("  TEST 4: Memory Cleanup and Deallocation")
    print("="*60)
    
    Process.reset_id_counter()
    
    # Create memory manager and processes
    memory = MemoryManager(total_frames=6, algorithm='FIFO')
    process1 = Process("CleanupTest1", 4, 8)  # 2 pages
    process2 = Process("CleanupTest2", 3, 12) # 3 pages
    
    memory.register_process(process1)
    memory.register_process(process2)
    
    # Allocate some pages
    memory.access_page(process1, 0)
    memory.access_page(process1, 1)
    memory.access_page(process2, 0)
    memory.access_page(process2, 1)
    
    # Verify allocation
    assert len(process1.page_table) == 2, "Process1 should have 2 pages allocated"
    assert len(process2.page_table) == 2, "Process2 should have 2 pages allocated"
    
    initial_used_frames = len(memory.physical_memory.allocated_frames)
    initial_free_frames = len(memory.physical_memory.free_frames)
    
    print(f"Before cleanup: {initial_used_frames} used, {initial_free_frames} free")
    
    # Test process cleanup
    cleanup_result = memory.deallocate_process(process1)
    
    # Verify cleanup results
    assert len(process1.page_table) == 0, "Process1 page table should be empty"
    assert process1.process_id not in memory.registered_processes, "Process1 should be unregistered"
    assert len(cleanup_result['frames_freed']) == 2, "Should have freed 2 frames"
    
    final_used_frames = len(memory.physical_memory.allocated_frames)
    final_free_frames = len(memory.physical_memory.free_frames)
    
    print(f"After cleanup: {final_used_frames} used, {final_free_frames} free")
    
    assert final_used_frames == initial_used_frames - 2, "Should have 2 fewer used frames"
    assert final_free_frames == initial_free_frames + 2, "Should have 2 more free frames"
    
    print("✅ Memory cleanup tests PASSED")

def test_enhanced_statistics():
    """Test enhanced statistics tracking"""
    print("\\n" + "="*60)
    print("  TEST 5: Enhanced Statistics Tracking")
    print("="*60)
    
    Process.reset_id_counter()
    
    # Create components
    memory = MemoryManager(total_frames=4, algorithm='LRU')
    scheduler = CPUScheduler(algorithm='RR', time_quantum=2)
    
    # Create processes with instructions
    process1 = Process("StatTest1", 3, 8)
    process2 = Process("StatTest2", 2, 4)
    
    for i in range(3):
        process1.add_instruction(f"Instruction {i+1}")
    
    for i in range(2):
        process2.add_instruction(f"Instruction {i+1}")
    
    memory.register_process(process1)
    memory.register_process(process2)
    scheduler.add_process(process1)
    scheduler.add_process(process2)
    
    # Run simulation with very fast delay for testing
    scheduler.set_execution_delay(0.01)
    result = scheduler.run_realtime_simulation(memory)
    
    # Verify statistics
    assert result['total_time'] > 0, "Total time should be > 0"
    assert result['completed_processes'] == 2, "Should have completed 2 processes"
    assert result['average_waiting_time'] >= 0, "Average waiting time should be >= 0"
    assert result['average_turnaround_time'] > 0, "Average turnaround time should be > 0"
    assert len(result['memory_accesses']) > 0, "Should have memory accesses"
    assert len(result['hex_execution_log']) > 0, "Should have hex execution log"
    
    # Verify memory statistics
    memory_stats = memory.get_statistics()
    assert memory_stats['total_accesses'] > 0, "Should have memory accesses"
    assert memory_stats['hit_ratio'] >= 0, "Hit ratio should be >= 0"
    assert memory_stats['algorithm'] == 'LRU', "Algorithm should be LRU"
    
    # Verify process statistics
    for process in [process1, process2]:
        assert process.page_hits >= 0, "Page hits should be >= 0"
        assert process.page_faults >= 0, "Page faults should be >= 0"
        assert process.get_hit_ratio() >= 0, "Hit ratio should be >= 0"
        assert process.state == "TERMINATED", "Process should be terminated"
        # Note: is_allocated is set to False during cleanup, which happens automatically in enhanced scheduler
    
    print("✅ Enhanced statistics tests PASSED")

def test_integration_compatibility():
    """Test backward compatibility with original features"""
    print("\\n" + "="*60)
    print("  TEST 6: Integration and Backward Compatibility")
    print("="*60)
    
    Process.reset_id_counter()
    
    # Test that enhanced classes work with original interfaces
    process = Process("CompatibilityTest", 3, 4)
    memory = MemoryManager(total_frames=4, algorithm='FIFO')
    scheduler = CPUScheduler(algorithm='FCFS')
    
    # Test original interface methods
    memory.register_process(process)
    scheduler.add_process(process)
    
    # Test original page access method
    result = memory.access_page(process, 0)
    assert result['status'] in ['HIT', 'FAULT'], "Should return valid status"
    
    # Test that both simple_id and process_id work
    assert hasattr(process, 'simple_id'), "Should have simple_id for compatibility"
    assert hasattr(process, 'process_id'), "Should have process_id for enhanced features"
    
    # Test that enhanced features don't break original functionality
    process.add_instruction("Test instruction")
    assert len(process.instructions) == 1, "Should be able to add instructions"
    
    print("✅ Integration and compatibility tests PASSED")

def run_all_enhanced_tests():
    """Run all enhanced test suites"""
    print("="*70)
    print("    ENHANCED OS SIMULATOR v2.1 - TEST SUITE")
    print("    Testing Integration of aiss Features")
    print("="*70)
    
    try:
        test_enhanced_process_features()
        test_hex_address_translation()
        test_interactive_controls()
        test_memory_cleanup()
        test_enhanced_statistics()
        test_integration_compatibility()
        
        print("\\n" + "="*70)
        print("    🎉 ALL ENHANCED TESTS PASSED SUCCESSFULLY! 🎉")
        print("    ✓ UUID process identification")
        print("    ✓ Hex address translation")
        print("    ✓ Interactive controls")
        print("    ✓ Automatic memory cleanup")
        print("    ✓ Enhanced statistics")
        print("    ✓ Backward compatibility")
        print("="*70)
        
        return True
        
    except AssertionError as e:
        print(f"\\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\\n💥 UNEXPECTED ERROR: {e}")
        return False

if __name__ == "__main__":
    success = run_all_enhanced_tests()
    sys.exit(0 if success else 1)
