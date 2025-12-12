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
