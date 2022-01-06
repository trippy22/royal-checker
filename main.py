import requests
import asyncio
import sys

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
    print(f'{args}')


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
    with open('Proxy_list.txt') as f:
        lst = f.read().splitlines()
        
    for l, d in enumerate(lst):
        data = d
        if len(sys.argv) > 1:
            data = d.replace('streaming', 'direct')
        get('http://whatismyip.akamai.com', data)


if __name__ == '__main__':
    main()
