# cve_extractor.py
"""
Clone the apple-cve repository and extract details for integration.
"""
import os
import subprocess
from pathlib import Path
from apple_framework_integration.models import CVE

REPO_URL = "https://github.com/Proteas/apple-cve.git"
BASE_PATH = "/mnt/data/repos"
import sys



def clone_repository():
    """
    Clones the apple-cve repository if not already cloned.
    """
    if not os.path.exists(REPO_PATH):
        try:
            subprocess.run(["git", "clone", REPO_URL, REPO_PATH], check=True)
            print("Repository cloned successfully.")
        except subprocess.CalledProcessError:
            print("Failed to clone the repository. Check your internet connection.")
    else:
        print("Repository already exists.")


def extract_cve_details():
    """
    Extracts CVE details from the repository and populates the database.
    """
    cve_files = list(Path(REPO_PATH).rglob("*.py"))  # Assuming CVEs are Python scripts
    for file_path in cve_files:
        cve_id = file_path.stem.upper()
        description = f"Exploit script for {cve_id}"
        try:
            CVE.objects.get_or_create(
                cve_id=cve_id,
                description=description,
                exploit_path=str(file_path),
            )
            print(f"Added {cve_id} to the database.")
        except Exception as e:
            print(f"Error adding {cve_id}: {e}")


if __name__ == "__main__":
    clone_repository()
    extract_cve_details()
    print("CVE details extracted and stored in the database.")
