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
