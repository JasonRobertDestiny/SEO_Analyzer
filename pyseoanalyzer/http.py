import certifi
from urllib3 import PoolManager
from urllib3 import Timeout


class Http:
    def __init__(self):
        user_agent = {"User-Agent": "Mozilla/5.0"}

        self.http = PoolManager(
            timeout=Timeout(connect=10.0, read=30.0),  # 增加超时时间：连接10秒，读取30秒
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where(),
            headers=user_agent,
        )

    def get(self, url):
        return self.http.request("GET", url)


http = Http()
