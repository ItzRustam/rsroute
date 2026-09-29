# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Combination of `run_server` and `test_server` for automated Docker file. without any network confusing"""

from app.server import create_server
import uvicorn # Run the Server
from dotenv import load_dotenv
import subprocess
import time
import sys
from multiprocessing import Process

load_dotenv()
import os

server = create_server()

def start_server():
    """Target function to launch the FastAPI server."""
    # Force host to 0.0.0.0 inside Docker so it listens on all interfaces,
    # or fallback to your .env configuration safely.
    uvicorn.run(
        server,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )


def run_tests():
    """Function to run the tests."""
    print("\n\nRunning Tests\n\n")

    # CASE A: If you are using a standard test file (e.g., test_server.py)
    import subprocess
    result = subprocess.run(["python", "test_server.py"], capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

    return result.returncode

if __name__ == "__main__":
    # Start the server in a separate background process
    server_process = Process(target=start_server)
    server_process.daemon = True
    server_process.start()
    time.sleep(2)

    # Running Test
    exit_code = 1
    try:
        exit_code = run_tests()
    except Exception as e:
        print(f"Test execution failed: {e}")
    finally:
        # 4. Clean up and terminate the server process safely
        print("Shutting down Server...")
        server_process.terminate()
        server_process.join()

    # Exit with 0 if tests passed, or 1/non-zero if they failed
    sys.exit(exit_code)