import datetime
import adafruit_dht 
import board
import smtplib
import sys
from email.message import EmailMessage
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from datetime import datetime
import pulseio

# DHT22 온습도 센서 초기화
dhtDevice = adafruit_dht.DHT22(board.D4)

# 현재 시간 설정
now = datetime.now()
current_time = now.strftime('%y-%m-%d %H:%M')

# 온도와 습도 측정
temp_c = dhtDevice.temperature
humidity = dhtDevice.humidity

# 온도와 습도 출력
print("Date: {} Temp: {:.1f} C  Humidity:{}%".format(current_time, temp_c, humidity))

# Gmail SMTP 서버 설정
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# 이메일 로그인 정보 설정
EMAIL_ADDR = 'jjorsae@gmail.com'
EMAIL_PASSWORD = 'eajt grfn tsso vmoj'

# Gmail SMTP 서버에 로그인
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

# 온도가 3도 미만 또는 32도 초과일 때 이메일 발송
if temp_c < 3 or temp_c > 32:
    message = EmailMessage()
    message.set_content('Date:{} Temp:{}C Humidity:{}%'.format(current_time, temp_c, humidity))
    message["subject"] = "서버실온도이상 Temp:{}C Humidity{}%".format(temp_c, humidity)
    message["From"] = 'thchoi@dsmbio.com'
    message["To"] = 'thchoi@dsmbio.com', 'ssbyun@dsmbio.com'
    smtp.send_message(message)
    smtp.quit()

# 온도가 40도를 초과할 때 SMS 발송
if temp_c > 40:
    # CoolSMS API 키 및 번호 설정
    api_key = "NCSGWRCQ0RKS6GC8"
    api_secret = "2GTMZOZ4ESQZAUVMM322SVYL7DEU7O7S"
    sms_to = '01051539372,01049501084'
    sms_from = '01051539372'
    
    # PulseIn 객체 생성 및 초기화
    pin = board.D4
    pulse_in = pulseio.PulseIn(pin)
    
    try:
        sms_text = '서버실온도이상 Date: {} Temp:{}C Humidity{}%'.format(current_time, temp_c, humidity)
        params = {
            'type': 'sms',
            'to': sms_to,
            'from': sms_from,
            'text': sms_text,
        }
        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])
        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
            sys.exit()

    finally:
        # PulseIn 객체 해제
        pulse_in.deinit()

# DHT22 센서 종료
dhtDevice.exit()
