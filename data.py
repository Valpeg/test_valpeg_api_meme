default_meme = {
    "text": "С завода уйду, буду удаленно работать",
    "url": "https://encrypted-tbn0.gstatic.com/"
           "images?q=tbn:ANd9GcSMI__D3EzqPzYd2zt7nD6kotutd3hWxAPQig&s",
    "tags": ["Шариков", "Собачье сердце"],
    "info": {"colors": "black and white", "objects": ["picture", "text"]}
}

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
