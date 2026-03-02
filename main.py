import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="DFMEA Configurator", layout="wide")

# ======================================================
# 🔐 USER LOGIN (WINDOWS USERNAME INPUT)
# ======================================================

if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    st.title("🔐 DFMEA Login")

    username_input = st.text_input(
        "Enter your Windows Username (example: ext.swadhwa)"
    )

    if st.button("Login"):
        if username_input.strip():
            st.session_state.username = username_input.strip()
            st.rerun()
        else:
            st.warning("Please enter a valid username.")

    st.stop()

# ======================================================
# 🔹 SIDEBAR USER INFO
# ======================================================

st.sidebar.success(f"Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.username = None
    st.rerun()

# ======================================================
# 🔹 BUILD HARD-CODED WINDOWS PATH
# ======================================================

username = st.session_state.username

base_path = rf"C:\Users\{username}\Vibracoustic\DFMEA_ESR - General\01_Project Handling\Bench mark parts\Wuxi Benchmarking"

file_path = os.path.join(base_path, "data.xlsx")
print(file_path)
files_folder = os.path.join(base_path, "Bushing")

# ======================================================
# 🔹 VALIDATE PATH
# ======================================================

if not os.path.exists(base_path):
    st.error(f"Base path not found:\n{base_path}")
    st.stop()

if not os.path.exists(file_path):
    st.error(f"Config file not found:\n{file_path}")
    st.stop()

# ======================================================
# 🔹 LOAD CONFIG FILE
# ======================================================

df = pd.read_excel(file_path).fillna("None")

# ======================================================
# 🔧 CONFIGURATOR
# ======================================================

st.title("🔧 DFMEA Smart Configurator")

st.sidebar.header("Configuration")

# -----------------------------
# TYPE (RADIO)
# -----------------------------
type_option = st.sidebar.radio(
    "Select Type",
    sorted(df["Type"].unique())
)

filtered_df = df[df["Type"] == type_option]

# -----------------------------
# SPECIAL BUSH
# -----------------------------
if type_option == "Special bush":

    speciality = st.sidebar.radio(
        "Select Speciality",
        sorted(filtered_df["Speciality"].unique())
    )
    filtered_df = filtered_df[filtered_df["Speciality"] == speciality]

# -----------------------------
# NON-HOUSING TYPES
# -----------------------------
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

# -----------------------------
# HOUSING TYPE
# -----------------------------
if type_option == "Bush with Housing":

    housing = st.sidebar.radio(
        "Select Housing",
        sorted(filtered_df["Housing"].unique())
    )
    filtered_df = filtered_df[filtered_df["Housing"] == housing]

# ======================================================
# 📥 RESULT SECTION
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
        st.error(f"File not found:\n{full_file_path}")

elif len(filtered_df) > 1:
    st.warning("Multiple matches found. Refine selection.")

else:
    st.error("No matching configuration found.")