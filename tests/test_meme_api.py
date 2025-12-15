import pytest
from data import TEST_DATA, NEGATIVE_TEST_DATA, NOT_FOUND_TEST_DATA, UPDATE_TEST_DATA, default_meme
from endpoints.get_all_meme import GetAllMemes


def test_auth_token_working(authorize_endpoint):
    """Проверка что токен работает"""
    # Метод verify_current_token_working() сам содержит assert'ы
    # и выбросит исключение если токен не работает
    result = authorize_endpoint.verify_current_token_working()

    # Можно дополнительно проверить что метод вернул True
    assert result is True, "Метод должен возвращать True при успешной проверке"


# Тест получения мема по ID
def test_get_meme(get_one_meme_endpoint, new_meme_id):
    # Получаем мем по ID через эндпоинт
    get_one_meme_endpoint.get_meme_by_id(new_meme_id)
    # Проверяем, что полученный мем имеет правильный ID
    get_one_meme_endpoint.verify_meme_received_successfully(new_meme_id)


# Тест для создания мемов с разными данными
@pytest.mark.parametrize("test_data", TEST_DATA)
def test_create_meme(test_data, create_meme_endpoint):
    # Извлекаем тело запроса из тестовых данных
    body = test_data['body']
    # Отправляем POST запрос для создания мема
    create_meme_endpoint.create_meme(body=body)
    # Проверяем, что мем успешно создан с правильными данными
    create_meme_endpoint.verify_meme_created_successfully(
        body['text'],  # Ожидаемый текст мема
        body['url'],  # Ожидаемый URL
        body['tags']  # Ожидаемые теги
    )


# Тест для негативных сценариев (400)
@pytest.mark.parametrize("test_data", NEGATIVE_TEST_DATA)
def test_create_meme_negative_cases(test_data, create_meme_endpoint):
    # Извлекаем тело запроса из тестовых данных
    body = test_data['body']
    # Отправляем POST запрос с некорректными данными
    create_meme_endpoint.create_meme(body=body)
    # Проверяем, что статус код ответа равен 400 (ошибка клиента)
    create_meme_endpoint.check_bad_request_error()


# Тесты для негативных сценариев (401)
def test_get_all_memes_unauthorized(get_all_memes_endpoint):
    """Тест получения всех мемов без авторизации"""
    get_all_memes_endpoint.verify_unauthorized_get_all()

def test_get_meme_by_id_unauthorized(get_one_meme_endpoint, new_meme_id):
    """Тест получения мема по ID без авторизации"""
    get_one_meme_endpoint.verify_unauthorized_get_by_id(new_meme_id)

def test_create_meme_unauthorized(create_meme_endpoint):
    """Тест создания мема без авторизации"""
    body = default_meme.copy()
    create_meme_endpoint.verify_unauthorized_create(body)

def test_update_meme_unauthorized(update_meme_endpoint, new_meme_id):
    """Тест обновления мема без авторизации"""
    body = {
        "id": new_meme_id,
        "text": "Обновленный без авторизации",
        "url": "https://example.com/update.jpg",
        "tags": ["update"],
        "info": {}
    }
    update_meme_endpoint.verify_unauthorized_update(new_meme_id, body)

def test_delete_meme_unauthorized(delete_meme_endpoint, new_meme_id):
    """Тест удаления мема без авторизации"""
    delete_meme_endpoint.verify_unauthorized_delete(new_meme_id)


# Тест для проверки ошибок "не найдено" (404)
@pytest.mark.parametrize("test_data", NOT_FOUND_TEST_DATA)
def test_create_meme_not_found(test_data, create_meme_endpoint):
    # Извлекаем тело запроса и URL из тестовых данных
    body = test_data['body']
    wrong_url = test_data['url']

    # Отправляем POST запрос на неправильный URL
    create_meme_endpoint.url = wrong_url
    create_meme_endpoint.create_meme(body=body)

    # Используем метод из родительского класса Endpoint для проверки ошибки 404
    create_meme_endpoint.check_not_found_error()


@pytest.mark.skip # Тест зависает из-за медленного интернета, требует длительного таймаута
# Тест получения всех мемов
def test_get_all_memes(get_all_memes_endpoint):
    # Получаем все мемы
    get_all_memes_endpoint.get_all_memes()
    # Проверяем, что список мемов получен успешно
    get_all_memes_endpoint.verify_memes_list_received()


# Тест обновления мемов с разными данными
@pytest.mark.parametrize("test_data", UPDATE_TEST_DATA)
def test_update_meme_with_different_data(test_data, update_meme_endpoint, new_meme_id):
    # Извлекаем тело запроса из тестовых данных
    body = test_data['body']
    # Заменяем id на реальный
    body['id'] = new_meme_id

    # Выполняем обновление мема
    update_meme_endpoint.update_meme(new_meme_id, body)
    # Проверяем, что мем успешно обновлен
    update_meme_endpoint.verify_meme_updated_successfully(
        body['text'],  # Ожидаемый текст мема
        body['url'],  # Ожидаемый URL
        body['tags']  # Ожидаемые теги
    )


# Тест удаления мема
def test_delete_meme(delete_meme_endpoint, new_meme_id):
    # Удаляем мем по ID
    delete_meme_endpoint.delete_meme_by_id(new_meme_id)
    # Проверяем, что удаление прошло успешно (статус 200)
    delete_meme_endpoint.verify_meme_deleted_successfully()
    # Проверяем, что мем действительно удален (статус 404 при попытке получить)
    delete_meme_endpoint.verify_meme_not_found(new_meme_id)


# Тест авторизации пользователя
def test_authorize_user(authorize_endpoint):
    """Тест авторизации пользователя"""
    # Авторизуем пользователя
    authorize_endpoint.authorize_user()
    # Проверяем, что авторизация прошла успешно (все ассерты внутри метода)
    authorize_endpoint.verify_authorization_successful()


# Тест проверки валидности токена
def test_check_token_validity(authorize_endpoint, auth_token):
    # Проверяем валидность токена
    authorize_endpoint.check_token_validity(auth_token)
    # Проверяем, что токен валиден
    authorize_endpoint.check_that_status_is_200()


@pytest.mark.skip
# Тест доступа без авторизации
def test_unauthorized_access(get_all_memes_endpoint):
    # Убираем токен из заголовков эндпоинта
    get_all_memes_endpoint.headers.pop('Authorization', None)
    # Пытаемся получить мемы без авторизации
    get_all_memes_endpoint.get_all_memes()
    # Проверяем, что получили ошибку авторизации
    get_all_memes_endpoint.check_unauthorized_error()


# Тест получения несуществующего мема
def test_get_nonexistent_meme(get_one_meme_endpoint):
    # Пытаемся получить несуществующий мем
    non_existent_id = 999999
    get_one_meme_endpoint.get_meme_by_id(non_existent_id)
    # Проверяем, что получили ошибку 404
    get_one_meme_endpoint.check_not_found_error()


# Тест обновления несуществующего мема
def test_update_nonexistent_meme(update_meme_endpoint):
    # Пытаемся обновить несуществующий мем
    body = {
        "id": 999999,
        "text": "Несуществующий мем",
        "url": "https://example.com/nonexistent.jpg",
        "tags": ["несуществующий"],
        "info": {"colors": "none", "objects": ["none"]}
    }
    update_meme_endpoint.update_meme(999999, body)
    # Проверяем, что получили ошибку 404
    update_meme_endpoint.check_not_found_error()


# Тест удаления несуществующего мема
def test_delete_nonexistent_meme(delete_meme_endpoint):
    # Пытаемся удалить несуществующий мем
    delete_meme_endpoint.delete_meme_by_id(999999)
    # Проверяем, что получили ошибку 404
    delete_meme_endpoint.check_not_found_error()
