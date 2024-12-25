import requests
import bs4
import urllib
from lxml.etree import parse
from lxml import html


import hashlib



def save_facebook_video(face_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
    }
    
    url = "https://getmyfb.com/process"
    response = requests.post(url, data={"id": face_url,"locale": "es"}, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    elem = soup.find("a", {"class": "hd-button"})
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
