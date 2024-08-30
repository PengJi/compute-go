import requests

ADDR = "http://192.168.35.141:80"


def test_upload():
    """
    上传本地pdf到指定路径
    API: /efile/openapi/v2/file/upload
    DOC: https://www.scnet.cn/ac/openapi/doc/2.0/api/efile/upload.html
    """
    url = ADDR + "/efile/openapi/v2/file/upload"
    payload = {"cover": "uncover", "path": "/home/jipeng/file-server"}
    files = [
        (
            "file",
            ("upload_file.txt", open("/home/jipeng/compute-go/proxy/file-server/upload_file.txt"), "application/plain"),
        )
    ]
    headers = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDg1Mjk2NiwidXNlcm5hbWUiOiJ0ZXN0In0.0DtyGjVLkCy-RCNC65rl3Pg2_Af_cw_JpJATePganno"
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


def test_download():
    """
    下载指定路径pdf
    API: /efile/openapi/v2/file/download
    DOC: https://www.scnet.cn/ac/openapi/doc/2.0/api/efile/download.html
    """
    url = ADDR + "/efile/openapi/v2/file/download?path=/home/jipeng/file-server/download_file.txt"
    payload = {}
    headers = {
        "Content-Type": "application/json",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDg1Mjk2NiwidXNlcm5hbWUiOiJ0ZXN0In0.0DtyGjVLkCy-RCNC65rl3Pg2_Af_cw_JpJATePganno"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    # test_upload()
    test_download()


"""
curl 方式
1. 上传
curl --location 'https://api01.xxx.com:65103/efile/openapi/v2/file/upload' \
--header 'token: sdf.eyJjb21wdXRlVXNlciI6ImpzeWFkbWluIiwiYWNjb3VudFN0YXR1cyI6Ik93ZSIsImNyZWF0b3IiOiJhYyIsInJvbGUiOiIxIiwiZXhwaXJlVGltZSI6IjE3MDA1NDc2NzQxODgiLCJjbHVzdGVySWQiOiIxMTI1MCIsImludm9rZXIiOiJiN2I5NjViNjZkM2IzNWJjMTQ0ZDI5YWY1MWUxNjFhMSIsInVzZXIiOiJqc3lhZG1pbiIsInVzZXJJZCI6IjIxOTI1OTExMzgwIn0.Q1GcEhGAhKiAoZQEABY27uE1oHYqS3szAEMngv_cOc0' \
--form "cover=uncover" \
--form "file=@/Users/Downloads/demo/Linux.pdf" \
--form "path=/public/home/test/BASE"

2. 下载
curl --location 'https://api01.xxx.com:65103/efile/openapi/v2/file/download?path=%2Fpublic%2Fhome%2Ftest%2FBASE%2Fluan.pdf' \
--header 'Content-Type: application/json' \
--header 'token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wdXRlVXNlciI6InNsdXJtdGVzdCIsImFjY291bnRTdGF0dXMiOiJUcmlhbCIsImNyZWF0b3IiOiJhYyIsInJvbGUiOiIxIiwiZXhwaXJlVGltZSI6IjE2ODU2MDAyMjU2MTUiLCJjbHVzdGVySWQiOiIxMTExMiIsImludm9rZXIiOiI2MDQ4Y2U3YmExNWMyYWYyZThjZWMxMjk5MWVjMTNjZiIsInVzZXIiOiJzbHVybXRlc3QiLCJ1c2VySWQiOiIxMTY1NTA0ODU0MSJ9.iLCKJ8PnDDK0_SA2NPYm1WozUG8D5ojwFqFhwaJCDc8'
"""
