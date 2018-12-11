import http.cookiejar
from urllib import request, parse, error
from time import sleep
from modules.strlib import *

COOKIE = http.cookiejar.CookieJar()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.'
                  '0.1 Safari/605.1.15',
    'Connection': 'keep-alive'}


def get_referer(url):
    loading_ui()
    ref_req = request.Request(url)
    ref_content = request.urlopen(ref_req).read().decode('utf-8')

    ref_pat_head = re.compile("Login.submitLoginRequest\(\);\" action=\"")
    ref_pat_tail = re.compile("\" >")
    ref_mid = get_pat(ref_pat_head, ref_pat_tail, ref_content)
    print('  Done')
    return 'https://sts.sydney.edu.au' + ref_mid


def get_page(url, headers=HEADERS, data=0, login_check=0, prompt='Loading'):
    global COOKIE
    loading_ui(prompt)
    if data:
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, headers=headers, data=data)
    else:
        req = request.Request(url, headers=headers)

    opener = request.build_opener(request.HTTPCookieProcessor(COOKIE))
    page = opener.open(req)
    print('  Done')
    try:
        if login_check:
            return page.read().decode('utf-8'), page.headers.__getitem__('x-frame-options')
        else:
            return page.read().decode('utf-8')
    except error.HTTPError as e:
        print('Unable to communicate with remote server')
        print(e)
        print('Try again later')
        exit(0)


def loading_ui(prompt='Loading'):
    print('⏳ ' + prompt + '\t', end='')
    for i in range(0, 50):
        if i < 5:
            print('▉', end='')
            sleep(0.1)
        elif i < 35:
            print('▉', end='')
            sleep(0.05)
        else:
            print('▉', end='')
            sleep(0.08)
