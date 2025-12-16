import allure


class Endpoint:
    url = 'http://memesapi.course.qa-practice.com'
    response = None
    json = None
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'nSGjlb7B2uym1Cq'  # Фиксированный токен из Postman
    }

    @allure.step('Проверка успешного ответа (200)')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200, f"Expected 200, got {self.response.status_code}"

    @allure.step('Проверка ошибки авторизации (401)')
    def check_unauthorized_error(self):
        assert self.response.status_code == 401, f"Expected 401, got {self.response.status_code}"

    @allure.step('Проверка ошибки клиента (400)')
    def check_bad_request_error(self):
        assert self.response.status_code == 400, f"Expected 400, got {self.response.status_code}"

    @allure.step('Проверка ошибки "не найдено" (404)')
    def check_not_found_error(self):
        assert self.response.status_code == 404, f"Expected 404, got {self.response.status_code}"

    @allure.step('Проверка содержимого мема')
    def verify_meme_content(self, expected_text, expected_url, expected_tags, expected_info):
        """Общая проверка содержимого мема для создания и обновления"""
        self.check_that_status_is_200()

        # Проверяем что json есть перед доступом
        if not hasattr(self, 'json') or not self.json:
            raise AssertionError("JSON ответ отсутствует")

            # Проверяем ВСЕ 5 полей мема
        assert self.json['text'] == expected_text, \
            f"Expected text '{expected_text}', got '{self.json['text']}'"
        assert self.json['url'] == expected_url, \
            f"Expected URL '{expected_url}', got '{self.json['url']}'"
        assert self.json['tags'] == expected_tags, \
            f"Expected tags {expected_tags}, got {self.json['tags']}"
        assert self.json['info'] == expected_info, \
            f"Expected info {expected_info}, got {self.json['info']}"

        # Просто убеждаемся что updated_by есть (но не проверяем значение)
        assert 'updated_by' in self.json, "Поле 'updated_by' должно быть в ответе"

        assert 'id' in self.json, "ID должен присутствовать в ответе"


    def set_token(self, token):
        """Установить токен авторизации"""
        self.headers['Authorization'] = token
