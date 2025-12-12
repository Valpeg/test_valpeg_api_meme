import pytest


# Данные для позитивных тестов (успешное создание мемов)
TEST_DATA = [
    # Первый набор данных для теста создания мема
    {'body': {
        "text": "Первый мем",
        "url": "https://example.com/meme1.jpg",
        "tags": ["tag1", "tag2"],
        "info": {"colors": "colorful", "objects": ["image"]}
    }},
    # Второй набор данных для теста создания мема
    {'body': {
        "text": "Второй мем",
        "url": "https://example.com/meme2.jpg",
        "tags": ["funny", "cat"],
        "info": {"colors": "black", "objects": ["cat", "text"]}
    }},
    # Третий набор данных для теста создания мема
    {'body': {
        "text": "Третий мем с длинным текстом",
        "url": "https://example.com/meme3.jpg",
        "tags": ["long", "text"],
        "info": {"colors": "multicolor", "objects": ["picture", "text", "frame"]}
    }}
]

# Данные для негативных тестов (ожидаемые ошибки 400)
NEGATIVE_TEST_DATA = [
    # Отсутствует обязательное поле text
    {'body': {
        "url": "https://example.com/meme.jpg",
        "tags": ["tag"],
        "info": {}
    }},
    # Отсутствует обязательное поле url
    {'body': {
        "text": "Test meme",
        "tags": ["tag"],
        "info": {}
    }},
    # Отсутствует обязательное поле tags
    {'body': {
        "text": "Test meme",
        "url": "https://example.com/meme.jpg",
        "info": {}
    }},
    # Отсутствует обязательное поле info
    {'body': {
        "text": "Test meme",
        "url": "https://example.com/meme.jpg",
        "tags": ["tag"]
    }},
    # Пустое тело запроса
    {'body': {}},
    # Неправильный тип данных для tags (строка вместо массива)
    {'body': {
        "text": "Test",
        "url": "https://example.com",
        "tags": "not an array",
        "info": {}
    }},
    # Неправильный тип данных для info (строка вместо объекта)
    {'body': {
        "text": "Test",
        "url": "https://example.com",
        "tags": ["tag"],
        "info": "not an object"
    }},
    # Null значения в обязательных полях
    {'body': {
        "text": None,
        "url": "https://example.com",
        "tags": ["tag"],
        "info": {}
    }}
]

# Данные для тестов с ошибкой "не найдено" (404)
NOT_FOUND_TEST_DATA = [
    # Неправильный URL endpoint
    {'url': 'http://memesapi.course.qa-practice.com/wrong_endpoint',
     'body': {
         "text": "Test meme",
         "url": "https://example.com/meme.jpg",
         "tags": ["tag"],
         "info": {}
     }},
    # URL с опечаткой
    {'url': 'http://memesapi.course.qa-practice.com/mem',
     'body': {
         "text": "Test meme",
         "url": "https://example.com/meme.jpg",
         "tags": ["tag"],
         "info": {}
     }},
    # Несуществующий endpoint
    {'url': 'http://memesapi.course.qa-practice.com/nonexistent',
     'body': {
         "text": "Test meme",
         "url": "https://example.com/meme.jpg",
         "tags": ["tag"],
         "info": {}
     }}
]

# Данные для обновления мемов
UPDATE_TEST_DATA = [
    # Полное обновление мема
    {'body': {
        "id": None,  # Будет заполнено в тесте
        "text": "Обновленный текст мема",
        "url": "https://example.com/updated_meme.jpg",
        "tags": ["обновленный", "тег"],
        "info": {"colors": "updated", "objects": ["updated"]}
    }},
    # Обновление с минимальными изменениями
    {'body': {
        "id": None,
        "text": "Только текст изменен",
        "url": "https://example.com/meme.jpg",
        "tags": ["tag1", "tag2"],
        "info": {"colors": "colorful", "objects": ["image"]}
    }},
    # Обновление с новыми тегами
    {'body': {
        "id": None,
        "text": "Мем с новыми тегами",
        "url": "https://example.com/meme.jpg",
        "tags": ["новый", "тег", "дополнительный"],
        "info": {"colors": "colorful", "objects": ["image"]}
    }}
]


def test_auth_token_working(authorize_endpoint):
        """Проверка что токен работает"""
        # Просто вызываем метод из эндпоинта
        is_working = authorize_endpoint.verify_current_token_working()


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


# Тест полного обновления мема (PUT запрос)
def test_put_meme(update_meme_endpoint, new_meme_id):
    # Тело запроса для полного обновления мема
    body = {
        "id": new_meme_id,
        "text": "Полностью обновленный мем",
        "url": "https://example.com/fully_updated_meme.jpg",
        "tags": ["обновленный", "полностью"],
        "info": {"colors": "new colors", "objects": ["new object"]}
    }
    # Выполняем полное обновление мема
    update_meme_endpoint.update_meme(new_meme_id, body)
    # Проверяем, что мем успешно обновлен
    update_meme_endpoint.verify_meme_updated_successfully(
        body['text'],  # Ожидаемый текст мема
        body['url'],  # Ожидаемый URL
        body['tags']  # Ожидаемые теги
    )


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
    # Авторизуем пользователя
    authorize_endpoint.authorize_user()
    # Проверяем, что авторизация прошла успешно
    authorize_endpoint.check_that_status_is_200()
    # Проверяем, что в ответе есть токен
    response_json = authorize_endpoint.response.json()
    assert 'token' in response_json, "Token should be in response"


# Тест проверки валидности токена
def test_check_token_validity(authorize_endpoint, auth_token):
    # Проверяем валидность токена
    authorize_endpoint.check_token_validity(auth_token)
    # Проверяем, что токен валиден
    authorize_endpoint.check_that_status_is_200()


@pytest.mark.skip
# Тест доступа без авторизации
def test_unauthorized_access():
    # Импортируем класс напрямую, чтобы не использовать фикстуру с токеном
    from endpoints.get_all_meme import GetAllMemes
    # Создаем endpoint без авторизации
    endpoint = GetAllMemes()
    # Пытаемся получить мемы без авторизации
    endpoint.get_all_memes()
    # Проверяем, что получили ошибку авторизации
    endpoint.check_unauthorized_error()


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
