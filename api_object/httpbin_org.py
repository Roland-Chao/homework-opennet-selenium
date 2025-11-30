from library.api_utils import APIUtils
from library.allure import allure_attach_log

class HttpbinOrg(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.base_url = "https://httpbin.org"

    @allure_attach_log(log_name="[Post] POST API (httpbin.org)")
    def post(self, **kwargs):
        api_url = f"{self.base_url}/post"
        self.post_request(url=api_url, **kwargs)
        return self

    @allure_attach_log(log_name="[Post] Custom Endpoint (httpbin.org)")
    def post_endpoint(self, endpoint: str, **kwargs):
        api_url = f"{self.base_url}{endpoint}"
        self.post_request(url=api_url, **kwargs)
        return self