from fastapi import FastAPI
import pandas as pd
import json
import requests
from app.Employee_Search import Employee_Search
import os

es_obj=Employee_Search()
df_us,df_uk,merged_df=es_obj.load_csv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/api/employees/")
async def get_all_employees():
    #print("here here 2")
    return es_obj.get_all_employees(df_us,df_uk,merged_df)

@app.get("/api/employees/name={name}")
async def get_employee_data(name = None):
    try:
        keystring=requests.utils.unquote(name)
        keywords=keystring.split(' ')
        return es_obj.get_employee_data(keywords,df_us,df_uk,merged_df)
    except KeyError:
        print('Invalid name provided')





