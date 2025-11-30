from library.api_utils import APIUtils
from library.allure import allure_attach_log

class TheDogAPI(APIUtils):
    def __init__(self, session, api_key=None):
        super().__init__(session)
        self.base_url = "https://api.thedogapi.com/v1"
        self.api_key = api_key
        if api_key:
            self.session.headers.update({'x-api-key': api_key})

    @allure_attach_log(log_name="[Get] Get Breeds (thedogapi.com)")
    def get_breeds(self, **kwargs):
        api_url = f"{self.base_url}/breeds"
        self.get_request(url=api_url, **kwargs)
        return self

    @allure_attach_log(log_name="[Post] Add to Favourites (thedogapi.com)")
    def add_favourite(self, **kwargs):
        api_url = f"{self.base_url}/favourites"
        self.post_request(url=api_url, **kwargs)
        return self
