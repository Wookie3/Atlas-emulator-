from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_debug():
    print("=" * 50)
    print("Atlas: Debugging Multiplication Loop")
    print("=" * 50)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    print("\nSetup:")
    mem.write(100, 3)   # Multiplicand
    mem.write(101, 5)   # Loop counter
    mem.write(102, 0)   # Initial accumulator
    mem.write(103, 1)   # Decrement value
    
    print(f"  Addr 100 (multiplicand): {mem.read(100)}")
    print(f"  Addr 101 (counter): {mem.read(101)}")
    print(f"  Addr 102 (init ACC): {mem.read(102)}")
    print(f"  Addr 103 (decrement): {mem.read(103)}")
    
    program = [
        # 0: Load B1 with loop counter (5)
        join_instruction(0x089, 1, 0, 101),
        # 1: Load accumulator with 0
        join_instruction(0x0EE, 0, 0, 102),
        # 2: Start loop: Add multiplicand (3) to accumulator
        join_instruction(0x0D2, 0, 0, 100),
        # 3: Decrement B1 by 1
        join_instruction(0x083, 1, 0, 103),
        # 4: Jump if B1 != 0 back to instruction 2
        join_instruction(0x091, 1, 0, 2),
        # 5: Print result (should be 15)
        join_instruction(0x200, 0, 0, 0),
        # 6: Halt
        join_instruction(0x000, 0, 0, 0)
    ]
    
    print("\nProgram:")
    for i, inst in enumerate(program):
        mem.write(i, inst)
        print(f"  Addr {i}: {hex(inst)}")
    
    print("\nExecution trace:")
    cpu.pc = 0
    cpu.running = True
    cpu.b_store[0] = 0
    
    step_count = 0
    max_steps = 20
    
    while cpu.running and step_count < max_steps:
        step_count += 1
        
        # Fetch
        inst = cpu.fetch()
        f, ba, bm, s = cpu.decode(inst)
        
        # Calculate effective address
        effective_addr = (s + cpu.b_store[bm]) & 0xFFFFFF
        
        print(f"\nStep {step_count}: PC={cpu.pc-1}")
        print(f"  Instruction: {hex(inst)}")
        print(f"  F={hex(f)}, Ba={ba}, Bm={bm}, S={s}")
        print(f"  B[{bm}]={cpu.b_store[bm]}")
        print(f"  Effective addr: {effective_addr}")
        
        # Execute
        if f == 0x089:  # LDB
            val = mem.read(effective_addr)
            cpu.b_store[ba] = val & 0xFFFFFF
            print(f"  LDB B{ba} = mem[{effective_addr}] = {val}")
            
        elif f == 0x0EE:  # LDA
            val = mem.read(effective_addr)
            cpu.accumulator = val & 0xFFFFFFFFFFFF
            print(f"  LDA ACC = mem[{effective_addr}] = {val}")
            
        elif f == 0x0D2:  # ADA
            val = mem.read(effective_addr)
            cpu.accumulator = (cpu.accumulator + val) & 0xFFFFFFFFFFFF
            print(f"  ADA ACC = ACC + mem[{effective_addr}] = {val}")
            print(f"  New ACC: {cpu.accumulator}")
            
        elif f == 0x083:  # SBB
            print(f"  SBB B{ba} = B{ba} - effective_addr({effective_addr})")
            cpu.b_store[ba] = (cpu.b_store[ba] - effective_addr) & 0xFFFFFF
            print(f"  New B{ba}: {cpu.b_store[ba]}")
            
        elif f == 0x091:  # JBN
            print(f"  JBN B{ba} != 0 -> addr {effective_addr}")
            print(f"  B{ba} = {cpu.b_store[ba]}")
            if cpu.b_store[ba] != 0:
                cpu.pc = effective_addr
                print(f"  JUMPING to {effective_addr}")
            else:
                print(f"  NOT jumping")
                
        elif f == 0x200:  # PRINT
            print(f"  PRINT ACC = {cpu.accumulator}")
            
        elif f == 0x000:  # HALT
            cpu.running = False
            print(f"  HALT")
            
        cpu.b_store[0] = 0
    
    print(f"\nFinal state:")
    print(f"  ACC: {cpu.accumulator}")
    print(f"  B1: {cpu.b_store[1]}")
    print(f"  PC: {cpu.pc}")

if __name__ == "__main__":
    test_debug()
