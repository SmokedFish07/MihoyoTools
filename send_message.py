# 安装依赖 pip3 install requests html5lib bs4 schedule
import os
import requests

# 从测试号信息获取
appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
# 收信人ID即 用户列表中的微信号
openId = os.environ.get("OPEN_ID")
# 模板ID
template_id = os.environ.get("MESSAGE_ID")


def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token




def send_sign_success(access_token, status, message):
    # touser 就是 openID
    # template_id 就是模板ID
    # url 就是点击模板跳转的url
    # data就按这种格式写，time和text就是之前{{time.DATA}}中的那个time，value就是你要替换DATA的值

    import datetime
    now = datetime.datetime.now()
    time_str = now.strftime("%Y年%m月%d日 %H:%M:%S")

    body = {
        "touser": openId.strip(),
        "template_id": template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "time": {  # 模板中的变量名
                "value": time_str
            },
            "status": {  # 模板中的变量名
                "value": status
            },
            "remark": {  # 模板中的变量名
                "value": message
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    response = requests.post(url, json=body, timeout=30)
    response.raise_for_status()
    print(response.text)



def send_sign_report(status="签到完成", message=""):
    # 1.获取access_token
    access_token = get_access_token()
    if not access_token:
        raise RuntimeError("获取微信 access_token 失败")
    # 2. 发送签到信息
    send_sign_success(access_token, status, message)

if __name__ == '__main__':
    send_sign_report(
        status=os.environ.get("SIGN_STATUS", "签到完成"),
        message=os.environ.get("SIGN_MESSAGE", ""),
    )