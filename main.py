import requests
import asyncio
import sys
import time
import glob
import util as u

LESS_PRINT = False

def run_async(callback):
    def inner(func):
        def wrapper(*args, **kwargs):
            def __exec():
                out = func(*args, **kwargs)
                callback(out)
                return out
            return asyncio.get_event_loop().run_in_executor(None, __exec)
        return wrapper
    return inner


def convert_proxy_format(proxy):
    if "@" in proxy:
        # The proxy is already in the desired format, return as is
        return proxy
    else:
        # Convert the proxy to the desired format
        data = proxy.split(":")
        if len(data) == 4:
            ip, port, username, password = data
            if port == '40000':
                port = '50000'
            return f"{username}:{password}@{ip}:{port}"
    return proxy


def _callback(*args):
    ip = str(args).split("'")[1]
    info = str(args).split("'")[3]
    response = str(args).split("'")[-1].lstrip(',').replace('),)', '').strip()
    resp = ''
    if response != -1:
        resp = f'({response}s)'
    isp, connection = u.get_isp(ip)
    connection = f'-[{connection}]' if 'n/a' not in connection else ''
    if 'Error' not in ip:
        print(f'[{isp}]{resp}{connection} {ip} {info}')
    #print(f'{args} {args[0]}')


def get_proxy_dict(conn):
    return {'https': f'socks5://{conn}', 'http': f'socks5://{conn}'}


@run_async(_callback)
def get(url, data):
    tt = 20
    if LESS_PRINT:
        tt = 3
    try:
        response = requests.get(url, timeout=tt, proxies=get_proxy_dict(data))
        d = response.text, data, round(response.elapsed.total_seconds(), 2)
    except Exception as e:
        d = "Error connecting", data, -1
    return d


def main():
    files = glob.glob('*.txt')
    lst = []
    for fi in files:
        with open(fi) as f:
            lst += f.read().splitlines()
            
    lst = set(lst)
    lst = list(lst)[0:21]
    for l, d in enumerate(lst):
        data = d
        conn2 = convert_proxy_format(data)
        data = conn2
        if len(sys.argv) > 1:
            setting = sys.argv[1]
            if setting == 'd':
                data = d.replace('streaming', 'direct')
            elif setting == 'i':
                data = d.replace('streaming', 'ispstatic')
            elif setting == 'si':
                data = d.replace('streaming', 'skipispstatic')
        get('http://whatismyip.akamai.com', data)


if __name__ == '__main__':
    main()
