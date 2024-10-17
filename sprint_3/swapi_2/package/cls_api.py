import requests as req


class APIRequester:

    def __init__(self) -> None:
        self.base_url = ''

    def get(self):
        try:
            response = req.get(self.base_url)
            response.raise_for_status()
        except req.ConnectionError as err:
            return f'Network Error {err}'
        except req.HTTPError as err:
            return f'HTTP Error {err}'
        return response
