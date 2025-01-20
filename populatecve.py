# populate_cve.py
import os
from apple_framework_integration.models import CVE

REPO_PATH = "/mnt/data/repos/apple-cve"

def populate_cve_database():
    for root, dirs, files in os.walk(REPO_PATH):
        for file in files:
            if file.endswith(".py"):  # Assuming CVE exploits are Python scripts
                cve_id = file.replace(".py", "").upper()
                description = f"Exploit for {cve_id}"
                exploit_path = os.path.join(root, file)
                CVE.objects.get_or_create(
                    cve_id=cve_id,
                    description=description,
                    exploit_path=exploit_path,
                )
    print("CVE database populated successfully.")
