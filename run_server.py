# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

"""Run RSRoute Server"""

from app.server import create_server
import uvicorn # Run the Server

server = create_server()

if __name__ == "__main__":
    uvicorn.run(
        server,
        host="0.0.0.0",
        port=8000
    )    

