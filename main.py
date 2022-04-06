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
    print(f'[{u.get_isp(ip)}] {ip} {info}')
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
            data = d.replace('streaming', 'direct')
        get('http://whatismyip.akamai.com', data)


if __name__ == '__main__':
    main()
