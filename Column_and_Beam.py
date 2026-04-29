# app.py
import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="ACI 318 RC Design", layout="wide")

st.title("🏗️ RC Design (ACI 318 / มยผ.)")

# -----------------------
# MATERIAL
# -----------------------
st.sidebar.header("Material")
fc = st.sidebar.number_input("fc' (MPa)", value=28.0)
fy = st.sidebar.number_input("fy (MPa)", value=420.0)

# -----------------------
# LOAD
# -----------------------
st.sidebar.header("Load")
D = st.sidebar.number_input("Dead Load (kN/m)", value=5.0)
L = st.sidebar.number_input("Live Load (kN/m)", value=3.0)

# Factored load
wu = 1.2 * D + 1.6 * L

# -----------------------
# BEAM DESIGN
# -----------------------
st.header("📏 Beam Design")

L_beam = st.number_input("Span (m)", value=5.0)
b = st.number_input("b (mm)", value=250.0)
d = st.number_input("d (mm)", value=450.0)

if st.button("ออกแบบคาน"):
    # Moment
    Mu = wu * L_beam**2 / 8  # kN-m
    Mu_Nmm = Mu * 1e6

    phi = 0.9

    # Solve As iteratively
    As = 100  # initial guess
    for _ in range(50):
        a = (As * fy) / (0.85 * fc * b)
        Mn = As * fy * (d - a/2)
        phiMn = phi * Mn

        As = As * (Mu_Nmm / phiMn)

    # Shear
    Vu = wu * L_beam / 2  # kN
    Vc = 0.17 * math.sqrt(fc) * b * d / 1000  # kN

    st.subheader("📊 Beam Results")
    st.write(f"Mu = {Mu:.2f} kN·m")
    st.write(f"As required = {As:.2f} mm²")

    if Vu > Vc:
        st.warning("❗ ต้องออกแบบเหล็กปลอก (Shear reinforcement required)")
    else:
        st.success("✔ Shear OK")

# -----------------------
# COLUMN DESIGN
# -----------------------
st.header("🏢 Column Design")

Pu = st.number_input("Pu (kN)", value=1200.0)
Ag = st.number_input("Ag (mm²)", value=400*400)

if st.button("ออกแบบเสา"):
    phi = 0.65

    Pu_N = Pu * 1000

    # Solve As
    numerator = Pu_N/phi - 0.85*fc*Ag
    denominator = fy - 0.85*fc

    As = numerator / denominator

    # ACI min/max steel
    As_min = 0.01 * Ag
    As_max = 0.08 * Ag

    As_use = max(As, As_min)

    st.subheader("📊 Column Results")
    st.write(f"As calc = {As:.2f} mm²")
    st.write(f"As min = {As_min:.2f} mm²")
    st.write(f"As max = {As_max:.2f} mm²")

    if As_use > As_max:
        st.error("❌ หน้าตัดเล็กเกินไป ต้องเพิ่มขนาดเสา")
    else:
        st.success(f"✔ ใช้ As = {As_use:.2f} mm²")
