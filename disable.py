import httpx
import xmltodict
import json
import os
import re




def get_ticket():
    request_failed = False
    api_key = os.getenv('SHARED_PANORAMA_API_KEY')
    raw_ticket_number = os.getenv('GP_TICKET').upper()
    first_half_ticket = re.fandall(r"^....", raw_ticket_number)
    back_half_ticket = re.fandall(r"....$", raw_ticket_number)
    ticket_number = f'{first_half_ticket[0]}-{back_half_ticket[0]}'
    duration = os.getenv('DURATION_IN_MINUTES')
    portal_name = os.getenv('portal_name')
    template_name = os.getenv('template_name')
    base_url = os.getenv('BASE_URL')
    ticket_url = f'/api/?type=op&cmd=<request><global-protect-portal><ticket><tpl>{template_name}</tpl><duration>{duration}</duration><portal>{portal_name}</portal><request></request>{ticket_number}</ticket></global-protect-portal></request>&key={api_key}'

    r = httpx.get(f'{base_url}{ticket_url}', verify=False)

    if 'request is invalid' in r.text:
        print(r.text.upper())
        disable_ticket = "Unable to retrieve ticket."
        request_failed = True
    else:
        print(r.text)
        ticket_response = json.loads(json.dumps(xmltodict.parse(r.text)))['response']['result']
        disable_ticket = re.search(r"\S*$", ticket_response).group()
    return disable_ticket, request_failed