import streamlit as st
from supabase import create_client
from datetime import datetime

st.set_page_config(page_title="Harry Group Research Hub", layout="centered")
SUPABASE_URL = "https://ikzhysqlfcaaxwrvaoqm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlremh5c3FsZmNhYXh3cnZhb3FtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3MzA1MjksImV4cCI6MjEwODMwNjUyOX0.L19CUqSCNe--RQS_kwftErj0lIADdyHMcM_B2GvDQZk"
BUCKET = "research"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.title("Harry Group - Login")
    pwd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pwd == "harry123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

st.title("Harry Group Research Hub - Permanent")
names = ["Harrison","Amudavi","Makena","Cameraman","Gideon","Ishmael","John mark","Mjshakers","MrMan","Kinara"]
selected_name = st.selectbox("Select your name", names)
title = st.text_input("Research Title / Topic")
file = st.file_uploader("Upload ANY file")

if st.button("Upload", type="primary"):
    if title and file:
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{selected_name}_{file.name}"
        supabase.storage.from_(BUCKET).upload(filename, file.getvalue())
        st.success(f"Permanent upload: {file.name}!")
        st.balloons()
    else:
        st.warning("Add Title and File")

st.divider()
st.subheader("All Uploads - Permanent")
try:
    files = supabase.storage.from_(BUCKET).list()
    if files:
        st.write(f"All Uploads ({len(files)})")
        for f in reversed(files):
            fname = f['name']
            url = supabase.storage.from_(BUCKET).get_public_url(fname)
            st.write(f"📄 {fname}")
            st.link_button(f"Download {fname}", url)
    else:
        st.info("No uploads yet")
except Exception as e:
    st.error(f"Make bucket 'research' Public in Supabase Storage. Error: {e}")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
