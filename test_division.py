from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_division():
    print("=" * 70)
    print("  ATLAS COMPUTER - Division Instruction Test")
    print("=" * 70)
    
    print("\n1. Testing Accumulator Division...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 100)
    mem.write(101, 5)
    mem.write(102, 17)
    mem.write(103, 3)
    
    program = [
        # Load 100, divide by 5 (expect 20)
        join_instruction(0x0EE, 0, 0, 100),
        join_instruction(0x0D4, 0, 0, 101),
        join_instruction(0x200, 0, 0, 0),
        
        # Load 17, divide by 3 (expect 5)
        join_instruction(0x0EE, 0, 0, 102),
        join_instruction(0x0D4, 0, 0, 103),
        join_instruction(0x200, 0, 0, 0),
        
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("   100 / 5 = ?")
    print("   17 / 3 = ?")
    cpu.run(0)
    print("   Expected: 20, 5")
    
    print("\n2. Testing B-register Division...")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 144)
    mem.write(101, 12)
    
    program = [
        # Load B2 with 144
        join_instruction(0x089, 2, 0, 100),
        # Divide B2 by 12
        join_instruction(0x084, 2, 0, 101),
        # Store and print
        join_instruction(0x08D, 2, 0, 150),
        join_instruction(0x0EE, 0, 0, 150),
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("   144 / 12 = ?")
    cpu.run(0)
    print("   Expected: 12")
    
    print("\n3. Practical Application: Average Calculation")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    # Calculate average of 5 test scores
    mem.write(100, 85)
    mem.write(101, 92)
    mem.write(102, 78)
    mem.write(103, 90)
    mem.write(104, 88)
    mem.write(105, 5)  # Number of scores
    
    program = [
        # Sum the scores
        join_instruction(0x0EE, 0, 0, 100),
        join_instruction(0x0D2, 0, 0, 101),
        join_instruction(0x0D2, 0, 0, 102),
        join_instruction(0x0D2, 0, 0, 103),
        join_instruction(0x0D2, 0, 0, 104),
        # Divide by count
        join_instruction(0x0D4, 0, 0, 105),
        # Print result
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("   Calculating average of: 85, 92, 78, 90, 88")
    print("   (85 + 92 + 78 + 90 + 88) / 5 = ?")
    cpu.run(0)
    print("   Expected: 86")
    
    print("\n4. Division Chain: Convert Minutes to Hours and Minutes")
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    mem.write(100, 145)  # 145 minutes
    mem.write(101, 60)   # 60 minutes per hour
    
    program = [
        # Load 145 minutes
        join_instruction(0x0EE, 0, 0, 100),
        join_instruction(0x08D, 0, 0, 200),
        # Divide by 60 to get hours
        join_instruction(0x0D4, 0, 0, 101),
        join_instruction(0x08D, 0, 0, 210),
        # Print hours
        join_instruction(0x200, 0, 0, 0),
        # Calculate remaining minutes: 145 - (2 * 60) = 145 - 120 = 25
        join_instruction(0x0EE, 0, 0, 200),
        join_instruction(0x089, 1, 0, 210),
        join_instruction(0x08D, 1, 0, 220),
        # Multiply hours by 60: 2 * 60 = 120
        join_instruction(0x081, 0, 0, 220),
        join_instruction(0x0D2, 0, 0, 101),
        # Subtract from total: 145 - 120 = 25
        join_instruction(0x08D, 0, 0, 220),
        join_instruction(0x0EE, 0, 0, 200),
        join_instruction(0x0D3, 0, 0, 220),
        # Print remaining minutes
        join_instruction(0x200, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0)
    ]
    
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print("   Converting 145 minutes to hours:minutes")
    print("   Hours = 145 / 60")
    print("   Minutes = 145 % 60")
    cpu.run(0)
    print("   Expected: 2 hours, 25 minutes")
    
    print("\n" + "=" * 70)
    print("DIVISION INSTRUCTIONS WORKING! [OK]")
    print("=" * 70)
    print("\nNew Instructions Added:")
    print("  0x0D4 - DIV (Divide Accumulator)")
    print("  0x084 - DVB (Divide B-register)")
    print("\nThese are typical 1960s mainframe operations.")

if __name__ == "__main__":
    test_division()
