import requests
import allure
from endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):

    @allure.step("Удаление мема")
    def delete_meme_by_id(self, meme_id):
        """Удаление мема по ID"""
        self.response = requests.delete(
            f'{self.url}/meme/{meme_id}',
            headers=self.headers
        )
        return self.response

    @allure.step("Проверка успешного удаления")
    def verify_meme_deleted_successfully(self):
        """Проверка что удаление прошло успешно"""
        self.check_that_status_is_200()

    @allure.step("Проверка что мем удален")
    def verify_meme_not_found(self, meme_id):
        """Проверка что мем действительно удален"""
        check_response = requests.get(
            f'{self.url}/meme/{meme_id}',
            headers=self.headers
        )
        self.response = check_response
        self.check_not_found_error()
