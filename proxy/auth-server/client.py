import requests

ADDR = "http://172.26.23.163:8080"


def get_token():
    url = ADDR + "/ac/openapi/v2/tokens"
    payload = {}
    headers = {
        "Content-Type": "application/json",
        "user": "test",
        "password": "111111",
        "orgid": "6048ce7ba15c2af2e8cec12991ec13cf",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def validate_token():
    url = ADDR + "/ac/openapi/v2/tokens/state"

    payload = {}
    headers = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDg1Mjk2NiwidXNlcm5hbWUiOiJ0ZXN0In0.0DtyGjVLkCy-RCNC65rl3Pg2_Af_cw_JpJATePganno"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    get_token()
    validate_token()
