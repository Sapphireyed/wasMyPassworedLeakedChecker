import requests
import hashlib
import sys

def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error: {res.status_code}')

    return res

def get_leaks_count(response, tail):
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == tail:
            return count
    return 0

def pwned_api_check(password):
    psw_hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = psw_hashed[:5], psw_hashed[5:]
    res = request_api_data(first5)
    print(res)
    return get_leaks_count(res, tail)

def main(args):
   for psw in args:
       count = pwned_api_check(psw)
       print(count)
       if count:
           print(f'{psw} found {count} times')
       else:
           print(f'{psw} not found')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))