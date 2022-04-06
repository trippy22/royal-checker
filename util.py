import requests
import re

tag = re.compile(r'<[^>]+>')

ISPS = {}

def strip_html(soup):
    stripped = tag.sub('', str(soup))
    return ' '.join(stripped.split())

def get_isp(ip_addr):
    if ip_addr in ISPS:
        return ISPS[ip_addr]
    r = requests.get(f'https://scamalytics.com/ip/{ip_addr}').text
    data = r.split('\n')
    for i, j in enumerate(data):
        if 'ISP Name' in j:
            text = strip_html(data[i+2])
            return text
