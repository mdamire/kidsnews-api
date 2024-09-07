
class NewsApiClientError(Exception):
    
    def __init__(self, msg='', status_code=None, response_text=None) -> None:
        self.status_code = status_code
        self.response_text = response_text
        if status_code or response_text:
            msg += f" status_code: {status_code}, response text: {response_text}"
        super().__init__(msg)
