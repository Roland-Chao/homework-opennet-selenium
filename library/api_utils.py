import requests, json
from library.exception import *
from library.logger import HandleLog

class APIUtils():
    def __init__(self, session):
        super().__init__()
        self.host = '[API Utils]'
        self.session = session
        self.log = HandleLog()
        
    def get_request(self, show_log=True, **kwargs):
        return self._request('get', show_log, **kwargs)

    def post_request(self, show_log=True, **kwargs):
        return self._request('post', show_log, **kwargs)
    
    def delete_request(self, show_log=True, **kwargs):
        return self._request('delete', show_log, **kwargs)
    
    def patch_request(self, show_log=True, **kwargs):
        return self._request('patch', show_log, **kwargs)

    def put_request(self, show_log=True, **kwargs):
        return self._request('put', show_log, **kwargs)
    
    def _request(self, method, show_log=True, **kwargs):
        try:
            self._last_url = kwargs.get("url")
            request_log = {
                k: v for k, v in {
                    "method": method.upper(),
                    "url": self._last_url,
                    "headers": dict(self.session.headers),
                    "params": kwargs.get("params"),
                    "data": kwargs.get("data"),
                    "json": kwargs.get("json"),
                }.items() if v is not None
            }
            self.log.info_log(f"{json.dumps(request_log, indent=4, ensure_ascii=False)}")
            
            try:
                self.response = self.session.request(
                    method, 
                    verify=self.session.verify,
                    **kwargs
                )
            
            except ConnectionError as e:
                raise SendRequestError(f'{self.host} Request failed: {str(e)}')
            
            self.log.info_log(f'{self.host} Response code: {self.response.status_code}')
            try:
                response_content = self.response.json()
                if show_log:
                    self.log.info_log(f'{self.host} Response content: {json.dumps(response_content, indent=4, ensure_ascii=False)}')
                    
            except ValueError:
                if show_log:
                    self.log.info_log(f'{self.host} Response content: {self.response.text[:200]}...')
                
            return self.response
            
        except requests.exceptions.RequestException as e:
            self.log.error_log(f'{self.host} Request failed: {str(e)}')
            raise SendRequestError(f'{self.host} Request failed: {str(e)}')
        
    def check_status_success(self):
        status_code = self.response.status_code
        self.log.info_log(f"check_status_code {status_code}")

        if status_code not in [200, 201, 202, 204]:
            try:
                detail = json.dumps(self.response.json(), indent=4, ensure_ascii=False)
                
            except ValueError:
                detail = self.response.text
                detail = (detail[:200] + '...') if len(detail) > 200 else detail
            
            except Exception:
                detail = self.response.text
            
            error_message = f'- Response code: {status_code}\n'
            error_message += f'- Request Url: {self._last_url}\n'
            error_message += f'- Detail: {detail}'
            match status_code:
                case 504:
                    raise API504Error(error_message)
                case 500:
                    raise API500Error(error_message)
                case 503:
                    raise API503Error(error_message)
                case 404:
                    raise API404Error(error_message)
                case 403:
                    raise API403Error(error_message)
                case 400:
                    raise API400Error(error_message)
                case _:
                    raise APIOtherStatusCodeError(error_message)
        return self
    
    def check_status_error(self, expected_error_code: int):
        status_code = self.response.status_code
        self.log.info_log(f"check_status_code {status_code}")

        if status_code != expected_error_code:
            raise APIOtherStatusCodeError(f"Response code: {status_code}")
        return self

    def get_response_data(self, key=None) -> dict:
        response_data = self.response.json()
        if key:
            return response_data[key]
        else:
            return response_data