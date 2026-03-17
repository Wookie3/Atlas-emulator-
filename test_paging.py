from atlas_emu.memory import Memory

def test_paging():
    print("--- Atlas Memory: Paging/Swap Test ---")
    
    # 2 core blocks (1024 words total RAM)
    # Page size is 512.
    # So RAM can only hold 2 pages at once.
    mem = Memory(core_blocks=2)
    
    print("Writing to Page 0 (addr 0)...")
    mem.write(0, 100)
    
    print("Writing to Page 1 (addr 512)...")
    mem.write(512, 200)
    
    print("--- PAR Status ---")
    print(f"Pages in PAR: {list(mem.par.keys())}")
    
    print("\nWriting to Page 2 (addr 1024) - This should trigger a swap (Page 0 out)...")
    mem.write(1024, 300)
    
    print("--- PAR Status ---")
    print(f"Pages in PAR: {list(mem.par.keys())}")
    
    print("\nReading back Page 0 (addr 0) - This should trigger a swap (Page 1 out)...")
    val = mem.read(0)
    print(f"Value at addr 0: {val} (Expected: 100)")
    
    print("--- PAR Status ---")
    print(f"Pages in PAR: {list(mem.par.keys())}")

if __name__ == "__main__":
    test_paging()
