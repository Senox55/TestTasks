import requests

headers = {
    'X-Yandex-API-Key': 'your_key'
}
respons = requests.get('https://api.weather.yandex.ru/v2/forecast?lat=52.37125&lon=4.89388', headers=headers)

if respons.status_code == 200:
    print(respons.json())
else:
    print(f"Ошибка {respons.status_code}, {respons.text}")