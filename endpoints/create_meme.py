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
        """Проверка созданного мема"""
        self.check_that_status_is_200()
        # Проверяем что json есть перед доступом
        if hasattr(self, 'json') and self.json:
            assert self.json['text'] == expected_text
            assert self.json['url'] == expected_url
            assert self.json['tags'] == expected_tags
            assert 'id' in self.json
