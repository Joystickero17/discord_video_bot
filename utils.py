import os
import requests
import bs4
import re
import hashlib
from urllib.parse import urlparse, urlunparse

class AbstractDownloader:
    base_url = ""
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
        }

    def get_name(self):
        return hashlib.md5(self.url.encode('utf-8')).hexdigest()
    
    def download(self):
        url = self.get_video_url()
        name = self.get_name()
        name = self._save_video(url, name)
        return name
        
    def get_video_url(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _save_video(self, url, name):
        response = requests.get(url, headers=self.headers)
        full_name = "{}.mp4".format(name)
        with open(full_name, "wb") as f:
            f.write(response.content)
        return full_name


FACEBOOK = "facebook.com"
TIKTOK = "tiktok.com"


class InvalidUrlParseError(Exception):
    pass

class ParserNotFoundError(Exception):
    pass


class FacebookDownloader(AbstractDownloader):
    base_url = "https://getmyfb.com/process"
    def get_video_url(self):
        response = requests.post(self.base_url, data={"id": self.url,"locale": "es"}, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        elem = soup.find("a", {"class": "hd-button"})
        if not elem:
            elem = soup.find("a", {"class": "ig-button"})
        url = elem.attrs.get("href")
        if url is None:
            raise ValueError("url not found")
        return url

class TiktokDownloader(AbstractDownloader):
    base_url = "https://api.twitterpicker.com/tiktok/mediav2"
    def get_video_url(self):
        parsed = urlparse(self.url)
        clean_path = (parsed.path or "").rstrip("/")
        id_from_url = clean_path.split("/")[-1] if clean_path else ""
        if not id_from_url:
            raise ValueError("No se pudo extraer el id desde la URL")
        response = requests.get(self.base_url, params={"id": id_from_url}, headers=self.headers)
        data = response.json()
        url = data.get("video_no_watermark",{}).get("url")
        if url is None:
            raise ValueError("url not found")
        return url

class DownloaderFactory:
    VALID_HOSTNAMES = [
        (FacebookDownloader, ("facebook.com", "instagram.com", "fb.com", "fb.me", "fb.watch")),
        (TiktokDownloader, ("tiktok.com", "tiktok.app", "tiktok.video"))
    ]
    def get_url_from_message(self, message):
        # Acepta tanto discord.Message como str
        text = getattr(message, "content", message)
        if not isinstance(text, str):
            raise TypeError("message must be str o tener .content")

        text = text.strip()
        if not text:
            raise ValueError("Mensaje vacío")

        # Quita prefijos de comando tipo: !face, !tk, !insta, etc.
        # (si el usuario pega sólo la URL, esto no afecta)
        parts = text.split()
        if parts and parts[0].startswith("!"):
            text = " ".join(parts[1:]).strip()

        # Encuentra la primera URL aunque venga sin esquema (p.ej. instagram.com/...)
        # Limpia puntuación final común en chats: ), ], ., , etc.
        url_like_re = re.compile(
            r"(?P<url>("
            r"(?:https?://)?"
            r"(?:www\.)?"
            r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"
            r"(?:/[^\s<>\]\)]*)?"
            r"))",
            re.IGNORECASE,
        )
        m = url_like_re.search(text)
        if not m:
            raise InvalidUrlParseError("No se encontró una URL en el mensaje")

        candidate = m.group("url").strip()
        candidate = candidate.rstrip(").,;!?'\"»›]")

        # Normaliza a URL válida con esquema
        if not re.match(r"^https?://", candidate, flags=re.IGNORECASE):
            candidate = "https://" + candidate

        parsed = urlparse(candidate)
        if not parsed.netloc:
            raise ValueError("URL inválida")

        # Asegura que no quede algo raro en path/query/fragment
        normalized = urlunparse(
            (
                parsed.scheme.lower() if parsed.scheme else "https",
                parsed.netloc,
                parsed.path or "",
                parsed.params or "",
                parsed.query or "",
                parsed.fragment or "",
            )
        )
        return normalized

    def get_downloader(self, message):
        url = self.get_url_from_message(message.content)
        host = (urlparse(url).hostname or "").lower()
        for downloader, hostnames in self.VALID_HOSTNAMES:
            if host.endswith(hostnames):
                #print(f"Downloader: {downloader.__class__.__name__}, Host: {host}")
                return downloader(url)
        raise ParserNotFoundError("Invalid URL")