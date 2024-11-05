import hashlib


class MarsURLEncoder:
    def __init__(self):
        self.link_dict = {}
        self.prefix = 'https://ma.rs/'
        self.md5 = hashlib.md5()

    def encode(self, long_url: str) -> str:
        self.md5.update(long_url.encode())
        hash = self.md5.hexdigest()
        if hash not in self.link_dict.keys():
            self.link_dict[hash] = long_url
        return f'{self.prefix}{hash}'

    def decode(self, short_url: str):
        search_hash = short_url.split('/')[-1]
        if search_hash in self.link_dict.keys():
            return self.link_dict.get(search_hash)


def main():
    links = ('https://tsup.ru/mars/marsohod-1/01-09-2023/daily_job.html',
             'https://tsup.ru/mars/01-08-2023/weekly_job.html',
             )
    encoder = MarsURLEncoder()
    for link in links:
        print(encoder.encode(link))

    for key in encoder.link_dict.keys():
        print(encoder.decode(key))


if __name__ == '__main__':
    main()
