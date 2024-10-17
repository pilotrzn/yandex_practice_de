from package.cls_api import APIRequester


class SWRequester(APIRequester):
    def set_url(self, new_url: str):
        self.base_url = new_url

    def get_sw_categories(self) -> list:
        ls_category = []
        self.set_url(f'{self.base_url}api/')
        response = self.get()
        categories = dict(response.json())
        for key in categories:
            ls_category.append(key)
        return ls_category

    def get_sw_info(self, sw_type: str) -> str:
        self.set_url(f'{self.base_url}{sw_type}')
        return self.get().text
