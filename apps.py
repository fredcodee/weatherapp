from bs4 import BeautifulSoup
import requests
import datetime
from time import sleep
from flask import Flask, render_template,request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@app.route("/home")
def home():
  url = "https://www.yahoo.com/news/weather/"
  weather = requests.get(url)
  soup = BeautifulSoup(weather.text, 'html.parser')


  city = soup.find_all("h1")[-1].text.strip()
  dateformat = datetime.datetime.now()
  time = dateformat.strftime("%X")
  day = dateformat.strftime("%A")
  localdate = dateformat.strftime("%x")
  date = day + " "+localdate
  description = soup.find("div", class_="My(2px)").find(
      "span", class_="description").text.strip()
  current_temperature = soup.find(
      "span", class_="Va(t)").text.strip()  # defult in f degree
  forecast_list = []


  def change_to_c(n):
    '''change from f degree to c degrees'''
    ff = 5/9
    _change = int(n)-32
    _change = ff * _change
    return(round(_change))


  up = change_to_c(current_temperature)


  def get_forecast():
    #more days
    list_tem = soup.find_all(attrs={'class': 'forecast-item'})
    for n in list_tem:
      _c = {}
      _c["day"] = n.find(attrs={'class': 'W(1/4)'}).span.text.strip()
      _h_t = n.find(attrs={'class': 'Ta(end)'}).find(
          attrs={'class': 'high'}).text.strip()
      _h = _h_t.split("°")
      _h.pop()
      _h = "".join(_h)
      _c["highest_tem"] = change_to_c(_h)
      _l_t = n.find(attrs={'class': 'Ta(end)'}).find(
          attrs={'class': 'low'}).text.strip()
      _l = _l_t.split("°")
      _l.pop()
      _l = "".join(_l)
      _c["lowest_tem"] = change_to_c(_l)
      forecast_list.append(_c)
      sleep(1)

  get_forecast()
  while len(forecast_list) > 5:
    forecast_list.pop()
  if description != "Thunderstorms":
    description = True
  else:
    description = False

  return(render_template('home.html', up=up, date=date, time=time, city= city, description=description, forecast_list = forecast_list))


@app.route("/cus", methods=["GET", "POST"])
def cus_location():
  pass

