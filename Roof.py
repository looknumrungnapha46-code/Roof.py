# app.py
import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Hip Roof Calculator", layout="centered")

st.title("🏠 โปรแกรมคำนวณหลังคาทรงปั้นหยา (Hip Roof)")

# ------------------------
# 📥 Input
# ------------------------
st.header("📐 กรอกข้อมูล")

length = st.number_input("ความยาวอาคาร (m)", value=12.0)
width = st.number_input("ความกว้างอาคาร (m)", value=8.0)
height = st.number_input("ความสูงสันหลังคา (m)", value=3.0)
overhang = st.number_input("ชายคายื่น (m)", value=0.5)
waste = st.slider("เผื่อเศษวัสดุ (%)", 0, 30, 10)

# ------------------------
# 🧮 Calculation
# ------------------------
def calculate_hip_roof(L, W, H, e, waste_factor):
    L_total = L + 2 * e
    W_total = W + 2 * e

    # ความยาวเอียง
    slope_width = math.sqrt((W_total / 2)**2 + H**2)
    slope_length = math.sqrt((L_total / 2)**2 + H**2)

    # ความยาวสันหลังคา
    ridge = L_total - W_total if L_total > W_total else 0

    # พื้นที่
    # ด้านยาว (trapezoid)
    area_trap = 2 * ((L_total + ridge) / 2 * slope_width)

    # ด้านสั้น (triangle)
    area_tri = 2 * (0.5 * W_total * slope_length)

    total_area = area_trap + area_tri
    total_with_waste = total_area * (1 + waste_factor)

    # มุม
    pitch_angle = math.degrees(math.atan(H / (W_total / 2)))

    return {
        "L_total": L_total,
        "W_total": W_total,
        "slope_width": slope_width,
        "slope_length": slope_length,
        "ridge": ridge,
        "area_trap": area_trap,
        "area_tri": area_tri,
        "total_area": total_area,
        "total_with_waste": total_with_waste,
        "pitch_angle": pitch_angle
    }

# ------------------------
# ▶️ Run
# ------------------------
if st.button("คำนวณ"):
    result = calculate_hip_roof(length, width, height, overhang, waste / 100)

    st.header("📊 ผลลัพธ์")

    st.subheader("🔹 ข้อมูลเรขาคณิต")
    st.write(f"ความยาวรวม: {result['L_total']:.2f} m")
    st.write(f"ความกว้างรวม: {result['W_total']:.2f} m")
    st.write(f"ความยาวสันหลังคา: {result['ridge']:.2f} m")

    st.subheader("📐 ความยาวเอียง")
    st.write(f"ด้านกว้าง: {result['slope_width']:.2f} m")
    st.write(f"ด้านยาว: {result['slope_length']:.2f} m")

    st.subheader("📏 พื้นที่หลังคา")
    data = {
        "ประเภท": ["ด้านยาว (Trapezoid)", "ด้านสั้น (Triangle)", "รวม"],
        "พื้นที่ (m²)": [
            result["area_trap"],
            result["area_tri"],
            result["total_area"]
        ]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    st.success(f"พื้นที่รวม (เผื่อเศษ): {result['total_with_waste']:.2f} m²")

    st.subheader("📐 มุมหลังคา")
    st.write(f"{result['pitch_angle']:.2f}°")

    # ------------------------
    # 📈 Visualization
    # ------------------------
    st.subheader("📊 เปรียบเทียบพื้นที่")
    chart_df = pd.DataFrame({
        "ประเภท": ["Trapezoid", "Triangle"],
        "พื้นที่": [result["area_trap"], result["area_tri"]]
    })
    st.bar_chart(chart_df.set_index("ประเภท"))
