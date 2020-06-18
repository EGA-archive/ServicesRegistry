import requests
import json


def explore_service(service):
    """Fetch the interesting information of a service
    by using its base URL"""
    service_dict = {}

    # Use the name and address keys of the service input dictionary
    service_dict["title"] = service["name"]
    service_url = service["address"]

    # Fetch the info page of the service
    service_info_page = requests.get(service_url)
    if service_info_page:
        service_dict["error"] = False
        service_info_dict = json.loads(service_info_page.content)

        service_dict["organization_name"] = service_info_dict["organization"]["name"]
        service_dict["name"] = service_info_dict["name"]
        service_dict["description"] = service_info_dict["description"]
        service_dict["visit_us"] = service_info_dict["organization"]["welcomeUrl"]
        service_dict["beacon_api"] = service_info_dict["serviceUrl"]
        service_dict["contact_us"] = service_info_dict["organization"]["contactUrl"]

        # For the logo, we need to check if the link is OK
        logo_url = service_info_dict["organization"]["logoUrl"]
        if logo_url.startswith("http"):
            try:
                logo_request = requests.get(logo_url)
                if logo_request:
                    service_dict["logo_url"] = logo_url
                else:
                    service_dict["logo_url"] = False
            except (requests.exceptions.InvalidURL, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
                service_dict["logo_url"] = False
        else:
            service_dict["logo_url"] = False
    else:
        service_dict["error"] = True

    return service_dict


def get_service_registry_context(serviceRegistryUrl):
    """Get the service registry information and ping all the
    registered services to get the necessary info for the UI."""

    context = {}

    # service_registry = requests.get(serviceRegistryUrl)
    service_registry = {
        "eu.crg.covid19beacon": {
            "name": "Covid Beacon",
            "address": "https://covid19beacon.crg.eu/api/"
            },
        "ca.distributedgenomics.poc": {
            "name": "CANDIG",
            "address": "https://poc.distributedgenomics.ca:5050"
            },
        "h3abionet.org": {
            "name": "H3Africa",
            "address": "https://beacon2.h3abionet.org/api"
            }
        }
    
    registries_list = []

    for value in service_registry.values():
        registries_list.append(explore_service(value))

    context["registries"] = registries_list

    return context