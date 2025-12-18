import requests
import allure
from endpoints.endpoint import Endpoint


class GetOneMeme(Endpoint):

    @allure.step("Получение мема по ID")
    def get_meme_by_id(self, meme_id):
        """Получение одного мема по id"""
        self.response = requests.get(
            f'{self.url}/meme/{meme_id}',
            headers=self.headers
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response

    @allure.step("Проверка полученного мема")
    def verify_meme_received_successfully(self, expected_id):
        """Проверка что получен правильный мем"""
        self.check_that_status_is_200()
        assert self.json['id'] == expected_id, f"Expected ID {expected_id}, got {self.json['id']}"

    @allure.step("Проверка получения мема без авторизации")
    def verify_unauthorized_get_by_id(self, meme_id):
        """Проверка что получение мема по ID без авторизации возвращает 401"""
        original_token = self.headers.get('Authorization')

        try:
            # Удаляем токен авторизации
            if 'Authorization' in self.headers:
                del self.headers['Authorization']

            # Пытаемся получить мем
            self.get_meme_by_id(meme_id)

            # Используем существующий метод check_unauthorized_error
            self.check_unauthorized_error()

            return self.response
        finally:
            # Восстанавливаем заголовки
            if original_token:
                self.headers['Authorization'] = original_token
