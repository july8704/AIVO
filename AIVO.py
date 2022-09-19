import calendar
import os
import datetime
import requests
from typing import Optional, Dict, Union
from requests import Response
import json
from typing import List
import pandas as pd
import io

AIVO_USER = os.environ.get("AIVO_USER")
AIVO_PASSWORD = os.environ.get("AIVO_PASSWORD")
AIVO_X_TOKEN_WEB = os.environ.get("AIVO_X_TOKEN_WEB")
AIVO_X_TOKEN_CONTADOR = os.environ.get("AIVO_X_TOKEN_CONTADOR")
AIVO_X_TOKEN_FE = os.environ.get("AIVO_X_TOKEN_FE")

class Aivo:
    def __init__(self):

        self.email = AIVO_USER
        self.password = AIVO_PASSWORD
        self.content_type = 'application/json'
        self.x_token_canalWeb = AIVO_X_TOKEN_WEB
        self.base_url = "https://api.aivo.co/api/v1"
        self.AutorizationBareer = f"{self.base_url}/user/login-simple"
        self.chatConversations  = f"{self.base_url}/stats/conversation/complete-list"
    def get_autorization_bearer(self) -> Response:
        url: str = f"{self.AutorizationBareer}"
        credencial = dict(email=self.email, password=self.password)
        payload = json.dumps(credencial)
        headers = {
            'Content-Type': self.content_type
        }
        r: Response = requests.request("POST", url,
                                   headers=headers,
                                   data=payload)
        autorization: List[dict] = r.json()
        bear = autorization.get('Authorization')

        return bear

    def get_web_chatConversations(self, start_date, end_date) -> Response:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        print(start_date)
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        url: str = f"{self.chatConversations}/export"
        query_params: Dict[str, Union[int, str]] = {"from": start_date, "to": end_date}
        Autorization = self.get_autorization_bearer()
        payload = {}
        headers = {
            'X-Token': AIVO_X_TOKEN_WEB,
            'Authorization': Autorization,
            'Content-Type': self.content_type
        }
        r: Response = requests.request("GET", url,
                                   headers=headers,
                                   data=payload,
                                    params=query_params)
        print(r)
        data = r.text
        print(data)

        return data

    def get_contador_chatConversations(self, start_date, end_date) -> Response:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        print(start_date)
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        url: str = f"{self.chatConversations}/export"
        query_params: Dict[str, Union[int, str]] = {"from": start_date, "to": end_date}
        Autorization = self.get_autorization_bearer()
        payload = {}
        headers = {
            'X-Token': AIVO_X_TOKEN_CONTADOR,
            'Authorization': Autorization,
            'Content-Type': self.content_type
        }
        r: Response = requests.request("GET", url,
                                   headers=headers,
                                   data=payload,
                                    params=query_params)
        print(r)
        data = r.text
        print(data)

        return data

    def get_fe_chatConversations(self, año, mes_number) -> Response:
        start_date = datetime.datetime.strptime(str(año)+"-"+str(mes_number)+"-"+"01", '%Y-%m-%d')
        last_day = calendar.monthrange(2022, mes_number)[1]
        end_date = datetime.datetime.strptime(str(año)+"-"+str(mes_number)+"-"+str(last_day)+" 23:59:59", '%Y-%m-%d %H:%M:%S')
        df_aivo = pd.DataFrame()

        for x in range  (5,30,5):
            end_date = datetime.datetime.strptime(str(año)+"-"+str(mes_number)+"-"+str(x)+" 23:59:59", '%Y-%m-%d %H:%M:%S')
            print(start_date)
            print(end_date)
            print(x)
            print('------------------------------------------------')
            url: str = f"{self.chatConversations}/export"
            query_params: Dict[str, Union[int, str]] = {"from": start_date, "to": end_date}
            Autorization = self.get_autorization_bearer()
            payload = {}
            headers = {
                'X-Token': AIVO_X_TOKEN_FE,
                'Authorization': Autorization,
                'Content-Type': self.content_type
            }
            r: Response = requests.request("GET", url,
                                       headers=headers,
                                       data=payload,
                                        params=query_params)
            data = r.text
            buffer = io.StringIO(data)
            df = pd.read_csv(filepath_or_buffer=buffer,
                             usecols=['Id', 'Fecha', 'Canal', 'Condición', 'Media', 'Nombre de usuario',
                                      'Email de usuario', 'Hash de usuario', 'Parámetros de usuario',
                                      'Nombre de la intención', 'Pregunta', 'Respuesta', 'Feedback',
                                      'Resolución', 'Tag', 'Host', 'País', 'Ciudad', 'Dispositivo', 'Path',
                                      'Tipo de encuesta', 'Valor', 'Encuesta', 'Pregunta encuesta',
                                      'Respuesta encuesta'])

            df_aivo = pd.concat([df, df_aivo])
            ## Actualizamos fechas
            start_date = datetime.datetime.strptime(str(año)+"-"+str(mes_number)+"-"+str(x+1), '%Y-%m-%d')
        else:
            start_date = datetime.datetime.strptime(str(año) + "-" + str(mes_number) + "-" + str(26), '%Y-%m-%d')
            end_date = datetime.datetime.strptime(str(año) + "-" + str(mes_number) + "-" + str(last_day) + " 23:59:59",
                                                  '%Y-%m-%d %H:%M:%S')
            url: str = f"{self.chatConversations}/export"
            query_params: Dict[str, Union[int, str]] = {"from": start_date, "to": end_date}
            Autorization = self.get_autorization_bearer()
            payload = {}
            headers = {
                'X-Token': AIVO_X_TOKEN_FE,
                'Authorization': Autorization,
                'Content-Type': self.content_type
            }
            r: Response = requests.request("GET", url,
                                           headers=headers,
                                           data=payload,
                                           params=query_params)
            data = r.text
            buffer = io.StringIO(data)
            df = pd.read_csv(filepath_or_buffer=buffer,
                             usecols=['Id', 'Fecha', 'Canal', 'Condición', 'Media', 'Nombre de usuario',
                                      'Email de usuario', 'Hash de usuario', 'Parámetros de usuario',
                                      'Nombre de la intención', 'Pregunta', 'Respuesta', 'Feedback',
                                      'Resolución', 'Tag', 'Host', 'País', 'Ciudad', 'Dispositivo', 'Path',
                                      'Tipo de encuesta', 'Valor', 'Encuesta', 'Pregunta encuesta',
                                      'Respuesta encuesta'])
            df_aivo = pd.concat([df, df_aivo])
        return df_aivo
if __name__ == "__main__":
    main_aivo = Aivo()
    df = pd.DataFrame()
    df = main_aivo.get_fe_chatConversations(2022,9)
    df.to_excel('Sept_2022.xlsx')
    df

    """
    buffer = io.StringIO(data)
    df = pd.read_csv(filepath_or_buffer=buffer, usecols=['Id', 'Fecha', 'Canal', 'Condición', 'Media', 'Nombre de usuario',
       'Email de usuario', 'Hash de usuario', 'Parámetros de usuario',
       'Nombre de la intención', 'Pregunta', 'Respuesta', 'Feedback',
       'Resolución', 'Tag', 'Host', 'País', 'Ciudad', 'Dispositivo', 'Path',
       'Tipo de encuesta', 'Valor', 'Encuesta', 'Pregunta encuesta',
       'Respuesta encuesta'])

    print(df)    
    """