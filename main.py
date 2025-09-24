import streamlit as st
import pandas as pd
from pymongo import MongoClient, DESCENDING

remoteclient = MongoClient(st.secrets["MONGODB"])
collection = remoteclient.tga.data3


st.set_page_config(layout="wide")

st.title("hi")



num_files = st.slider("How many files to get?", 10, 5000, 100)

@st.cache_data
def get_search(search_limit=100):
    st.write("getting latest files")
    search = collection.find({}).sort({'current_release': DESCENDING}).limit(num_files)
    last_files = list(search)
    return last_files

#if st.button("get more data"):
#    get_search(search_limit=num_files)

#num_files = 200
df = pd.DataFrame(get_search(search_limit=num_files))
columns_to_keep = ["code", "title", "type", "current_release"]

df_selected = df[columns_to_keep]

st.write(df_selected)

last_updated = collection.find().sort({'ts': DESCENDING}).limit(1)
st.write(f"Database last updated: {last_updated.next()['ts']}")