import streamlit as st
import pandas as pd
from pathlib import Path
from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.
client = bigquery.Client()

@st.cache_data
def load_data():
    query = """
    SELECT Final_Incident_Category, Priority, Dispatched_Time, Unit_On_Scene_TimeStamp
    FROM `sound-essence-442801-t6.cmpe_255_hw1_san_jose_fires.processed_fire_results`
    """
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

st.title("San Jose Fire Incident Data Analysis")

# Load the data
df = load_data()

# Question 1: Distribution of Incident Types
st.header("Distribution of Incident Types")

incident_counts = df['Final_Incident_Category'].value_counts()

fig, ax = plt.subplots(figsize=(12, 6))
incident_counts.plot(kind='bar', ax=ax)
plt.title('Distribution of Incident Types')
plt.xlabel('Incident Category')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig)

# Question 2: Response Times by Priority
st.header("Response Times by Priority")

df['Response_Time'] = (pd.to_datetime(df['Unit_On_Scene_TimeStamp']) - pd.to_datetime(df['Dispatched_Time'])).dt.total_seconds() / 60

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='Priority', y='Response_Time', data=df, ax=ax)
plt.title('Response Time by Priority')
plt.xlabel('Priority')
plt.ylabel('Response Time (minutes)')

st.pyplot(fig)