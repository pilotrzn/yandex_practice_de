from package.cls_api import APIRequester


class SWRequester(APIRequester):
    def set_url(self, url: str):
        self.base_url = url

    def get_sw_categories(self) -> dict:
        self.set_url(f'{self.base_url}api/')
        response = self.get()
        categories = dict(response.json())
        return categories

    def get_sw_info(self, sw_type: str) -> str:
        self.set_url(f'{sw_type}')
        return self.get().text
