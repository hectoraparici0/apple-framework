import os
import subprocess
import json
import sys

# Paths
QUANTUM_PATH = "/Users/aet/Documents/GitHub/aetsystem/src/lib/quantum"
FRAMEWORK_PATH = "/Users/aet/Desktop/apple framework"
DEPLOY_SCRIPT = os.path.join(FRAMEWORK_PATH, "deploymac.sh")
NPM_LOG_FILE = "/Users/aet/.npm/_logs/latest.log"

def create_package_json():
    """
    Ensure the quantum-core directory has a valid package.json file.
    """
    print("[INFO] Checking and creating package.json for quantum-core...")
    package_json_path = os.path.join(QUANTUM_PATH, "package.json")
    
    if not os.path.exists(package_json_path):
        package_data = {
            "name": "quantum-core",
            "version": "1.0.0",
            "main": "core.sh",
            "scripts": {
                "start": "bash core.sh"
            },
            "license": "ISC"
        }
        with open(package_json_path, "w") as f:
            json.dump(package_data, f, indent=2)
        print("[INFO] Created package.json for quantum-core.")
    else:
        print("[INFO] package.json for quantum-core already exists.")

def update_framework_dependencies():
    """
    Update the apple-framework project to reference the quantum-core package.
    """
    print("[INFO] Updating apple-framework dependencies...")
    package_json_path = os.path.join(FRAMEWORK_PATH, "package.json")

    try:
        with open(package_json_path, "r") as f:
            package_data = json.load(f)

        # Update dependencies
        package_data.setdefault("dependencies", {})
        package_data["dependencies"]["quantum-core"] = f"file:{QUANTUM_PATH}"

        with open(package_json_path, "w") as f:
            json.dump(package_data, f, indent=2)

        print("[INFO] Updated dependencies in apple-framework package.json.")
    except Exception as e:
        print(f"[ERROR] Failed to update dependencies: {e}")
        sys.exit(1)

def install_dependencies():
    """
    Install dependencies for the apple-framework project.
    """
    print("[INFO] Installing npm dependencies for apple-framework...")
    try:
        subprocess.run(["npm", "install"], cwd=FRAMEWORK_PATH, check=True)
        print("[INFO] Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Dependency installation failed.")
        print(f"[INFO] Check the npm logs at: {NPM_LOG_FILE}")
        sys.exit(1)

def run_deploy_script():
    """
    Run the deploymac.sh script to build and deploy the application.
    """
    print("[INFO] Running deploy script...")
    try:
        subprocess.run([DEPLOY_SCRIPT], cwd=FRAMEWORK_PATH, check=True)
        print("[INFO] Deployment completed successfully.")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Deploy script failed.")
        sys.exit(1)

def validate_paths():
    """
    Validate the required paths and files.
    """
    print("[INFO] Validating paths...")
    if not os.path.exists(QUANTUM_PATH):
        print(f"[ERROR] Quantum path does not exist: {QUANTUM_PATH}")
        sys.exit(1)
    if not os.path.exists(FRAMEWORK_PATH):
        print(f"[ERROR] Framework path does not exist: {FRAMEWORK_PATH}")
        sys.exit(1)
    if not os.path.exists(DEPLOY_SCRIPT):
        print(f"[ERROR] Deploy script does not exist: {DEPLOY_SCRIPT}")
        sys.exit(1)
    print("[INFO] All paths validated successfully.")

def main():
    """
    Main function to automate the fix and deploy process with error handling.
    """
    print("[INFO] Starting fix and deploy automation...")

    # Step 1: Validate paths
    validate_paths()

    # Step 2: Create package.json for quantum-core
    create_package_json()

    # Step 3: Update dependencies in apple-framework
    update_framework_dependencies()

    # Step 4: Install dependencies
    install_dependencies()

    # Step 5: Run deploy script
    run_deploy_script()

    print("[INFO] Fix and deploy process completed successfully.")

if __name__ == "__main__":
    main()
