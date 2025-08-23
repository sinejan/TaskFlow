#!/usr/bin/env python3
"""
TaskFlow - Unified Launcher
Starts both backend and frontend servers
"""

import os
import sys
import time
import signal
import subprocess
import threading
import webbrowser
from pathlib import Path

class TaskFlowLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def start_backend(self):
        """Start the Flask backend server"""
        print("🚀 Starting backend server...")
        try:
            # Change to backend directory and start the Flask app
            backend_path = Path(__file__).parent / "backend"
            self.backend_process = subprocess.Popen(
                [sys.executable, "app.py"],
                cwd=backend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Backend server started on http://localhost:5000")
            return True
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start a simple HTTP server for frontend"""
        print("🌐 Starting frontend server...")
        try:
            # Start a simple HTTP server in the frontend directory
            frontend_path = Path(__file__).parent / "frontend"
            self.frontend_process = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8080"],
                cwd=frontend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Frontend server started on http://localhost:8080")
            return True
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False

    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        import requests

        print("⏳ Waiting for backend to be ready...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:5000", timeout=1)
                if response.status_code == 200:
                    print("✅ Backend is ready!")
                    return True
            except:
                pass
            time.sleep(1)

        print("❌ Backend failed to start within timeout")
        return False

    def open_browser(self):
        """Open the TaskFlow application in the default browser"""
        print("🌐 Opening TaskFlow in your browser...")
        try:
            webbrowser.open("http://localhost:8080/landing/html/index.html")
            print("✅ TaskFlow opened in browser")
        except Exception as e:
            print(f"❌ Failed to open browser: {e}")
            print("📝 Please manually open: http://localhost:8080/landing/html/index.html")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down TaskFlow...")
        self.running = False
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            print("🔄 Stopping backend server...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()

        if self.frontend_process:
            print("🔄 Stopping frontend server...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()

        print("✅ TaskFlow stopped successfully")

    def monitor_processes(self):
        """Monitor backend and frontend processes"""
        while self.running:
            if self.backend_process and self.backend_process.poll() is not None:
                print("❌ Backend process died unexpectedly")
                break

            if self.frontend_process and self.frontend_process.poll() is not None:
                print("❌ Frontend process died unexpectedly")
                break

            time.sleep(1)

    def run(self):
        """Main run method"""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        print("=" * 50)
        print("🎯 TaskFlow - Modern Task Management")
        print("=" * 50)

        # Start backend
        if not self.start_backend():
            return False

        # Wait for backend to be ready
        if not self.wait_for_backend():
            self.cleanup()
            return False

        # Start frontend
        if not self.start_frontend():
            self.cleanup()
            return False

        # Give frontend a moment to start
        time.sleep(2)

        # Open browser
        self.open_browser()

        print("\n" + "=" * 50)
        print("🎉 TaskFlow is now running!")
        print("📱 Frontend: http://localhost:8080/landing/html/index.html")
        print("🔧 Backend API: http://localhost:5000")
        print("⌨️  Press Ctrl+C to stop")
        print("=" * 50)

        # Monitor processes
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

        return True

def main():
    """Main entry point"""
    launcher = TaskFlowLauncher()
    success = launcher.run()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
