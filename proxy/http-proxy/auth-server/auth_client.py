import click
import requests

ADDR = "http://172.26.23.163:8080"


def generate_token():
    url = ADDR + "/ac/openapi/v2/tokens"
    payload = {}
    headers = {
        "Content-Type": "application/json",
        # TODO
        "user": "test",
        "password": "111111",
        "orgid": "6048ce7ba15c2af2e8cec12991ec13cf",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def validate_token(jwt_token):
    url = ADDR + "/ac/openapi/v2/tokens/state"

    payload = {}
    headers = {
        "token": jwt_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


@click.group(name="token")
def token():
    """Define group of commands."""
    pass


@token.command(name="run")
@click.option("-g", "--generate", is_flag=True, help="generate token")
@click.option("-t", "--token", required=False, default="", help="token to be verified")
def run(generate, token):
    if generate:
        generate_token()
        return

    if token:
        validate_token(token)
        return

    print("Please specify either generate or token.")


if __name__ == "__main__":
    run()
