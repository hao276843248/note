# requests

POST请求发送json数据

```py
# json数据不用转换，直接扔给json参数就行了
# timeout只限制连接上服务器后接收到服务器返回第一条数据的时间，超时抛出requests.exception.ReadtimeError
response = requests.post(url, json=dict_data, timeout=10)
```