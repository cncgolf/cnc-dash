import streamlit as st
import pandas as pd

st.set_page_config(page_title='Clubs n Covers Outreach Tracker', layout='wide')

st.title('🏌️ Clubs n Covers Golf Course Outreach Tracker')

# Google Sheet public CSV URL would be placed here
sheet_url = st.secrets["sheet_url"]
df = pd.read_csv(sheet_url)

# Sidebar Filters
status_filter = st.sidebar.selectbox('Filter by Status', ['All'] + sorted(df['Status'].unique().tolist()))
follow_up_due = st.sidebar.checkbox('Show Only Follow-Ups Due')

# Apply Filters
if status_filter != 'All':
    df = df[df['Status'] == status_filter]
if follow_up_due:
    df['Follow Up Date'] = pd.to_datetime(df['Follow Up Date'], errors='coerce')
    df = df[df['Follow Up Date'] <= pd.Timestamp.today()]

# Display
st.dataframe(df)

# Notes
st.markdown("""---
Developed for Clubs n Covers Golf
""")
