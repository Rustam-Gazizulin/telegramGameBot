import requests


# Функция расчета курса валюты
def convert_to_rub(currency: str, value: float) -> float | str:

    # Отправляем GET-запрос и сохраняем ответ в переменной response
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')

    # Если код ответа на запрос - 200, то обрабатываем полученные данные
    if response.status_code == 200:
        response = response.json()
        try:
            return round(((response['Valute'][currency.upper()]['Value']) * value), 2)
        except KeyError:

            return f'Такой валюты нет в базе'
    else:
        return f'Сервер не отвечает код ошибки {response.status_code}'


def get_list_valute() -> list:
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']
    list_valute = []
    for i in response:
        list_valute.append(i)
    return list_valute


