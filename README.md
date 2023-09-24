# SimpleRequestsFramework

## Description
This is a simple will be used to request requests wrapped up response package is json at the same time the content will be stored locally api package . Support for GET and POST requests , while supporting multiple proxy protocols , you can preset the Header and other related information .

## Installation
```bash
pip install simple-requests-framework
```

## Usage
```python
from SimpleRequestFramework import SimpleRequestFramework

custom_headers = {
    "User-Agent": "CustomUserAgent/1.0",
    "Authorization": "Bearer YOUR_TOKEN"
}
# new a framework instance, and set the save directory, use proxy, proxy type, proxy address, and custom headers
framework = SimpleRequestFramework(
    save_directory="output_files",
    use_proxy=True,
    proxy_type="http",
    proxy_address="http://127.0.0.1:8080",
    headers=custom_headers
)

# GET request example
get_url = "https://api.ip.sb/ip"
params = {
    "param1": "value1",
    "param2": "value2"
}
framework.fetch_and_save(get_url, "output_get.json", method="GET", params=params)

# POST request example
post_url = "https://httpbin.org/post"
data = {
    "data1": "value1",
    "data2": "value2"
}
framework.fetch_and_save(post_url, "output_post.json", method="POST", data=data)
```
Also supports configuration of framework instances as json files


create a json file named config.json
```json
{
    "save_directory": "output_files",
    "use_proxy": true,
    "proxy_type": "http",
    "proxy_address": "http://127.0.0.1:8080",
    "headers": {
      "User-Agent": "CustomUserAgent/1.0",
      "Authorization": "Bearer YOUR_TOKEN"
    }
}
```

```python
from SimpleRequestFramework import SimpleRequestFramework

framework = SimpleRequestFramework(config_json="config.json")
```