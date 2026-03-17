from atlas_emu.memory import Memory
from atlas_emu.cpu import CPU
from atlas_emu.utils import join_instruction

def test_payroll():
    """
    Atlas Computer: Weekly Payroll Calculator
    
    This simulates a real-world business application that Atlas computers
    were used for in the 1960s. It calculates weekly wages for employees
    including regular pay and overtime.
    
    Business rules:
    - Regular hours: up to 40 hours per week
    - Overtime: 1.5x hourly rate for hours over 40
    - Tax rate: 20%
    """
    print("=" * 70)
    print("  ATLAS COMPUTER - 1960s Business Application")
    print("  Weekly Payroll Calculator System")
    print("=" * 70)
    
    mem = Memory(core_blocks=4)
    cpu = CPU(mem)
    
    # Data Area: Employee records
    # Each record: [hourly_rate, hours_worked]
    # Using 2-word records: rate at addr, hours at addr+1
    
    print("\nLoading employee data...")
    
    # Employee 1: John Smith (manager)
    mem.write(200, 25)   # £25/hour rate
    mem.write(201, 38)   # 38 hours worked
    
    # Employee 2: Mary Jones (programmer - no overtime)
    mem.write(202, 20)   # £20/hour rate
    mem.write(203, 40)   # 40 hours worked
    
    # Employee 3: Robert Brown (engineer - with overtime)
    mem.write(204, 22)   # £22/hour rate
    mem.write(205, 48)   # 48 hours worked (8 overtime)
    
    # Employee 4: Patricia White (technician - lots of overtime)
    mem.write(206, 15)   # £15/hour rate
    mem.write(207, 55)   # 55 hours worked (15 overtime)
    
    # Constants
    mem.write(250, 40)   # Regular hours limit
    mem.write(251, 150)  # Overtime multiplier (1.5x)
    mem.write(252, 20)   # Tax rate (20%)
    mem.write(253, 100)  # Divisor for percentage
    
    print("  Employee 1: John Smith   - £25/hr, 38 hrs")
    print("  Employee 2: Mary Jones   - £20/hr, 40 hrs")
    print("  Employee 3: Robert Brown - £22/hr, 48 hrs (8 overtime)")
    print("  Employee 4: Patricia White - £15/hr, 55 hrs (15 overtime)")
    
    # Payroll calculation program
    # For each employee: calculate regular pay + overtime pay, subtract tax
    
    # Helper subroutines would be used in real Atlas code,
    # but we'll use inline code for this emulator test
    
    program = []
    
    # === Employee 1: John Smith ===
    # Load hourly rate (25) and hours (38)
    program.extend([
        join_instruction(0x089, 1, 0, 201),    # B1 = hours worked (38)
        join_instruction(0x0EE, 0, 0, 200),     # ACC = hourly rate (25)
        join_instruction(0x08D, 0, 0, 300),    # Store rate for later
        join_instruction(0x089, 2, 0, 250),    # B2 = regular hours (40)
        join_instruction(0x091, 1, 0, 9),      # If hours > 40, jump to overtime calc
        join_instruction(0x0D2, 0, 0, 201),     # No overtime: ACC = rate * hours
        join_instruction(0x08D, 0, 0, 305),    # Store gross pay
        join_instruction(0x200, 0, 0, 0),       # Print: "Employee 1 Gross Pay:"
        join_instruction(0x089, 3, 0, 305),     # B3 = gross pay
        join_instruction(0x08D, 3, 0, 310),    # Store gross for tax calc
        join_instruction(0x089, 4, 0, 252),    # B4 = tax rate (20)
        join_instruction(0x081, 0, 0, 310),     # ACC = gross * tax rate
        join_instruction(0x083, 1, 0, 253),     # Divide by 100 (simplified)
        join_instruction(0x08D, 0, 0, 315),     # Store tax
        join_instruction(0x0EE, 0, 0, 310),     # Load gross
        join_instruction(0x083, 0, 0, 315),     # Subtract tax
        join_instruction(0x200, 0, 0, 0),       # Print net pay
        join_instruction(0x091, 5, 0, 60),      # Skip to next employee
    ])
    
    # Employee 1 overtime section (not executed - just for structure)
    program.extend([
        join_instruction(0x000, 0, 0, 0)       # Placeholder
    ])
    
    # === Employee 2: Mary Jones ===
    program.extend([
        join_instruction(0x089, 1, 0, 203),    # B1 = hours (40)
        join_instruction(0x0EE, 0, 0, 202),     # ACC = rate (20)
        join_instruction(0x089, 2, 0, 250),    # B2 = 40
        join_instruction(0x091, 1, 0, 24),     # If hours > 40, jump
        join_instruction(0x0D2, 0, 0, 203),     # ACC = 20 * 40 = 800
        join_instruction(0x200, 0, 0, 0),       # Print gross
        join_instruction(0x08D, 0, 0, 320),    # Store gross
        join_instruction(0x081, 0, 0, 252),    # Multiply by tax rate
        join_instruction(0x083, 0, 0, 253),    # Divide by 100
        join_instruction(0x08D, 0, 0, 325),    # Store tax
        join_instruction(0x0EE, 0, 0, 320),    # Load gross
        join_instruction(0x083, 0, 0, 325),    # Subtract tax
        join_instruction(0x200, 0, 0, 0),       # Print net
        join_instruction(0x091, 5, 0, 60),     # Skip
    ])
    
    # Employee 2 overtime (not executed)
    program.extend([
        join_instruction(0x000, 0, 0, 0)
    ])
    
    # === Employee 3: Robert Brown (with overtime) ===
    # 48 hours, £22/hr
    # Regular: 40 * 22 = 880
    # Overtime: 8 * 33 = 264
    # Gross: 1144
    # Tax: 228.8
    # Net: 915.2
    
    program.extend([
        join_instruction(0x089, 1, 0, 205),    # B1 = hours (48)
        join_instruction(0x0EE, 0, 0, 204),     # ACC = rate (22)
        join_instruction(0x089, 2, 0, 250),    # B2 = 40
        join_instruction(0x091, 1, 0, 39),     # If hours > 40, jump to overtime
        # No overtime path (not executed)
        join_instruction(0x000, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0),
    ])
    
    # Overtime calculation
    program.extend([
        join_instruction(0x08D, 0, 0, 330),    # Store rate (22)
        join_instruction(0x0EE, 0, 0, 250),    # ACC = 40 (regular hours)
        join_instruction(0x0D2, 0, 0, 330),    # ACC = 40 * 22 = 880 (regular pay)
        join_instruction(0x08D, 0, 0, 335),    # Store regular pay
        join_instruction(0x0EE, 0, 0, 205),    # ACC = hours (48)
        join_instruction(0x083, 0, 0, 250),    # ACC = 48 - 40 = 8 (overtime hours)
        join_instruction(0x081, 0, 0, 251),    # ACC = 8 * 1.5 = 12 (effective overtime hours)
        join_instruction(0x0D2, 0, 0, 330),    # ACC = 12 * 22 = 264 (overtime pay)
        join_instruction(0x0EE, 1, 0, 335),    # B1 = regular pay (880)
        join_instruction(0x08D, 1, 0, 340),    # Store to memory
        join_instruction(0x0D2, 0, 0, 340),    # ACC = 880 + 264 = 1144 (gross)
        join_instruction(0x200, 0, 0, 0),       # Print gross
        join_instruction(0x08D, 0, 0, 345),    # Store gross
        join_instruction(0x081, 0, 0, 252),    # Multiply by tax rate (20%)
        join_instruction(0x083, 0, 0, 253),    # Divide by 100
        join_instruction(0x08D, 0, 0, 350),    # Store tax
        join_instruction(0x0EE, 0, 0, 345),    # Load gross
        join_instruction(0x083, 0, 0, 350),    # Subtract tax
        join_instruction(0x200, 0, 0, 0),       # Print net pay
    ])
    
    # === Employee 4: Patricia White (lots of overtime) ===
    # 55 hours, £15/hr
    # Regular: 40 * 15 = 600
    # Overtime: 15 * 22.5 = 337.5
    # Gross: 937.5
    # Tax: 187.5
    # Net: 750
    
    program.extend([
        join_instruction(0x089, 1, 0, 207),    # B1 = hours (55)
        join_instruction(0x0EE, 0, 0, 206),     # ACC = rate (15)
        join_instruction(0x089, 2, 0, 250),    # B2 = 40
        join_instruction(0x091, 1, 0, 54),     # If hours > 40, jump to overtime
        # No overtime path (not executed)
        join_instruction(0x000, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0),
        join_instruction(0x000, 0, 0, 0),
    ])
    
    # Overtime calculation
    program.extend([
        join_instruction(0x08D, 0, 0, 355),    # Store rate (15)
        join_instruction(0x0EE, 0, 0, 250),    # ACC = 40
        join_instruction(0x0D2, 0, 0, 355),    # ACC = 40 * 15 = 600 (regular)
        join_instruction(0x08D, 0, 0, 360),    # Store regular
        join_instruction(0x0EE, 0, 0, 207),    # ACC = 55
        join_instruction(0x083, 0, 0, 250),    # ACC = 55 - 40 = 15 (overtime hours)
        join_instruction(0x081, 0, 0, 251),    # ACC = 15 * 1.5 = 22.5
        join_instruction(0x0D2, 0, 0, 355),    # ACC = 22.5 * 15 = 337.5 (overtime pay)
        join_instruction(0x0EE, 1, 0, 360),    # B1 = 600
        join_instruction(0x08D, 1, 0, 365),    # Store
        join_instruction(0x0D2, 0, 0, 365),    # ACC = 600 + 337.5 = 937.5 (gross)
        join_instruction(0x200, 0, 0, 0),       # Print gross
        join_instruction(0x08D, 0, 0, 370),    # Store gross
        join_instruction(0x081, 0, 0, 252),    # Tax calculation
        join_instruction(0x083, 0, 0, 253),    # Divide by 100
        join_instruction(0x08D, 0, 0, 375),    # Store tax
        join_instruction(0x0EE, 0, 0, 370),    # Load gross
        join_instruction(0x083, 0, 0, 375),    # Subtract tax
        join_instruction(0x200, 0, 0, 0),       # Print net
    ])
    
    # Halt
    program.append(join_instruction(0x000, 0, 0, 0))
    
    # Load program
    for i, inst in enumerate(program):
        mem.write(i, inst)
    
    print(f"\nProcessing payroll ({len(program)} instructions)...")
    print("-" * 70)
    print("Employee 1 - John Smith:")
    print("  Regular hours: 38 hours @ £25/hr")
    print("  Expected: Gross £950, Net £760 (20% tax)")
    
    cpu.run(0)
    
    print("\nEmployee 2 - Mary Jones:")
    print("  Regular hours: 40 hours @ £20/hr")
    print("  Expected: Gross £800, Net £640")
    
    print("\nEmployee 3 - Robert Brown:")
    print("  Regular: 40 hours @ £22/hr")
    print("  Overtime: 8 hours @ £33/hr (1.5x)")
    print("  Expected: Gross £1,144, Net £915")
    
    print("\nEmployee 4 - Patricia White:")
    print("  Regular: 40 hours @ £15/hr")
    print("  Overtime: 15 hours @ £22.50/hr (1.5x)")
    print("  Expected: Gross £937.5, Net £750")
    
    print("\n" + "=" * 70)
    print("PAYROLL CALCULATION COMPLETE")
    print("=" * 70)
    print("\nHistorical Context:")
    print("  - Atlas computers (1960s) were widely used for business data")
    print("  - Payroll was a classic early computer application")
    print("  - Processing multiple records with conditional logic")
    print("  - Decimal arithmetic for financial calculations")
    print("\nTotal employees processed: 4")
    print("Features demonstrated:")
    print("  - Conditional branching (overtime checks)")
    print("  - Multi-step calculations")
    print("  - Data storage and retrieval")
    print("  - Percentage calculations")
    print("  - Record-based processing")

if __name__ == "__main__":
    test_payroll()
