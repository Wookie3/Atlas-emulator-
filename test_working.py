from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_working():
    print("=" * 50)
    print("Atlas Computer Emulator: Working Test Suite")
    print("=" * 50)
    
    print("\n1. Multiplication Test (7 * 8)...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 7)
    mem.write(101, 8)
    mem.write(102, 0)
    mem.write(103, 1)
    
    program = [
        join_instruction(0x089, 1, 0, 101),
        join_instruction(0x0EE, 0, 0, 102),
        join_instruction(0x0D2, 0, 0, 100),
        join_instruction(0x083, 1, 0, 103),
        join_instruction(0x091, 1, 0, 2),
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    cpu.run(0)
    print(f"   Result: {cpu.accumulator} (Expected: 56)")
    assert cpu.accumulator == 56, "Multiplication test failed!"
    print("   [PASS]")
    
    print("\n2. Cross-page Addition (42 + 17 + 99)...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(1024, 42)
    mem.write(1025, 17)
    mem.write(1536, 99)
    
    program = [
        join_instruction(0x0EE, 0, 0, 1024),
        join_instruction(0x0D2, 0, 0, 1025),
        join_instruction(0x0D2, 0, 0, 1536),
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    cpu.run(0)
    print(f"   Result: {cpu.accumulator} (Expected: 158)")
    assert cpu.accumulator == 158, "Addition test failed!"
    print("   [PASS]")
    
    print("\n3. B-register Operations (7 + 10 - 3)...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 7)
    mem.write(101, 10)
    mem.write(102, 3)
    
    program = [
        join_instruction(0x089, 2, 0, 100),
        join_instruction(0x081, 2, 0, 101),
        join_instruction(0x083, 2, 0, 102),
        join_instruction(0x08D, 2, 0, 150),
        join_instruction(0x0EE, 0, 0, 150),
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    cpu.run(0)
    print(f"   Result: {cpu.accumulator} (Expected: 14)")
    assert cpu.accumulator == 14, "B-register test failed!"
    print("   [PASS]")
    
    print("\n4. JBZ Jump Test...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 100)
    mem.write(103, 1)
    mem.write(107, 5)
    mem.write(108, 1000)
    
    program = [
        join_instruction(0x089, 3, 0, 107),
        join_instruction(0x0EE, 0, 0, 100),
        join_instruction(0x083, 3, 0, 103),
        join_instruction(0x08F, 3, 0, 6),
        join_instruction(0x0D2, 0, 0, 108),
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    cpu.run(0)
    print(f"   Result: {cpu.accumulator} (Expected: 1100)")
    assert cpu.accumulator == 1100, "JBZ test failed!"
    print("   [PASS]")
    
    print("\n5. JBN Jump Test...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 100)
    mem.write(108, 1)
    mem.write(109, 1000)
    
    program = [
        join_instruction(0x089, 4, 0, 108),
        join_instruction(0x0EE, 0, 0, 100),
        join_instruction(0x091, 4, 0, 6),
        join_instruction(0x0D2, 0, 0, 109),
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    cpu.run(0)
    print(f"   Result: {cpu.accumulator} (Expected: 100)")
    assert cpu.accumulator == 100, "JBN test failed!"
    print("   [PASS]")
    
    print("\n6. Memory Paging Test...")
    mem = Memory(core_blocks=2)
    
    mem.write(0, 111)
    mem.write(512, 222)
    mem.write(1024, 333)
    mem.write(1536, 444)
    
    v0 = mem.read(0)
    v512 = mem.read(512)
    v1024 = mem.read(1024)
    v1536 = mem.read(1536)
    
    print(f"   Page 0: {v0} (Expected: 111)")
    print(f"   Page 1: {v512} (Expected: 222)")
    print(f"   Page 2: {v1024} (Expected: 333)")
    print(f"   Page 3: {v1536} (Expected: 444)")
    
    assert v0 == 111 and v512 == 222 and v1024 == 333 and v1536 == 444, "Paging test failed!"
    print("   [PASS]")
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED! [OK]")
    print("=" * 50)
    print("\nThe Atlas emulator is working correctly!")
    print("Features tested:")
    print("  - 48-bit accumulator arithmetic")
    print("  - 24-bit B-register operations")
    print("  - Conditional jumps (JBZ, JBN)")
    print("  - Virtual memory with paging")
    print("  - Instruction fetching and decoding")
    print("  - Loops and control flow")

if __name__ == "__main__":
    test_working()
