#!/usr/bin/env python3
"""
Cross-Platform Compatibility Test Script
========================================

This script tests the Jenkins setup across different platforms to ensure
it works seamlessly on Windows, macOS, Linux, and cloud VMs.
"""

import platform
import sys
import subprocess
import os
import time
from pathlib import Path

class CrossPlatformTester:
    """Test cross-platform compatibility of Jenkins setup."""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_mac = self.platform == 'darwin'
        self.is_linux = self.platform == 'linux'
        self.workspace_path = Path(__file__).parent.absolute()
        
    def print_header(self, message):
        """Print a header message."""
        print(f"\n{'='*60}")
        print(f"🧪 {message}")
        print(f"{'='*60}")
        
    def print_test(self, test_name, status, details=""):
        """Print test result."""
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {test_name}")
        if details:
            print(f"   {details}")
    
    def run_command(self, cmd, capture_output=True, timeout=30):
        """Run a command with error handling."""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=capture_output, 
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout.strip() if capture_output else ""
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def test_platform_detection(self):
        """Test platform detection."""
        self.print_header("Platform Detection Test")
        
        self.print_test(
            "Platform Detection",
            True,
            f"Detected: {self.platform} ({platform.release()})"
        )
        
        self.print_test(
            "Architecture Detection",
            True,
            f"Architecture: {platform.machine()}"
        )
        
        self.print_test(
            "Python Version",
            True,
            f"Python: {sys.version.split()[0]}"
        )
        
        return True
    
    def test_python_commands(self):
        """Test Python command availability."""
        self.print_header("Python Command Availability Test")
        
        python_commands = ['python3', 'python']
        pip_commands = ['pip3', 'pip']
        
        python_available = False
        pip_available = False
        
        for cmd in python_commands:
            success, output = self.run_command(f"{cmd} --version")
            if success:
                self.print_test(f"{cmd} command", True, output)
                python_available = True
                break
            else:
                self.print_test(f"{cmd} command", False, "Not available")
        
        for cmd in pip_commands:
            success, output = self.run_command(f"{cmd} --version")
            if success:
                self.print_test(f"{cmd} command", True, output)
                pip_available = True
                break
            else:
                self.print_test(f"{cmd} command", False, "Not available")
        
        # Test python -m pip as fallback
        if not pip_available and python_available:
            python_cmd = 'python3' if self.run_command("python3 --version")[0] else 'python'
            success, output = self.run_command(f"{python_cmd} -m pip --version")
            self.print_test(f"{python_cmd} -m pip", success, output if success else "Not available")
            pip_available = success
        
        return python_available and pip_available
    
    def test_docker_commands(self):
        """Test Docker command availability."""
        self.print_header("Docker Command Availability Test")
        
        docker_available = False
        docker_running = False
        
        # Test docker command
        success, output = self.run_command("docker --version")
        if success:
            self.print_test("Docker command", True, output)
            docker_available = True
        else:
            self.print_test("Docker command", False, "Not available")
            return False
        
        # Test docker info
        success, output = self.run_command("docker info")
        if success:
            self.print_test("Docker daemon", True, "Running")
            docker_running = True
        else:
            self.print_test("Docker daemon", False, "Not running")
        
        # Test docker compose
        compose_available = False
        for cmd in ["docker compose version", "docker-compose --version"]:
            success, output = self.run_command(cmd)
            if success:
                self.print_test("Docker Compose", True, output)
                compose_available = True
                break
        
        if not compose_available:
            self.print_test("Docker Compose", False, "Not available (optional)")
        
        return docker_available and docker_running
    
    def test_path_handling(self):
        """Test path handling across platforms."""
        self.print_header("Path Handling Test")
        
        # Test workspace path
        self.print_test(
            "Workspace Path",
            True,
            f"Path: {self.workspace_path}"
        )
        
        # Test Windows path conversion
        if self.is_windows:
            workspace_mount = str(self.workspace_path)
            workspace_mount = workspace_mount.replace('\\', '/')
            if len(workspace_mount) > 1 and workspace_mount[1] == ':':
                workspace_mount = f"/{workspace_mount[0].lower()}{workspace_mount[2:]}"
            self.print_test(
                "Windows Path Conversion",
                True,
                f"Converted: {workspace_mount}"
            )
        else:
            self.print_test(
                "Unix Path Handling",
                True,
                f"Path: {self.workspace_path}"
            )
        
        # Test file operations
        test_file = self.workspace_path / "test_cross_platform.txt"
        try:
            with open(test_file, 'w') as f:
                f.write("Cross-platform test file")
            
            if test_file.exists():
                self.print_test("File Creation", True, "Success")
                test_file.unlink()  # Clean up
            else:
                self.print_test("File Creation", False, "Failed")
        except Exception as e:
            self.print_test("File Creation", False, str(e))
        
        return True
    
    def test_docker_socket_permissions(self):
        """Test Docker socket permissions."""
        self.print_header("Docker Socket Permissions Test")
        
        if self.is_windows:
            self.print_test("Docker Socket", True, "Windows - using named pipes")
            return True
        
        # Check if Docker socket exists
        socket_path = "/var/run/docker.sock"
        if os.path.exists(socket_path):
            self.print_test("Docker Socket Exists", True, f"Path: {socket_path}")
            
            # Check permissions
            try:
                stat_info = os.stat(socket_path)
                permissions = oct(stat_info.st_mode)[-3:]
                self.print_test("Socket Permissions", True, f"Permissions: {permissions}")
            except Exception as e:
                self.print_test("Socket Permissions", False, str(e))
        else:
            self.print_test("Docker Socket", False, "Socket not found")
            return False
        
        return True
    
    def test_jenkins_setup_script(self):
        """Test Jenkins setup script syntax and imports."""
        self.print_header("Jenkins Setup Script Test")
        
        setup_script = self.workspace_path / "jenkins-setup.py"
        
        if not setup_script.exists():
            self.print_test("Setup Script", False, "jenkins-setup.py not found")
            return False
        
        # Test Python syntax
        success, output = self.run_command(f"python3 -m py_compile {setup_script}")
        self.print_test("Python Syntax", success, output if not success else "Valid")
        
        # Test imports
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("jenkins_setup", setup_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.print_test("Module Imports", True, "All imports successful")
        except Exception as e:
            self.print_test("Module Imports", False, str(e))
            return False
        
        return True
    
    def test_workshop_scenarios(self):
        """Test workshop scenario files."""
        self.print_header("Workshop Scenarios Test")
        
        scenarios_dir = self.workspace_path / "jenkins-scenarios"
        if not scenarios_dir.exists():
            self.print_test("Scenarios Directory", False, "jenkins-scenarios not found")
            return False
        
        scenarios = list(scenarios_dir.glob("scenario_*"))
        self.print_test(
            "Scenarios Found",
            len(scenarios) > 0,
            f"Found {len(scenarios)} scenarios"
        )
        
        # Test each scenario
        for scenario in scenarios:
            jenkinsfile = scenario / "Jenkinsfile"
            requirements = scenario / "requirements.txt"
            
            self.print_test(
                f"Scenario {scenario.name}",
                jenkinsfile.exists() and requirements.exists(),
                f"Jenkinsfile: {'✅' if jenkinsfile.exists() else '❌'}, Requirements: {'✅' if requirements.exists() else '❌'}"
            )
        
        return True
    
    def run_all_tests(self):
        """Run all compatibility tests."""
        self.print_header("CROSS-PLATFORM COMPATIBILITY TEST SUITE")
        print(f"Platform: {self.platform} ({platform.release()})")
        print(f"Architecture: {platform.machine()}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Workspace: {self.workspace_path}")
        
        tests = [
            ("Platform Detection", self.test_platform_detection),
            ("Python Commands", self.test_python_commands),
            ("Docker Commands", self.test_docker_commands),
            ("Path Handling", self.test_path_handling),
            ("Docker Socket", self.test_docker_socket_permissions),
            ("Setup Script", self.test_jenkins_setup_script),
            ("Workshop Scenarios", self.test_workshop_scenarios),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} - ERROR: {e}")
                results.append((test_name, False))
        
        # Summary
        self.print_header("TEST SUMMARY")
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your setup is cross-platform compatible.")
            return True
        else:
            print("⚠️  Some tests failed. Please check the issues above.")
            return False

def main():
    """Main entry point."""
    tester = CrossPlatformTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
