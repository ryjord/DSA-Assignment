# Libs
import os
import glob
import json

# Utils
from utils.helpers import load_test_case

# Runs the VRP algorithms via an interactive CLI
def interactive_cli(bakery_builder, Algorithm):
    # Determine the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Search path for JSON test cases
    tests_path = os.path.join(base_dir, 'tests', '*.json')
    files = sorted(glob.glob(tests_path))

    # Initialise
    tests = []

    # Loop through each file
    for file in files:
        try:
            with open(file, 'r') as test_files:
                # Parse JSON payload
                data = json.load(test_files)

                # Extract label
                label = data.get("label", os.path.basename(file))
                tests.append((file, label))
        except Exception as error:
            tests.append((file, os.path.basename(file)))

    # Menu
    while True:
        # Menu printout
        print("\n" + "=" * 40)
        print("        VRP Algorithm Tester        ")
        print("=" * 40)
        print("[0] Default Bakery Example")

        # Loop through all Cases
        for i, (filepath, label) in enumerate(tests, 1):
            print(f"[{i}] {label}")

        # Menu Options
        print("-" * 40)
        print("[A] Run All Tests (Comparison Mode)")
        print("[V] Visualise All Tests")
        print("[Q] Quit")
        print("=" * 40)

        # User Input
        choice = input("\nSelect an option: ").strip().upper()

        # Key Match
        match choice:
            # Quit
            case 'Q':
                print("Exiting...")
                break

            # Run All
            case 'A':
                print("\n" + "=" * 80)
                print(" Running ALL tests...")
                print("=" * 80)

                # Run Default Main
                bakery_instance = bakery_builder()
                Algorithm(bakery_instance, label="Bakery Example", hide_details=True)

                # Run Filecases
                for filepath, label in tests:
                    instance = load_test_case(filepath)

                    # Ensure loaded
                    if instance is not None:
                        Algorithm(instance, label=label, hide_details=True)

                print("\n>> All tests completed!")

            # Visualise
            case 'V':
                print("\n" + "=" * 80)
                print(" Generating Visualisations for ALL tests...")
                print("=" * 80)

                # Bakery
                bakery_instance = bakery_builder()
                Algorithm(bakery_instance, label="Bakery Example", hide_details=False)

                # Loop through test cases
                for filepath, label in tests:
                    instance = load_test_case(filepath)

                    # Ensure loaded
                    if instance is not None:
                        Algorithm(instance, label=label, hide_details=False)
                print("\n>> All visualisations generated and saved!")

            # Default
            case '0':
                bakery_instance = bakery_builder()
                Algorithm(bakery_instance, label="Bakery Example")

            # Other Cases
            case _:
                try:
                    index = int(choice)

                    # Number within range
                    if 1 <= index <= len(tests):
                        # File used bvased on index
                        filepath, label = tests[index-1]
                        instance = load_test_case(filepath)

                        # Ensure Loaded Again
                        # Note : i could probably isolate this to call these checks once
                        if instance is not None:
                            Algorithm(instance, label=label)
                    else:
                        print("Invalid option. Please enter a valid number.")
                except Exception as error:
                    # Invalid
                    print("Invalid input. Please enter a valid choice from the menu.")
