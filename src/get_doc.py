import requests


def get_doc():

     response = requests.get("https://staging-mobi.mobiapp.cn:8443/static/files/API_V_2_0.yaml")

     return response.text
