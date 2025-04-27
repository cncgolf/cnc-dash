import streamlit as st
import pandas as pd

# --- SIMPLE PASSWORD PROTECTION ---
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect. Try again.")
        return False
    else:
        return True

if not check_password():
    st.stop()
# --- END OF PASSWORD PROTECTION ---

# Main app starts here
st.set_page_config(page_title='Clubs n Covers Outreach Tracker', layout='wide')
st.title('🏌️ Clubs n Covers Golf Course Outreach Tracker')

# Load data
sheet_url = st.secrets["sheet_url"]
df = pd.read_csv(sheet_url)

# Sidebar Filters
status_filter = st.sidebar.selectbox('Filter by Status', ['All'] + sorted(df['Status'].dropna().unique()))
follow_up_due = st.sidebar.checkbox('Show Only Follow-Ups Due')

# Apply Filters
if status_filter != 'All':
    df = df[df['Status'] == status_filter]
if follow_up_due:
    df['Follow Up Date'] = pd.to_datetime(df['Follow Up Date'], errors='coerce')
    df = df[df['Follow Up Date'] <= pd.Timestamp.today()]

# Correct columns matching the new Google Sheet
expected_cols = ["Course Name", "Phone", "Notes", "Follow Up Date", "Website Address"]
available_cols = [col for col in expected_cols if col in df.columns]

st.dataframe(df[available_cols], use_container_width=True)

st.markdown("---")
st.caption("Developed for Clubs n Covers Golf")
