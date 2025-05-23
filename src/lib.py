import os
import re
from datetime import timedelta

import requests_cache


class SteamAPI:
    def __init__(self, key: str, expire_after=timedelta(hours=24)) -> None:
        self.key = key
        self.session = requests_cache.CachedSession(
            expire_after=expire_after,
            ignored_parameters=['key'],
        )

    def resolve_steam_id(self, custom_url: str) -> str:
        response = self.session.get(
            'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1',
            params={'key': self.key, 'vanityurl': custom_url},
        )
        response.raise_for_status()
        content = response.json()['response']
        if content['success'] != 1:
            raise ValueError(content['message'])
        return content['steamid']

    def get_user_apps(self, steam_id: str) -> list[int]:
        response = self.session.get(
            'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1',
            params={'key': self.key, 'steamid': steam_id},
        )
        response.raise_for_status()
        content = response.json()['response']

        apps = [
            app['appid']
            for app in sorted(
                content['games'],
                key=lambda app: app['playtime_forever'],
                reverse=True,
            )
        ]
        return apps


class SteamCardExchangeScraper:
    def __init__(self, expire_after=-1) -> None:
        self.session = requests_cache.CachedSession(expire_after=expire_after)

    def get_badge_urls(self, app_id: int):
        response = self.session.get(
            'https://www.steamcardexchange.net/index.php',
            params=f'gamepage-appid-{app_id}',
        )
        response.raise_for_status()
        return re.findall('steamcdn-a\\.akamaihd\\.net.+/(.+).png', response.text)


class AppDB:
    def __init__(self, path: str) -> None:
        pass


STEAM_API = SteamAPI(key=os.environ['STEAM_KEY'])
STEAMCARDEXCHANGE_SCRAPER = SteamCardExchangeScraper()
APP_DB = AppDB(':memory:')
