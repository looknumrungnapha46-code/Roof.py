import math

def roof_area(length, width, height):
    """
    length = ความยาวบ้าน (เมตร)
    width = ความกว้างบ้าน (เมตร)
    height = ความสูงจากชายคาถึงสันหลังคา (เมตร)
    """

    half_width = width / 2

    # คำนวณความยาวด้านเอียง
    slope_length = math.sqrt(half_width**2 + height**2)

    # พื้นที่หลังคา (2 ด้าน)
    area = 2 * (length * slope_length)

    return area


# ตัวอย่างการใช้งาน
length = 10  # เมตร
width = 8    # เมตร
height = 3   # เมตร

area = roof_area(length, width, height)
print(f"พื้นที่หลังคา = {area:.2f} ตารางเมตร")
