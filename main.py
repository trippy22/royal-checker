import requests
import asyncio
import sys
import time
import glob
import util as u

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


def _callback(*args):
    ip = str(args).split("'")[1]
    info = str(args).split("'")[3]
    isp, connection = u.get_isp(ip)
    connection = f'-[{connection}]' if 'n/a' not in connection else ''
    print(f'[{isp}]{connection} {ip} {info}')
    #print(f'{args} {args[0]}')


def get_proxy_dict(conn):
    return {'https': f'socks5://{conn}', 'http': f'socks5://{conn}'}


@run_async(_callback)
def get(url, data):
    try:
        d = requests.get(url, timeout=20, proxies=get_proxy_dict(data)).text, data
    except Exception as e:
        d = "Error connecting", data
    return d


def main():
    files = glob.glob('*.txt')
    lst = []
    for fi in files:
        with open(fi) as f:
            lst += f.read().splitlines()
            
    lst = set(lst)
    for l, d in enumerate(lst):
        data = d
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
