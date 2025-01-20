# setup_integrate_repos.py
"""
Integration script for cloning and setting up repositories.
Automates repository cloning, dependency installation, and linking to Django.
"""

import os
import subprocess

# Define repositories and integration paths
REPOSITORIES = {
    "Peek-a-Walk": "https://github.com/FPSG-UIUC/Peek-a-Walk.git",
    "Augury": "https://github.com/FPSG-UIUC/augury.git",
    "Loader": "https://github.com/palera1n/loader.git",
    "Palera1n": "https://github.com/palera1n/palera1n.git",
    "SSH Ramdisk Tool": "https://github.com/TechC0xy/SSH-Ramdisk-Tool-Activation-IOS.git",
    "FutureRestore-GUI": "https://github.com/CoocooFroggy/FutureRestore-GUI.git",
    "FutureRestore": "https://github.com/futurerestore/futurerestore.git",
    "Meltdown-Spectre": "https://github.com/kianenigma/meltdown-spectre.git",
    "Inspectre-Gadget": "https://github.com/vusec/inspectre-gadget.git",
    "Checkm8 GUI": "https://github.com/TarballCoLtd/checkm8gui.git",
    "iDict": "https://github.com/Pr0x13/iDict.git",
    "iBrutr": "https://github.com/Pr0x13/iBrutr.git",
    "Pushy": "https://github.com/jchambers/pushy.git",
    "IAIK Meltdown": "https://github.com/IAIK/meltdown.git",
    "Bootstrap-Stable": "https://github.com/DsSoft-Byte/Bootstrap-Stable.git",
}

BASE_PATH = "./repos"


def clone_repositories():
    """
    Clones each repository into the base path.
    """
    os.makedirs(BASE_PATH, exist_ok=True)
    for name, repo_url in REPOSITORIES.items():
        repo_path = os.path.join(BASE_PATH, name)
        if not os.path.exists(repo_path):
            try:
                subprocess.run(["git", "clone", repo_url, repo_path], check=True)
                print(f"Cloned {name} successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to clone {name}. Check the repository URL or your internet connection.")
        else:
            print(f"{name} already cloned.")


def setup_dependencies():
    """
    Installs dependencies for the cloned repositories if they exist.
    """
    for name in REPOSITORIES.keys():
        repo_path = os.path.join(BASE_PATH, name)
        requirements_file = os.path.join(repo_path, "requirements.txt")
        if os.path.exists(requirements_file):
            try:
                subprocess.run(["pip", "install", "-r", requirements_file], check=True, cwd=repo_path)
                print(f"Installed dependencies for {name}.")
            except subprocess.CalledProcessError:
                print(f"Failed to install dependencies for {name}.")


def integrate_with_django():
    """
    Links cloned repositories into the Django project.
    """
    django_app_path = "./apple_integration_project/apple_framework_integration/external_tools"
    os.makedirs(django_app_path, exist_ok=True)

    for name in REPOSITORIES.keys():
        source_path = os.path.join(BASE_PATH, name)
        dest_path = os.path.join(django_app_path, name)
        if not os.path.exists(dest_path):
            try:
                os.symlink(source_path, dest_path)
                print(f"Linked {name} into Django app.")
            except OSError:
                print(f"Failed to link {name}. Check permissions.")


if __name__ == "__main__":
    print("Starting repository integration process...")
    clone_repositories()
    setup_dependencies()
    integrate_with_django()
    print("Integration complete. Repositories linked to the Django project.")
