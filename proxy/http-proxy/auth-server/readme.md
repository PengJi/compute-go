产生 jwt
```bash
python auth_client.py -g | python -m json.tool
```
示例输出
```json
{
    "msg": "success",
    "code": "0",
    "data": [
        {
            "clusterName": "OpenAPI\u8ba1\u7b97\u4e2d\u5fc3",
            "clusterId": "11112",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMTExMTIiLCJleHAiOjE3MjQ5ODkyNTQsInVzZXJuYW1lIjoidGVzdCJ9.f9R6w1AnZQGNwJlIph5Vb5v_tdJYEHSrwCCKGtRSZBA"
        },
        {
            "clusterName": "test\u4e2d\u5fc3",
            "clusterId": "111131",
            "token": ""
        },
        {
            "clusterName": "ac",
            "clusterId": "0",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDk4OTI1NCwidXNlcm5hbWUiOiJ0ZXN0In0.0l1dxliCL3w8vDJm3SSmteEpXR8C4bUcGxSpnJP8Zxg"
        }
    ]
}

```

验证 jwt
```bash
python auth_client.py -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDk4OTIxMiwidXNlcm5hbWUiOiJ0ZXN0In0.hyG0XxBNzAyli_aBK1Gu7ujROW_Yd1rodT3xnPCs43M | python -m json.tool
```
示例输出
```bash
{
    "msg": "success",
    "code": "0",
    "data": "token is valid"
}
```
