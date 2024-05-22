# SGGS-ANON 匿名曙光留言板


## 系統

#### *多模組設計*
 - api
 - frontend
 - moderation
 - static_files

#### *管理*
- 留言管理
- 回覆管理
- 使用者管理
- 管理員管理

#### *DB儲存的資料*
##### *使用者註冊時*
- 使用者名稱
- 電子郵件
- 密碼
- 註冊時間
- 最後登入時間
- 權限
- 帳號狀態
##### *留言時*
- 留言內容
- 留言時間
- 留言者
- 是否被管理員設定隱藏或標記

### 详细设计

- ##### 短信验证码接口实现

```python
import urllib.parse, urllib.request
import json

def send_sms_code(phone):
    '''
    函数功能：发送短信验证码（6位随机数字）
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''
    verify_code = str(random.randint(100000, 999999))

    try:
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile": phone,  # 接受短信的用户手机号码
            "tpl_id": "162901",  # 您申请的短信模板ID，根据实际情况修改
            "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
            "key": "替换成自己的APPKEY",  # 应用APPKEY(应用详细页查询)
        }
        params = urllib.parse.urlencode(params).encode()

        f = urllib.request.urlopen(url, params)
        content = f.read()
        res = json.loads(content)

        if res and res['error_code'] == 0:
            return verify_code
        else:
            return False
    except:
        return False
```

