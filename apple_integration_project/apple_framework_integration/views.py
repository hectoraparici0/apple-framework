"""Views for the app."""
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import CVE

def cve_list(request):
    search_query = request.GET.get('search', '')
    cves = CVE.objects.filter(cve_id__icontains=search_query)
    return render(request, 'cve_list.html', {'cves': cves, 'search_query': search_query})

def cve_detail(request, cve_id):
    cve = get_object_or_404(CVE, cve_id=cve_id)
    return render(request, 'cve_detail.html', {'cve': cve})

def update_cves(request):
    # Call the scraper script to fetch and update CVEs
    from cve_scraper import fetch_cves
    fetch_cves()
    return render(request, 'update_success.html')
