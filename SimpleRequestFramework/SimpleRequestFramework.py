import requests
import json
import os


class SimpleRequestFramework:
    def __init__(self, config_json=None, save_directory=".", use_proxy=False, proxy_type="http", proxy_address=None, headers=None, cookies=None):
        """
        初始化 SimpleRequestFramework 实例。

        :param config_json: JSON 字符串，包含初始化的配置信息。
        :param save_directory: 存储响应文件的目录。默认为当前目录。
        :param use_proxy: 是否使用代理。默认为 False。
        :param proxy_type: 代理类型，支持 "http", "https", 和 "socks5"。只在 use_proxy 为 True 时有效。
        :param proxy_address: 代理地址。例如: "socks5://127.0.0.1:1080"。只在 use_proxy 为 True 时有效。
        :param headers: 自定义请求头，格式为字典类型。例如: {"User-Agent": "CustomUserAgent/1.0"}。
        :param cookies: 自定义 cookies，格式为字典类型。例如: {"session": "YOUR_SESSION_COOKIE", "user_id": "123456"}。
        """
        if config_json:
            config_data = json.loads(config_json)
            save_directory = config_data.get("save_directory", ".")
            use_proxy = config_data.get("use_proxy", False)
            proxy_type = config_data.get("proxy_type", "http")
            proxy_address = config_data.get("proxy_address", None)
            headers = config_data.get("headers", {})
            cookies = config_data.get("cookies", {})

        self.save_directory = save_directory
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        self.proxies = {}
        if use_proxy and proxy_type and proxy_address:
            if proxy_type.lower() in ["http", "https", "socks5"]:
                self.proxies[proxy_type.lower()] = proxy_address
            else:
                print("不支持的代理类型：", proxy_type)

        self.headers = headers if headers else {}
        self.cookies = cookies if cookies else {}

    def _send_request(self, method, url, **kwargs):
        if self.proxies:
            kwargs["proxies"] = self.proxies

        # 设置默认 headers
        headers = kwargs.get("headers", {})
        if headers is None:
            headers = {}
        headers.update(self.headers)
        kwargs["headers"] = headers

        # 添加默认 cookies
        cookies = kwargs.get("cookies", {})
        if cookies is None:
            cookies = {}
        cookies.update(self.cookies)
        kwargs["cookies"] = cookies

        response = None
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()

            if not response.content:
                print(f"{method} 请求返回了空内容")
                return None

            return response.json()

        except requests.RequestException as e:
            print(f"{method} 请求失败: {e}")
        except json.JSONDecodeError:
            print(f"{method} 请求的响应不是一个有效的 JSON 格式")

        if response:
            print("响应内容：", response.text)

        return None

    def get_request(self, url, params=None, headers=None):
        """
        发起GET请求并获取响应数据。
        """
        return self._send_request("GET", url, params=params, headers=headers)

    def post_request(self, url, data=None, headers=None):
        """
        发起POST请求并获取响应数据。
        """
        return self._send_request("POST", url, json=data, headers=headers)

    def save_data_to_file(self, data, file_name):
        """
        将数据保存为JSON文件。
        """
        full_path = os.path.join(self.save_directory, file_name, ".json")
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"数据已保存到 {full_path}")
        except Exception as e:
            print(f"保存失败: {e}")

    def fetch_and_save(self, url, file_name, method="GET", params_or_data=None, headers=None):
        """
        根据请求方法从URL获取数据并保存到文件。
        """
        if method.upper() == "GET":
            data = self.get_request(url, params=params_or_data, headers=headers)
        elif method.upper() == "POST":
            data = self.post_request(url, data=params_or_data, headers=headers)
        else:
            print(f"不支持的请求方法: {method}")
            return

        if data:
            self.save_data_to_file(data, file_name)
            return data

