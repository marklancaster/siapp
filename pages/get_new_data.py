import streamlit as st
from datetime import datetime, date
import requests
from pymongo.errors import BulkWriteError
from pymongo import AsyncMongoClient, MongoClient
from utils.constants import *
from beanie import init_beanie
from models.training_package import TrainingPackage
import asyncio


async def fetch_training_packages():
    tps = []
    mongodbclient = AsyncMongoClient(MONGODB_CONNECTION_STRING)
    await init_beanie(database=mongodbclient.tga, document_models=[TrainingPackage])
    for code in TRAINING_PACKAGES:
        url = BASE_URL + code
        r = requests.get(url)
        if r.status_code == 200:
            tp = TrainingPackage(**r.json())
            training_package = await TrainingPackage.find_one(TrainingPackage.code == code)
            if training_package.releases == tp.releases:
                st.write(f"{code} up to date")
            else:
                st.write(f"{code} needs updating, however, this has not been implemented yet. Sorry.")
                tps.append(tp)
    return tps

st.title("Check for new Data")
st.write("Please wait while we check for new data...")




tps = asyncio.run(fetch_training_packages())
if tps:
    pass
    #asyncio.run(check_data_exists(data))
    #st.write(data)