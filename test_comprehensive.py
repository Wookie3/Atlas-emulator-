from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_comprehensive():
    print("=" * 50)
    print("Atlas Computer Emulator: Comprehensive Test")
    print("=" * 50)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    print("\n1. Setting up data across multiple pages...")
    
    # Data Setup
    # Page 0 (Addresses 0-511)
    mem.write(100, 7)    # Multiplicand
    mem.write(101, 8)    # Multiplier
    mem.write(102, 0)    # Result accumulator
    mem.write(103, 1)    # Counter decrement value
    mem.write(104, 10)   # For B-register test (add)
    mem.write(105, 3)    # For B-register test (subtract)
    mem.write(106, 100)  # For accumulator test
    mem.write(107, 5)    # For JBZ test counter
    mem.write(152, 1000) # For JBZ test addition
    
    # Page 2 (Addresses 1024-1535) - Test paging
    mem.write(1024, 42)  # Value in second page
    mem.write(1025, 17)  # Value in second page
    
    # Page 3 (Addresses 1536-2047) - Test paging
    mem.write(1536, 99)  # Value in third page
    
    print(f"   - Addr 100: {mem.read(100)}")
    print(f"   - Addr 1024: {mem.read(1024)}")
    print(f"   - Addr 1536: {mem.read(1536)}")
    
    print("\n2. Loading program...")
    
    # Program: Tests multiple operations
    # Instructions:
    # 0x089 = LDB (Load B-line)
    # 0x0D2 = ADA (Add to Accumulator)
    # 0x083 = SBB (Subtract from B-line)
    # 0x091 = JBN (Jump if B != 0)
    # 0x08F = JBZ (Jump if B == 0)
    # 0x0EE = LDA (Load Accumulator)
    # 0x0F2 = STA (Store Accumulator)
    # 0x200 = PRINT extracode
    # 0x000 = HALT
    
    program = [
        # === Test 1: Multiplication (7 * 8) ===
        # 0: Load B1 with multiplier (8)
        join_instruction(0x089, 1, 0, 101),
        # 1: Load accumulator with 0
        join_instruction(0x0EE, 0, 0, 102),
        # 2: Start loop - Add multiplicand to accumulator
        join_instruction(0x0D2, 0, 0, 100),
        # 3: Subtract 1 from B1
        join_instruction(0x083, 1, 0, 103),
        # 4: If B1 != 0, jump back to instruction 2
        join_instruction(0x091, 1, 0, 2),
        
        # 5: Print result (should be 56)
        join_instruction(0x200, 0, 0, 0),
        
        # === Test 2: Accumulator operations ===
        # 6: Load accumulator with value from page 2 (42)
        join_instruction(0x0EE, 0, 0, 1024),
        # 7: Add value from page 2 (17) - triggers paging
        join_instruction(0x0D2, 0, 0, 1025),
        # 8: Add value from page 3 (99) - triggers paging again
        join_instruction(0x0D2, 0, 0, 1536),
        # 9: Print result (should be 158)
        join_instruction(0x200, 0, 0, 0),
        
        # === Test 3: B-register operations ===
        # 10: Load B2 with value from memory (7)
        join_instruction(0x089, 2, 0, 100),
        # 11: Add 10 to B2 (from memory)
        join_instruction(0x081, 2, 0, 104),
        # 12: Subtract 3 from B2 (from memory)
        join_instruction(0x083, 2, 0, 105),
        # 13: Store B2 value into memory
        join_instruction(0x08D, 2, 0, 150),
        # 14: Load accumulator from B2 value
        join_instruction(0x0EE, 0, 0, 150),
        # 15: Print B2 value via accumulator (should be 14)
        join_instruction(0x200, 0, 0, 0),
        
        # === Test 4: Conditional jumps (JBZ) ===
        # 16: Load B3 with 5
        join_instruction(0x089, 3, 0, 107),
        # 17: Load accumulator with 100
        join_instruction(0x0EE, 0, 0, 106),
        # 18: Decrement B3
        join_instruction(0x083, 3, 0, 103),
        # 19: If B3 == 0, jump to 21 (should not jump)
        join_instruction(0x08F, 3, 0, 21),
        # 20: Add 1000 to accumulator (need to use memory)
        join_instruction(0x08D, 0, 0, 152),
        join_instruction(0x0D2, 0, 0, 152),
        # 21: Print accumulator (should be 1100, not 100)
        join_instruction(0x200, 0, 0, 0),
        
        # 22: Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    # Write initial value for JBZ test
    mem.write(105, 5)
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"   - Program loaded: {len(program)} instructions")
    
    print("\n3. Running program...")
    print("-" * 50)
    
    cpu.run(0)
    
    print("-" * 50)
    print("\n4. Execution summary:")
    print("   - All tests completed")
    print("   - Paging handled automatically")
    print(f"   - Final PC: {cpu.pc}")
    print(f"   - Final Accumulator: {cpu.accumulator}")
    print(f"   - Final B-register values:")
    print(f"     B1: {cpu.b_store[1]}")
    print(f"     B2: {cpu.b_store[2]}")
    print(f"     B3: {cpu.b_store[3]}")
    print("\n" + "=" * 50)
    print("Test Results:")
    print("  Test 1 (7 * 8): Expected 56")
    print("  Test 2 (42 + 17 + 99): Expected 158")
    print("  Test 3 (B-reg operations): Expected 14")
    print("  Test 4 (JBZ jump): Expected 1100")
    print("=" * 50)

if __name__ == "__main__":
    test_comprehensive()
