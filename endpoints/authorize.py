import requests
import allure
from endpoints.endpoint import Endpoint


class Authorize(Endpoint):

    @allure.step("Авторизация пользователя")
    def authorize_user(self, name="valpeg"):
        """Авторизация и получение токена"""
        self.response = requests.post(
            f'{self.url}/authorize',
            json={'name': name},
            headers=self.headers
        )
        if self.response.status_code == 200:
            self.token = self.response.json()['token']
            self.headers['Authorization'] = self.token
        return self.response

    @allure.step("Проверка валидности токена")
    def check_token_validity(self, token):
        """Проверка жив ли токен"""
        self.response = requests.get(
            f'{self.url}/authorize/{token}',
            headers={'Authorization': token}
        )
        return self.response

    @allure.step("Проверка что текущий токен работает")
    def verify_current_token_working(self):
        """Проверка что текущий токен в headers работает"""
        if 'Authorization' not in self.headers:
            return False

        # Проверяем на существующем меме (ID 1)
        test_response = requests.get(
            f'{self.url}/meme/1',
            headers=self.headers
        )

        # Сохраняем тестовый ответ в отдельную переменную
        self.test_response = test_response
        return test_response.status_code == 200
