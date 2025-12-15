import requests
import allure
from endpoints.endpoint import Endpoint


class UpdateMeme(Endpoint):

    @allure.step("Обновление мема")
    def update_meme(self, meme_id, body):
        """Изменение существующего мема"""
        self.response = requests.put(
            f'{self.url}/meme/{meme_id}',
            json=body,
            headers=self.headers
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response

    @allure.step("Проверка успешного обновления мема")
    def verify_meme_updated_successfully(self, expected_text, expected_url, expected_tags):
        """Проверка обновленного мема"""
        self.check_that_status_is_200()
        assert self.json['text'] == expected_text
        assert self.json['url'] == expected_url
        assert self.json['tags'] == expected_tags

    @allure.step("Проверка обновления мема без авторизации")
    def verify_unauthorized_update(self, meme_id, body):
        """Проверка что обновление мема без авторизации возвращает 401"""
        original_token = self.headers.get('Authorization')

        try:
            # Удаляем токен авторизации
            if 'Authorization' in self.headers:
                del self.headers['Authorization']

            # Пытаемся обновить мем
            self.update_meme(meme_id, body)

            # Используем существующий метод check_unauthorized_error
            self.check_unauthorized_error()

            return self.response
        finally:
            # Восстанавливаем заголовки
            if original_token:
                self.headers['Authorization'] = original_token
