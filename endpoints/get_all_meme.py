import requests
import allure
from endpoints.endpoint import Endpoint


class GetAllMemes(Endpoint):

    @allure.step("Получение всех мемов")
    def get_all_memes(self):
        """Получение списка всех мемов"""
        self.response = requests.get(
            f'{self.url}/meme',
            headers=self.headers
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response

    @allure.step("Проверка получения списка мемов")
    def verify_memes_list_received(self):
        """Проверка получения списка мемов"""
        self.check_that_status_is_200()
        assert isinstance(self.json, list), "Response should be a list"

    @allure.step("Проверка получения мемов без авторизации")
    def verify_unauthorized_get_all(self):
        """Проверка что получение всех мемов без авторизации возвращает 401"""
        original_token = self.headers.get('Authorization')

        try:
            # Удаляем токен авторизации
            if 'Authorization' in self.headers:
                del self.headers['Authorization']

            # Пытаемся получить мемы
            self.get_all_memes()

            # Используем существующий метод check_unauthorized_error
            self.check_unauthorized_error()

            return self.response
        finally:
            # Восстанавливаем заголовки
            if original_token:
                self.headers['Authorization'] = original_token
