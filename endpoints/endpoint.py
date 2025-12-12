import allure


class Endpoint:
    url = 'http://memesapi.course.qa-practice.com'
    response = None
    json = None
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'nSGjlb7B2uym1Cq'  # Фиксированный токен из Postman
    }

    @allure.step('Проверка успешного ответа (200)')
    def check_that_status_is_200(self):
        assert self.response.status_code == 200, f"Expected 200, got {self.response.status_code}"

    @allure.step('Проверка ошибки авторизации (401)')
    def check_unauthorized_error(self):
        assert self.response.status_code == 401, f"Expected 401, got {self.response.status_code}"

    @allure.step('Проверка ошибки клиента (400)')
    def check_bad_request_error(self):
        assert self.response.status_code == 400, f"Expected 400, got {self.response.status_code}"

    @allure.step('Проверка ошибки "не найдено" (404)')
    def check_not_found_error(self):
        assert self.response.status_code == 404, f"Expected 404, got {self.response.status_code}"

    def set_token(self, token):
        """Установить токен авторизации"""
        self.headers['Authorization'] = token
