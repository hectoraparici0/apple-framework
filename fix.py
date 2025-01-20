import os
import subprocess
import json

# Paths
QUANTUM_PATH = "/Users/aet/Documents/GitHub/aetsystem/src/lib/quantum"
FRAMEWORK_PATH = "/Users/aet/Desktop/apple_framework"
DEPLOY_SCRIPT = os.path.join(FRAMEWORK_PATH, "deploymac.sh")

def create_package_json():
    """ Create a package.json for the quantum-core directory."""
    print("Creating package.json for quantum-core...")
    package_json_path = os.path.join(QUANTUM_PATH, "package.json")
    
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
    
    print(f"Created package.json at {package_json_path}")


def update_framework_dependencies():
    """
    Update the apple-framework project to reference the quantum-core package.
    """
    print("Updating apple-framework dependencies...")
    package_json_path = os.path.join(FRAMEWORK_PATH, "package.json")

    # Load the existing package.json
    with open(package_json_path, "r") as f:
        package_data = json.load(f)

    # Update dependencies to reference quantum-core
    package_data.setdefault("dependencies", {})
    package_data["dependencies"]["quantum-core"] = f"file:{QUANTUM_PATH}"

    # Save the updated package.json
    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)
    
    print(f"Updated dependencies in {package_json_path}")


def install_dependencies():
    """
    Install dependencies for the apple-framework project.
    """
    print("Installing dependencies for apple-framework...")
    try:
        subprocess.run(["npm", "install"], cwd=FRAMEWORK_PATH, check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error installing dependencies:")
        print(e)
        exit(1)


def run_deploy_script():
    """
    Run the deploy script to deploy the application.
    """
    print("Running deploy script...")
    try:
        subprocess.run([DEPLOY_SCRIPT], cwd=FRAMEWORK_PATH, check=True)
        print("Deployment completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error running deploy script:")
        print(e)
        exit(1)


def main():
    """
    Main function to automate the fix and deployment process.
    """
    print("Starting fix and deploy automation...")

    # Step 1: Create package.json for quantum-core
    if not os.path.exists(os.path.join(QUANTUM_PATH, "package.json")):
        create_package_json()
    else:
        print("package.json for quantum-core already exists.")

    # Step 2: Update apple-framework dependencies
    update_framework_dependencies()

    # Step 3: Install dependencies
    install_dependencies()

    # Step 4: Run the deploy script
    run_deploy_script()

    print("Fix and deploy process completed successfully.")


if __name__ == "__main__":
    main()
