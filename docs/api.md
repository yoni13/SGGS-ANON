# API introduction and usage of the sggs-ano API v1

## Introduction
We use https to access the API. The base URL is `/api/v1/`.

### Get Message Board data
#### Request
- Method: `GET`
- URL: `/mb_board/`
- Additional args: `?limit=10` (optional,interger) `?page=1` (optional,interger) `?reverse=1` (optional,ignored if not 1)

#### Response
- Status: `200 OK`
- Content: 
```json
[
    {
        "content": "Wellcome !",
        "post_id": "XRiFSDbRYC",
        "pub_time": "2024-02-08 20:39",
        "uname": "Cartman"
    },
    {
        "content": "Hellllllo \n testing",
        "post_id": "EXwxCXmvFx",
        "pub_time": "2024-02-08 20:58",
        "uname": "Cartman"
    },
    {
        "content": "這裡好酷，匿名自由~~",
        "post_id": "CmRijQSBhf",
        "pub_time": "2024-02-08 21:25",
        "uname": "Whale120"
    },
    {
        "content": "註冊的問題解決摟~可以註冊了！",
        "post_id": "EWJqhlejGQ",
        "pub_time": "2024-02-10 22:30",
        "uname": "Cartman"
    },
    {
        "content": "匿名寫好了",
        "post_id": "nPSuUUZrOIanonymous",
        "pub_time": "2024-02-11 21:52",
        "uname": "匿名"
    }
]
```


### Get Reply data
#### Request
- Method: `GET`
- URL: `/mb_replys/`
- Additional args: `?post_id`(required,str) `?limit=10` (optional,interger) `?page=1` (optional,interger) `?reverse=1` (optional,ignored if not 1)

#### Response
- Status: `200 OK`
- Content:
```json

{
    "post": {
        "content": "這裡好酷，匿名自由~~",
        "post_id": "CmRijQSBhf",
        "pub_time": "2024-02-08 21:25",
        "uname": "Whale120"
    },
    "replys": [
        {
            "content": "蝦啦",
            "pub_time": "2024-02-09 14:24",
            "uname": "Cartman"
        },
        {
            "content": "搞不好欸（",
            "pub_time": "2024-02-09 12:35",
            "uname": "Whale120"
        },
        {
            "content": "我就不信學校找得到這裡。",
            "pub_time": "2024-02-09 02:12",
            "uname": "Cartman"
        },
        {
            "content": "不要開兩個帳號，偶看到了",
            "pub_time": "2024-02-08 21:30",
            "uname": "Cartman"
        },
        {
            "content": "還能回覆欸",
            "pub_time": "2024-02-08 21:25",
            "uname": "Whale120"
        }
    ]
}
```