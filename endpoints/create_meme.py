import requests
import allure
from endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):

    @allure.step("Создание нового мема")
    def create_meme(self, body):
        """Создание нового мема"""
        self.response = requests.post(
            f'{self.url}/meme',
            json=body,
            headers=self.headers
        )
        # Пытаемся получить JSON только если статус 200
        if self.response.status_code == 200:
            try:
                self.json = self.response.json()
            except:
                self.json = None
        return self.response

    @allure.step("Проверка успешного создания мема")
    def verify_meme_created_successfully(self, expected_text, expected_url, expected_tags):
        """Проверка созданного мема - использует общий метод из родителя"""
        self.verify_meme_content(expected_text, expected_url, expected_tags)

    @allure.step("Проверка создания мема без авторизации")
    def verify_unauthorized_create(self, body):
        """Проверка что создание мема без авторизации возвращает 401"""
        # Сохраняем оригинальный токен
        original_token = self.headers.get('Authorization')

        try:
            # Удаляем токен авторизации
            if 'Authorization' in self.headers:
                del self.headers['Authorization']

            # Пытаемся создать мем
            self.create_meme(body)

            # Используем существующий метод check_unauthorized_error из родительского класса
            self.check_unauthorized_error()

            return self.response
        finally:
            # Восстанавливаем токен
            if original_token:
                self.headers['Authorization'] = original_token
