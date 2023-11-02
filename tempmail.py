#temp.py

import datetime
import adafruit_dht 
import board
import smtplib
import sys
from email.message import EmailMessage
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from datetime import datetime

dhtDevice = adafruit_dht.DHT22(board.D4)
now=datetime.now()
current_time=now.strftime('%y-%m-%d %H:%M')


temp_c=dhtDevice.temperature
humidity = dhtDevice.humidity

print("Date: {} Temp: {:.1f} C  Humidity:{}%".format(current_time,temp_c,humidity))

SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=465

smtp=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

EMAIL_ADDR='jjorsae@gmail.com'
EMAIL_PASSWORD='eajt grfn tsso vmoj'

smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)


if temp_c<3 or temp_c>32:
    message=EmailMessage()
    message.set_content('Date:{} Temp:{}C Humidity:{}%'.format(current_time,temp_c,humidity))
    message["subject"]="서버실온도이상 Temp:{}C Humidity{}%".format(temp_c,humidity)
    message["From"]='thchoi@dsmbio.com'
    message["To"]='thchoi@dsmbio.com','ssbyun@dsmbio.com'
    smtp.send_message(message)

    smtp.quit()
    

if temp_c>38:
    if __name__=="__main__":
        api_key="NCSGWRCQ0RKS6GC8"
        api_secret="L1FUITZUTSQEJ8QRZNOYA31IORNWY0DC"

        params=dict()
        params['type']='sms'
        params['to']='01051539372,01049501084'
        params['from']='01051539372'
        params['text']='서버실온도이상 Date: {} Temp:{}C Humidity{}%'.format(current_time,temp_c,humidity)

        cool=Message(api_key,api_secret)
        try:
            response=cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % reponse['error_list'])
        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
        sys.exit()



