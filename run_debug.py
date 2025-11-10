#  run_debug.py — Simple debug helper script

# This file is just for checking if the main pipeline runs fine.
# It imports the main() function from src/run_pipeline.py
# and prints clear messages in the terminal.
# Useful when testing the project before final submission.


import traceback
from pathlib import Path

# Try to import the main() function from our main pipeline file
try:
    from src.run_pipeline import main
    print("Successfully imported run_pipeline.main")
except Exception:
    print("Error: Could not import run_pipeline.main")
    traceback.print_exc()  # shows full error details
    raise SystemExit(1)    # stop execution if import fails

# Run the main() function to see if everything works properly
try:
    main()
    print("run_pipeline.main() executed without errors")
except Exception:
    print("run_pipeline.main() raised an exception while running")
    traceback.print_exc()

# Check if the 'outputs' folder exists and list its files
out = Path("outputs")
if out.exists():
    print("\n Contents of the outputs folder:")
    for p in sorted(out.iterdir()):
        print(" -", p.name, f"({p.stat().st_size} bytes)")
else:
    print("\n Outputs folder not found at:", out.resolve())

# End of file — nothing fancy, just a small test script :)
