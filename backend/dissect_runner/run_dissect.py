# backend/dissect_runner/run_dissect.py
import subprocess
import os
import uuid

def run_dissect(input_path: str, output_dir: str) -> str:
    """
    Runs the r6-dissect tool on the provided input_path, which can be
    either a .rec file or a directory of .rec files, and returns the
    absolute path to the generated JSON file.
    Assumes the r6-dissect binary lives at backend/dissect/r6-dissect.
    """
    # Locate backend root
    base_dir     = os.path.dirname(os.path.abspath(__file__))     # .../backend/dissect_runner
    backend_root = os.path.abspath(os.path.join(base_dir, os.pardir))  # .../backend
    dissect_bin  = os.path.join(backend_root, "dissect", "r6-dissect")

    # Ensure binary exists
    if not os.path.isfile(dissect_bin):
        raise RuntimeError(f"Could not find r6-dissect at {dissect_bin}")

    # Prepare absolute paths
    input_abs  = os.path.abspath(input_path)
    os.makedirs(output_dir, exist_ok=True)
    output_abs = os.path.abspath(output_dir)
    output_file = os.path.join(output_abs, f"{uuid.uuid4().hex}_match.json")

    # Run the dissect command by absolute path
    cmd = [dissect_bin, input_abs, "-o", output_file]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        # Print stderr for debugging
        print(f"[r6-dissect ERROR]\n{result.stderr}")
        raise RuntimeError(f"r6-dissect failed: {result.stderr.strip()}")

    print(f"[r6-dissect] JSON output → {output_file}")
    return output_file
