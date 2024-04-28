# API introduction and usage of the sggs-anon API v1

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
    "content": "awab testing",
    "post_id": "PLSnHjOBlj",
    "pub_time": "2024-04-23 13:46",
    "replys_count": 1,
    "uname": "Cartman"
  },
  {
    "content": "Hello after reseting\r\nFrom the darkness.",
    "post_id": "dDcqemrBVm",
    "pub_time": "2024-04-19 14:14",
    "replys_count": 0,
    "uname": "Cartman"
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
