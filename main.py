import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="DFMEA Configurator", layout="wide")

# ======================================================
# 🔹 DYNAMIC USER PATH
# ======================================================
username = os.environ["USERNAME"]

base_path = rf"C:\Users\{username}\Vibracoustic\DFMEA_ESR - General\01_Project Handling\Bench mark parts"
file_path = os.path.join(base_path, "data.xlsx")
files_folder = os.path.join(base_path, "Wuxi Benchmarking")

# ======================================================
# 🔹 LOAD CONFIG
# ======================================================
if not os.path.exists(file_path):
    st.error("Config file not found. Check OneDrive sync.")
    st.stop()

df = pd.read_excel(file_path).fillna("None")

st.title("🔧 DFMEA Smart Configurator")

st.sidebar.header("Configuration")

# ======================================================
# 🔹 TYPE (RADIO)
# ======================================================
type_option = st.sidebar.radio(
    "Select Type",
    sorted(df["Type"].unique())
)

filtered_df = df[df["Type"] == type_option]

# ======================================================
# 🔹 SPECIAL BUSH
# ======================================================
if type_option == "Special bush":

    speciality = st.sidebar.radio(
        "Select speciality",
        sorted(filtered_df["Speciality"].unique())
    )
    filtered_df = filtered_df[filtered_df["Speciality"] == speciality]

# ======================================================
# 🔹 ALL EXCEPT HOUSING
# ======================================================
if type_option != "Bush with Housing":

    mre = st.sidebar.radio(
        "Select MRE",
        sorted(filtered_df["MRE"].unique())
    )
    filtered_df = filtered_df[filtered_df["MRE"] == mre]

    inner = st.sidebar.radio(
        "Select Inner",
        sorted(filtered_df["Inner"].unique())
    )
    filtered_df = filtered_df[filtered_df["Inner"] == inner]

    outer = st.sidebar.radio(
        "Select Outer",
        sorted(filtered_df["Outer"].unique())
    )
    filtered_df = filtered_df[filtered_df["Outer"] == outer]

# ======================================================
# 🔹 HOUSING TYPE
# ======================================================
if type_option == "Bush with Housing":

    housing = st.sidebar.radio(
        "Select Housing",
        sorted(filtered_df["Housing"].unique())
    )
    filtered_df = filtered_df[filtered_df["Housing"] == housing]

# ======================================================
# 🔹 RESULT SECTION
# ======================================================
st.subheader("Result")

if len(filtered_df) == 1:

    row = filtered_df.iloc[0]
    file_name = row["FileURL"]
    full_file_path = os.path.join(files_folder, file_name)

    st.success(f"Matched Configuration: {file_name}")

    if os.path.exists(full_file_path):

        with open(full_file_path, "rb") as f:
            file_bytes = f.read()

        st.download_button(
            label="📥 Download DFMEA File",
            data=file_bytes,
            file_name=file_name,
            mime="application/octet-stream"
        )

    else:
        st.error("DFMEA file not found in files folder.")

elif len(filtered_df) > 1:
    st.warning("Multiple matches found. Refine selection.")

else:
    st.error("No matching configuration found.")