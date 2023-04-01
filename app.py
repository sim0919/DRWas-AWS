from flask import Flask
import requests
import pymysql
from datetime import datetime
import sys

db_path = sys.argv[1]
app = Flask(__name__)
db = pymysql.connect(host=db_path, port=3306, user='writeuser', passwd='Writeuser1!', db='dbdata', charset='utf8')

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/ping")
def ping():
    return "ok"

@app.route("/api/getInfo")
def getInfo() :

    cursor = db.cursor()
    sql = "select count(*) as cont from joindata"
    cursor.execute(sql)
    num = cursor.fetchall()[0][0]
    cursor.close()

    return {
        "userName" : "콩순이",
        "userBank" : "(주)콩순이",
        "user" : str(num)
    }

@app.route("/api/getUSDKRW")
def getUSDKRW() :
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange = requests.get(url, headers=headers).json()

    cursor = db.cursor()
    sql = "insert into joindata (price,time) values (%s, %s)"

    cursor.execute(sql, (str(exchange[0]['basePrice']),datetime.now()))


    db.commit()
    cursor.close()

    return { "exchange" : str(exchange[0]['basePrice']) }


@app.route("/api/test")
def getTest() :

    return "Test Message"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")