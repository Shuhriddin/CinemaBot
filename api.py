import aiohttp
from environs import Env
from data.config import BACKEND_URL
import asyncio
env = Env()
env.read_env()
URL = f"{env.str('BACKEND_URL')}/api"


async def get_user(telegram_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/user/", data={'telegram_id': telegram_id}) as response:
                if response.status == 204:
                    return "Not found"
                data = await response.json()
                return data
        except:
            return {}

async def create_user(telegram_id: str, language='uz', name: str = None):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/botuser/", data={'telegram_id': telegram_id, 'name': name, 'language': language}) as response:
                if response.status == 201:
                    data = await response.json()
                    return data
                else:
                    error_message = await response.text()
                    print(f"Failed to create user: {response.status} - {error_message}")
                    return "User creation failed"
        except Exception as e:
            print(f"Exception occurred: {e}")
            return "Error"

async def get_all_users():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/botuser/") as response:
                data = await response.json()
                return data
        except:
            return []

async def users_count():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/botuser") as response:
                if response.status == 200:
                    data = await response.json()
                    count = len(data)
                    return count
        except:
            return 0

async def change_user_language(telegram_id, language):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/lang/", data={'telegram_id': telegram_id, 'language': language}) as response:
                if response.status == 204:
                    return 'Not Found'
                else:
                    return await response.json()
        except:
            return None

async def add_channel(channel_id: str, channel_name: str = None, channel_members_count: str = None):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/channels/", data={'channel_id': channel_id, 'channel_name': channel_name, 'channel_members_count': channel_members_count}) as response:
                if response.status == 201:
                    return 'ok'
                else:
                    return 'bad'
        except:
            return None

async def get_all_channels():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=f"{URL}/channels/") as response:
                return await response.json()
        except:
            return []

async def get_channel(channel_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/channel/", data={'channel_id': channel_id}) as response:
                if response.status == 206:
                    return await response.json()
                else:
                    return {}
        except:
            return {}

async def delete_channel(channel_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=f"{URL}/delete_channel/", data={'channel_id': channel_id}) as response:
                if response.status == 200:
                    return 'Ok'
                else:
                    return "Bad"
        except:
            return "Bad"

async def create_movie(description=None, file_id=None):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/movie/", data={'description': description, 'file_id': file_id}) as response:
                data = await response.json()
                return data.get('id', "Yuklanmadi!")
        except Exception as e:
            print(f"Error in create_movie: {e}")
            return "Yuklanmadi!"

# Teppasiga tegish mumkin emas xamma kod ishlaydi
async def search_movie(key):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/movies/?search={key}") as response:
                data = await response.json()
                return data
        except Exception as e:
            # print(f"Error in search_movie: {e}")
            return []

async def search_movie_code(code):
    async with aiohttp.ClientSession() as session:
        try:
            # URL ni o'zgartirmaymiz, ammo so'rov manzilini to'g'ri shaklda yaratamiz
            url = f"{URL}/movie_code/{code}"
            async with session.get(url) as response:
                print(f"Status kodi: {response.status}")
                if response.status == 206:
                    data = await response.json()
                    # print(f"Qaytgan ma'lumot: {data}")
                    return data
                else:
                    # print(f"Kino yo`q! Status kodi: {response.status}")
                    return {}
        except Exception as e:
            return {}

async def get_film(id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/movie/{id}/") as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    # print(f"Unexpected status code {response.status}: {await response.text()}")
                    return {}
        except Exception as e:
            # print(f"Error in get_film: {e}")
            return {}

async def movie_rate(code):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{URL}/movie_rate/", data={'id': code}) as response:
                if response.status == 206:
                    data = await response.json()
                    return data
                elif response.status == 200:
                    data = await response.json()
                    return data
                else:
                    # print(f"Unexpected status code {response.status}: {await response.text()}")
                    return {}
        except Exception as e:
            # print(f"Error in movie_rate: {e}")
            return {}

async def top_movies():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{URL}/movie_top/") as response:
                data = await response.json()
                return data
        except Exception as e:
            # print(f"Error in top_movies: {e}")
            return []