import requests
import bs4
from lxml.etree import parse
from lxml import html
import js2py
import re
import hashlib



def save_facebook_video(face_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
    }
    
    url = "https://getmyfb.com/process"
    response = requests.post(url, data={"id": face_url,"locale": "es"}, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    elem = soup.find("a", {"class": "hd-button"})
    if not elem:
        elem = soup.find("a", {"class": "ig-button"})
    url = elem.attrs.get("href")
    if url is None:
        raise ValueError("url not found")
    video_response = requests.get(url, headers=headers)
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    with open("{}.mp4".format(name), "wb") as f:
        f.write(video_response.content)

    return "{}.mp4".format(name)


def save_video_tiktok(video_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
    }
    main_url = "https://tiktokio.com/#google_vignette"
    response = requests.get(main_url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    prefix = soup.find('input', {"name": "prefix"}).get("value")
    url = "https://tiktokio.com/api/v1/tk-htmx"
    response = requests.post(url, data={"prefix": prefix,"vid": video_url}, headers=headers)
    root = html.fromstring(response.content)
    tree = root.getroottree()
    real_url = tree.xpath("/html/div/div[1]/div/a")[0].get("href")
    video_response = requests.get(real_url, headers=headers)
    name = hashlib.md5(real_url.encode('utf-8')).hexdigest()
    with open("{}.mp4".format(name), "wb") as f:
        f.write(video_response.content)

    return "{}.mp4".format(name)



def save_video_instagram(video_url):
    val ='''
    var _0xc0e = [
    "",
    "split",
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/",
    "slice",
    "indexOf",
    "",
    "",
    ".",
    "pow",
    "reduce",
    "reverse",
    "0",
    ];
    function _0xe0c(d, e, f) {
    var g = _0xc0e[2][_0xc0e[1]](_0xc0e[0]);
    var h = g[_0xc0e[3]](0, e);
    var i = g[_0xc0e[3]](0, f);
    var j = d[_0xc0e[1]](_0xc0e[0])
        [_0xc0e[10]]()
        [_0xc0e[9]](function (a, b, c) {
        if (h[_0xc0e[4]](b) !== -1)
            return (a += h[_0xc0e[4]](b) * Math[_0xc0e[8]](e, c));
        }, 0);
    var k = _0xc0e[0];
    while (j > 0) {
        k = i[j % f] + k;
        j = (j - (j % f)) / f;
    }
    return k || _0xc0e[11];
    }
    function unitary (h, u, n, t, e, r) {
        r = "";
        for (var i = 0, len = h.length; i < len; i++) {
        var s = "";
        while (h[i] !== n[e]) {
            s += h[i];
            i++;
        }
        for (var j = 0; j < n.length; j++)
            s = s.replace(new RegExp(n[j], "g"), j);
        r += String.fromCharCode(_0xe0c(s, e, 10) - t);
        }
        return decodeURIComponent(r);
    }
    unitary('''
    headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
        }
    payload = {
        "q": video_url,
        "t": "media",
        "lang": "es",
        "v": "v2",
    }
    response = requests.post("https://v3.savevid.net/api/ajaxSearch", headers=headers, data=payload)
    data = response.json()
    js_code = data["data"].replace("\\", "")
    lista = re.findall(r'\((.*?)\)', js_code)
    js_args = lista[-1]

    val+=js_args+')'
    result = js2py.eval_js(val)
    soup = bs4.BeautifulSoup(result, 'html.parser')
    elem = soup.find_all("a")
    url = elem[1].get("href").replace("\\", "").replace('"', '')
    response = requests.get(url, headers=headers)
    name = hashlib.md5(video_url.encode('utf-8')).hexdigest()
    with open("{}.mp4".format(name), "wb") as f:
        f.write(response.content)
    return "{}.mp4".format(name)