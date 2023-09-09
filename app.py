from MISW_EXP_1_VALIDADOR import create_app
from flask_restful import Resource, Api
from flask import Flask, request
from random import random, randint
import requests
from celery import Celery

celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)


@celery_app.task(name='log.registrar')
def enviar_log(datos_log):
    pass


with app.app_context():
    for i in range(5000):
        operand_1 = randint(1, 10)
        operand_2 = randint(1, 10)
        query_result = operand_1 + operand_2
        if random() < 0.5:
            query_result = randint(1, 20)

        res1 = requests.get(
            f'http://127.0.0.1:5000/calificar?operand_1={operand_1}&operand_2={operand_2}&query_result={query_result}')

        data1 = res1.json().get('correct_answer')

        res2 = requests.get(
            f'http://127.0.0.1:5001/calificar?operand_1={operand_1}&operand_2={operand_2}&query_result={query_result}')

        data2 = res2.json().get('correct_answer')

        res3 = requests.get(
            f'http://127.0.0.1:5002/calificar?operand_1={operand_1}&operand_2={operand_2}&query_result={query_result}')

        data3 = res3.json().get('correct_answer')
        # print(f"{operand_1}+{operand_2}={query_result}: {data}")

        unavailable = 'None'
        if data1 == data2 == data3:
            unavailable = 'None'
        elif data1 == data2:
            unavailable = 3
        elif data2 == data3:
            unavailable = 1
        else:
            unavailable = 2

        datos = {'operand_1': operand_1, 'operand_2': operand_2, 'query_result': query_result, 'server_1_response': data1,
                 'server_2_response': data2, 'server_3_response': data3, 'unavailable_server': unavailable}
        args = (datos,)
        enviar_log.apply_async(args)
