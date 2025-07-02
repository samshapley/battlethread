#!/usr/bin/env python3
"""
Simple web server for BattleThread timeline application.
Serves static files and runs on port 8080.
"""

import http.server
import socketserver
import os
import threading
import time

PORT = 8080

class BattleThreadHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve from battlethread directory."""
    
    def __init__(self, *args, **kwargs):
        # Change to battlethread directory
        super().__init__(*args, directory="battlethread", **kwargs)
    
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        # Prevent caching during development
        if self.path.endswith(('.js', '.css')):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        else:
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom logging format
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server():
    """Run the web server."""
    with socketserver.TCPServer(("", PORT), BattleThreadHandler) as httpd:
        print(f"BattleThread Timeline Server")
        print(f"=" * 40)
        print(f"Server running on port {PORT}")
        print(f"Local URL: http://localhost:{PORT}")
        print(f"Public URL will be displayed when accessed")
        print(f"=" * 40)
        print(f"Press Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    # First, ensure we have sample data
    if not os.path.exists("battlethread/data/battles_timeline.json"):
        print("Creating sample data...")
        import subprocess
        subprocess.run(["python", "battlethread/create_sample_data.py"])
    
    # Run the server
    run_server()