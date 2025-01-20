# cve_scraper.py
"""
Scrapes CVE details from Stack Watch for Apple products and stores them in the database.
"""

import requests
from bs4 import BeautifulSoup
from apple_framework_integration.models import CVE

STACKWATCH_URL = "https://stack.watch/product/apple/"

def fetch_cves():
    """
    Scrapes CVE data from Stack Watch and stores it in the database.
    """
    response = requests.get(STACKWATCH_URL)
    if response.status_code != 200:
        print("Failed to fetch CVE data.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    cve_list = soup.find_all('a', href=True, text=True)

    for link in cve_list:
        if link.text.startswith("CVE"):
            cve_id = link.text.strip()
            description = f"Details for {cve_id}"  # You can enhance this with more specific parsing
            try:
                CVE.objects.get_or_create(
                    cve_id=cve_id,
                    description=description,
                    exploit_path=None,  # Since exploits are not provided, leave empty
                )
                print(f"Added {cve_id} to the database.")
            except Exception as e:
                print(f"Error adding {cve_id}: {e}")

if __name__ == "__main__":
    fetch_cves()
