# Libs
import os
import glob
import json

# Utils
from utils.helpers import load_test_case


# --- CLI ---

# Renders the interactive CLI menu and handles user input for running algorithms
def interactive_cli(bakery_builder, solver):
    # Scan for JSONs
    files = sorted(glob.glob("tests/*.json"))
    tests = []
    
    for f in files:
        try:
            with open(f, 'r') as fh:
                data = json.load(fh)
                label = data.get("label", os.path.basename(f))
                tests.append((f, label))
        except Exception:
            tests.append((f, os.path.basename(f)))
            
    while True:
        print("\n" + "=" * 40)
        print("        VRP Algorithm Tester        ")
        print("=" * 40)
        print("[0] Default Bakery Example")
        for i, (filepath, label) in enumerate(tests, 1):
            print(f"[{i}] {label}")
        print("-" * 40)
        print("[A] Run All Tests (Comparison Mode)")
        print("[Q] Quit")
        print("=" * 40)
        
        choice = input("\nSelect an option: ").strip().upper()
        
        if choice == 'Q':
            print("Exiting...")
            break
            
        elif choice == 'A':
            print("\n" + "=" * 80)
            print("  Running ALL tests in bulk...")
            print("=" * 80)
            
            # Run Bakery
            bakery_instance = bakery_builder()
            solver(bakery_instance, label="Bakery Example", hide_details=True)
            
            # Run All Files
            for filepath, label in tests:
                instance = load_test_case(filepath)
                if instance:
                    solver(instance, label=label, hide_details=True)
                    
            print("\n>> All tests completed!")
            
        elif choice == '0':
            bakery_instance = bakery_builder()
            solver(bakery_instance, label="Bakery Example")
            
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(tests):
                    filepath, label = tests[idx-1]
                    instance = load_test_case(filepath)
                    if instance:
                        solver(instance, label=label)
                else:
                    print("Invalid option. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid choice from the menu.")
