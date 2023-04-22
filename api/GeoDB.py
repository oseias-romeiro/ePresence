from requests import request
from os import getenv
from math import sqrt


URL = "https://wft-geo-db.p.rapidapi.com/v1/geo"
HEADERS = {
    'X-RapidAPI-Key': '926d16ce17mshf66b9c1208529cdp1713d6jsn534dc5f8e0aa', # getenv("RAPID_KEY")
    'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
}


def get_distance(coordA: tuple, coordB: tuple) -> float:
    return sqrt(pow(coordA[0]-coordB[0], 2) + pow(coordA[1]-coordB[1], 2))


def get_nearby_cities(lat, lon) -> dict:
    """
        Retorna dados da cidade mais próxima de uma coordenada dada
    """
    url = URL+f"/locations/{lat}{lon}/nearbyCities"
    params = {"radius": "100"}

    try:
        res = request("GET", url=url, headers=HEADERS, params=params)
        return res.json()["data"][0]
    except Exception as e:
        print(e.__str__())
        return ""


