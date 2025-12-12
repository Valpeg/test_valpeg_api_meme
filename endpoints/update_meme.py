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
