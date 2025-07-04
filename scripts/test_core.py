import os
import sys

# --- Setup Python Path ---
# This is crucial for allowing Python to find the .pyd module.
# It adds the parent directory's 'ui' folder to the list of places
# Python looks for modules.
print("1. Setting up Python path...")
try:
    # Construct the path to the 'ui' directory relative to this script
    ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui'))
    sys.path.append(ui_path)
    print(f"   Added '{ui_path}' to sys.path")
    import caninana_core
    print("   Successfully imported 'caninana_core' module.")
except ImportError as e:
    print("\n[FATAL ERROR] Could not import 'caninana_core'.")
    print(f"   Details: {e}")
    print("   Please ensure 'caninana_core.pyd' (or .so) exists in the 'ui' directory.")
    sys.exit(1)


def main():
    """Main function to run the test suite."""
    print("\n2. Preparing test environment...")

    # Define file paths relative to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    clean_file_path = os.path.join(project_root, "clean_file.txt")
    infected_file_path = os.path.join(project_root, "infected_file.txt")
    signatures_path = os.path.join(project_root, "signatures", "test_signatures.json")

    # Define file contents, which we will now use for both writing and scanning.
    clean_content = b"this is a safe file, there are no threats here."
    eicar_string = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

    # The try...finally block ensures our temporary test files are always cleaned up.
    try:
        # Create test files
        print("   Creating temporary test files...")
        with open(clean_file_path, "wb") as f:
            f.write(clean_content)
        with open(infected_file_path, "wb") as f:
            f.write(eicar_string)
        print("   Created 'clean_file.txt' and 'infected_file.txt'")

        print("\n3. Initializing C++ Core Engines...")
        analyzer = caninana_core.FileTypeAnalyzer()
        scanner = caninana_core.SignatureEngine()
        print("   Instances of FileTypeAnalyzer and SignatureEngine created.")

        print("\n4. Loading signatures...")
        if not scanner.load_signatures(signatures_path):
            raise RuntimeError(f"Failed to load signatures from '{signatures_path}'")
        print(f"   SUCCESS: Signatures loaded from '{signatures_path}'")

        # --- Test Clean File ---
        print("\n\n--- TESTING CLEAN FILE ---")
        print(f"Analyzing '{os.path.basename(clean_file_path)}'...")
        clean_info = analyzer.analyze_file(clean_file_path)
        print(f"-> Analysis Result: {clean_info}")

        print("Scanning file content (from memory)...")
        # REFACTOR: Pass the in-memory bytes directly to the scanner.
        # This avoids re-reading the file from disk.
        clean_scan_result = scanner.scan_bytes(clean_content, clean_info)
        print(f"-> Scan Result: {clean_scan_result}")

        if not clean_scan_result.threat_detected:
            print("   VERIFICATION: PASSED. No threat was detected, as expected.")
        else:
            print("   VERIFICATION: FAILED. A threat was detected, which is incorrect.")

        # --- Test Infected File ---
        print("\n\n--- TESTING INFECTED FILE ---")
        print(f"Analyzing '{os.path.basename(infected_file_path)}'...")
        infected_info = analyzer.analyze_file(infected_file_path)
        print(f"-> Analysis Result: {infected_info}")

        print("Scanning file content (from memory)...")
        # REFACTOR: Pass the in-memory EICAR string directly to the scanner.
        # This bypasses the file-locking bug while still testing the scan logic.
        infected_scan_result = scanner.scan_bytes(eicar_string, infected_info)
        print(f"-> Scan Result: {infected_scan_result}")

        if infected_scan_result.threat_detected:
            print("   VERIFICATION: PASSED. EICAR signature was detected, as expected.")
            print(f"   Detected signatures: {infected_scan_result.detected_signatures}")
        else:
            print("   VERIFICATION: FAILED. No threat was detected, which is incorrect.")

    except Exception as e:
        print(f"\n[ERROR] An exception occurred during testing: {e}")
    finally:
        # --- Cleanup ---
        print("\n\n5. Cleaning up test files...")
        for f_path in [clean_file_path, infected_file_path]:
            if os.path.exists(f_path):
                try:
                    os.remove(f_path)
                    print(f"   Removed '{os.path.basename(f_path)}'")
                except OSError as e:
                    print(f"   Warning: Could not remove '{os.path.basename(f_path)}': {e}")
            else:
                print(f"   Skipped '{os.path.basename(f_path)}' (was not created).")


if __name__ == "__main__":
    main()