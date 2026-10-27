# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Combination of `run_server` and `test_server` for automated Docker file without any network confusion"""

from app.server import create_server
import uvicorn  # Run the Server
from dotenv import load_dotenv
import subprocess
import time
import sys
import urllib.request
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


def wait_for_server(timeout: int = 15) -> bool:
    """Poll until the server is ready to accept connections."""
    host = os.getenv("HOST", "127.0.0.1")
    if host == "0.0.0.0":
        host = "127.0.0.1"
    port = os.getenv("PORT", "8000")
    url = f"http://{host}:{port}/"

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def run_tests():
    """Function to run the tests."""
    print("\n\nRunning Tests\n\n")

    result = subprocess.run([sys.executable, "test_server.py"], capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode


if __name__ == "__main__":
    # Start the server in a separate background process
    server_process = Process(target=start_server)
    server_process.daemon = True
    server_process.start()

    # Wait for the server to be ready before firing tests
    server_ready = wait_for_server(timeout=15)
    if not server_ready:
        print("Warning: Server health check timed out, attempting tests anyway...")

    # Running Test
    exit_code = 1
    try:
        exit_code = run_tests()
    except Exception as e:
        print(f"Test execution failed: {e}")
    finally:
        # Clean up and terminate the server process safely
        print("Shutting down Server...")
        server_process.terminate()
        server_process.join()

    # Exit with 0 if tests passed, or non-zero if they failed
    sys.exit(exit_code)
