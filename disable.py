import os
import re
import json
import httpx
import xmltodict

def get_ticket():
    """
    Function to retrieve a ticket from a remote server using an API key. 

    Environment variables:
    PANORAMA_API_KEY : str : the API key for accessing the server
    GP_REQUEST : str : the raw ticket number
    DURATION_IN_MINUTES : str : the requested duration for the ticket 
    PORTAL_NAME : str : the name of the portal to access
    TEMPLATE_NAME : str : the template name for the request
    BASE_URL : str : the base URL for the API server

    Returns:
    disable_ticket : str : the retrieved ticket or an error message
    request_failed : bool : a flag indicating whether the request failed
    """
    print("starting")
    api_key = os.getenv('PANOS_API_KEY')
    raw_ticket_number = os.getenv('GP_REQUEST').upper()

    first_half_ticket = re.findall(r"^....", raw_ticket_number)
    back_half_ticket = re.findall(r"....$", raw_ticket_number)
    
    ticket_number = f'{first_half_ticket[0]}-{back_half_ticket[0]}'
    duration = os.getenv('DURATION_IN_MINUTES')
    portal_name = os.getenv('PORTAL_NAME')
    template_name = os.getenv('TEMPLATE_NAME')
    base_url = os.getenv('BASE_URL')
    
    ticket_url = (
        f"/api/?type=op&cmd=<request><global-protect-portal>"
        f"<ticket><tpl>{template_name}</tpl><duration>{duration}</duration>"
        f"<portal>{portal_name}</portal><request>{ticket_number}</request>"
        f"</ticket></global-protect-portal></request>&key={api_key}"
    )

    print(f'{base_url}{ticket_url}')

    # Note: Suppressing SSL warnings can be dangerous. Consider providing a path to a cert file.
    # httpx.TimeoutConfig(connect_timeout=5, read_timeout=None, write_timeout=5)
    r = httpx.get(f'{base_url}{ticket_url}', verify=False, timeout=None)

    if 'request is invalid' in r.text:
        disable_ticket = "Unable to retrieve ticket."
        request_failed = True
    else:
        ticket_response = json.loads(json.dumps(xmltodict.parse(r.text)))['response']['result']
        disable_ticket = re.search(r"\S*$", ticket_response).group()
        request_failed = False

    return disable_ticket, request_failed

if __name__ == "__main__":
    get_ticket()
