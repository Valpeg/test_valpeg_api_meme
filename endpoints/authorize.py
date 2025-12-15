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

    @allure.step("Проверка успешной авторизации")
    def verify_authorization_successful(self):
        """Проверка что авторизация прошла успешно"""
        self.check_that_status_is_200()
        response_json = self.response.json()
        assert 'token' in response_json, "Token should be in response"
        return True

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
            raise AssertionError("Токен авторизации отсутствует в headers")

        # Проверяем валидность токена
        token = self.headers['Authorization']
        self.check_token_validity(token)

        # Проверяем что получили успешный ответ
        self.check_that_status_is_200()

        return True
