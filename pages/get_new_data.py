import streamlit as st
from datetime import datetime, date
import requests
from pymongo.errors import BulkWriteError
from pymongo import AsyncMongoClient, MongoClient
from utils.constants import *
from beanie import init_beanie
from models.training_package import TrainingPackage
import asyncio
import json


async def fetch_training_packages():
    tps = []
    mongodbclient = AsyncMongoClient(MONGODB_CONNECTION_STRING)
    await init_beanie(database=mongodbclient.tga, document_models=[TrainingPackage])
    TRAINING_PACKAGES.sort()
    for code in TRAINING_PACKAGES:
        url = BASE_URL + code
        r = requests.get(url)
        if r.status_code == 200:
            tp = TrainingPackage(**r.json())
            st.write(f"Downloaded data for {tp.code}")
            tps.append(r.json())
            # training_package = await TrainingPackage.find_one(TrainingPackage.code == code)
            # if training_package.releases == tp.releases:
            #     st.write(f"{code} up to date")
            # else:
            #     await TrainingPackage.find_one_and_delete(TrainingPackage.code == code)
            #     await tp.insert()
            #     #st.write(tp)
            #     #st.write(f"{code} needs updating, however, this has not been implemented yet. Sorry.")
            #     st.write(f"{code} updated")
            #     #tps.append(tp)
    #st.download_button(label="Download data", data=json.dumps(tps), file_name="tga_info_json.txt")
    return tps

st.title("Check for new Data")
st.write("Please wait while we check for new data...")




tps = asyncio.run(fetch_training_packages())
if tps:
    pass
    #st.write(tps)
    st.download_button(label="Download data", data=json.dumps(tps), file_name=f"tga_info_json_{datetime.now().strftime('%Y%m%d')}.txt")
    #asyncio.run(check_data_exists(data))
    #st.write(data)