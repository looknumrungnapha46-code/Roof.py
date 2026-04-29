# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calorie Calculator", layout="centered")

st.title("🔥 โปรแกรมคำนวณแคลอรี่เพื่อลดน้ำหนัก")

# -------------------------
# 📥 USER INPUT
# -------------------------
st.header("👤 ข้อมูลร่างกาย")

gender = st.selectbox("เพศ", ["ชาย", "หญิง"])
age = st.number_input("อายุ (ปี)", 10, 100, 25)
weight = st.number_input("น้ำหนัก (kg)", 30.0, 200.0, 70.0)
height = st.number_input("ส่วนสูง (cm)", 120.0, 220.0, 170.0)

activity = st.selectbox(
    "ระดับกิจกรรม",
    {
        "นั่งทำงาน": 1.2,
        "ออกกำลังกายเล็กน้อย": 1.375,
        "ออกกำลังกายปานกลาง": 1.55,
        "ออกกำลังกายหนัก": 1.725,
        "นักกีฬา": 1.9
    }
)

activity_factor = activity

# -------------------------
# 🍽️ FOOD INPUT
# -------------------------
st.header("🍽️ อาหารที่รับประทาน")

food_list = []

num_foods = st.number_input("จำนวนรายการอาหาร", 1, 20, 3)

for i in range(num_foods):
    st.subheader(f"รายการที่ {i+1}")
    col1, col2 = st.columns(2)

    with col1:
        food_name = st.text_input(f"ชื่ออาหาร {i+1}", key=f"name{i}")
    with col2:
        calories = st.number_input(f"แคลอรี่ (kcal)", 0.0, 2000.0, key=f"cal{i}")

    food_list.append({"อาหาร": food_name, "แคลอรี่": calories})

# -------------------------
# 🧮 CALCULATION
# -------------------------
def calculate_bmr(gender, weight, height, age):
    if gender == "ชาย":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

if st.button("คำนวณ"):
    # BMR
    bmr = calculate_bmr(gender, weight, height, age)

    # TDEE
    tdee = bmr * activity_factor

    # Intake
    df = pd.DataFrame(food_list)
    total_intake = df["แคลอรี่"].sum()

    # Deficit
    deficit = tdee - total_intake

    # -------------------------
    # 📊 OUTPUT
    # -------------------------
    st.header("📊 ผลลัพธ์")

    st.subheader("🔥 พลังงานร่างกาย")
    st.write(f"BMR: {bmr:.2f} kcal/day")
    st.write(f"TDEE: {tdee:.2f} kcal/day")

    st.subheader("🍽️ พลังงานที่รับเข้า")
    st.dataframe(df, use_container_width=True)
    st.success(f"รวม: {total_intake:.2f} kcal")

    st.subheader("⚖️ วิเคราะห์การลดน้ำหนัก")

    if deficit > 0:
        st.success(f"คุณขาดดุลพลังงาน: {deficit:.2f} kcal 🎉")
    else:
        st.error(f"คุณเกินพลังงาน: {-deficit:.2f} kcal ⚠️")

    # -------------------------
    # 🎯 Recommendation
    # -------------------------
    st.subheader("🎯 คำแนะนำ")

    target_deficit = 500

    if deficit < target_deficit:
        st.warning("ควรลดอาหารหรือเพิ่มการออกกำลังกาย")
    else:
        st.success("อยู่ในช่วงลดน้ำหนักที่ดี")

    # -------------------------
    # 📈 Chart
    # -------------------------
    chart_df = pd.DataFrame({
        "ประเภท": ["TDEE", "Intake"],
        "ค่า": [tdee, total_intake]
    })
    st.bar_chart(chart_df.set_index("ประเภท"))
