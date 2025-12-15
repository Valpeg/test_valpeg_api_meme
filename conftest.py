import pytest
import requests
from endpoints.authorize import Authorize
from endpoints.create_meme import CreateMeme
from endpoints.get_all_meme import GetAllMemes
from endpoints.get_one_meme import GetOneMeme
from endpoints.update_meme import UpdateMeme
from endpoints.delete_meme import DeleteMeme
from data import default_meme  # Используем default_meme из data.py

@pytest.fixture()
def new_meme_id(create_meme_endpoint, delete_meme_endpoint):
    """Фикстура для создания временного мема"""
    print('Создание мема для теста')
    # Используем метод create_meme из класса CreateMeme
    create_meme_endpoint.create_meme(body=default_meme)
    # Получаем ID созданного мема из ответа
    meme_id = create_meme_endpoint.response.json()['id']

    yield meme_id
    print('Удаление мема после теста')

    # Используем метод delete_meme_by_id из класса DeleteMeme
    delete_meme_endpoint.delete_meme_by_id(meme_id)


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def get_one_meme_endpoint():
    return GetOneMeme()


@pytest.fixture()
def get_all_memes_endpoint():
    return GetAllMemes()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def authorize_endpoint():
    return Authorize()


# Простая фикстура для токена
@pytest.fixture()
def auth_token():
    """Фикстура для получения токена авторизации"""
    # Создаем endpoint авторизации
    auth_endpoint = Authorize()
    # Выполняем авторизацию
    auth_endpoint.authorize_user()
    # Получаем токен из ответа
    token = auth_endpoint.response.json()['token']
    return token
