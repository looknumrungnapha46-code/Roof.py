import math

class HipRoofCalculator:
    def __init__(self, length, width, height, overhang=0.0, waste_factor=0.1):
        """
        length = ความยาวอาคาร (m)
        width = ความกว้างอาคาร (m)
        height = ความสูงสันหลังคา (m)
        overhang = ชายคายื่น (m)
        waste_factor = เผื่อเศษวัสดุ (เช่น 0.1 = 10%)
        """
        self.L = length + 2 * overhang
        self.W = width + 2 * overhang
        self.H = height
        self.waste = waste_factor

    def slope_length_width(self):
        """ความยาวเอียงด้านกว้าง"""
        return math.sqrt((self.W / 2)**2 + self.H**2)

    def slope_length_length(self):
        """ความยาวเอียงด้านยาว"""
        return math.sqrt((self.L / 2)**2 + self.H**2)

    def area_trapezoid_sides(self):
        """พื้นที่ด้านยาว (2 ด้าน)"""
        slope = self.slope_length_width()
        ridge_length = self.L - self.W  # สันหลังคา

        area_one_side = (self.L + ridge_length) / 2 * slope
        return 2 * area_one_side

    def area_triangle_sides(self):
        """พื้นที่ด้านสั้น (2 ด้าน)"""
        slope = self.slope_length_length()
        area_one_side = 0.5 * self.W * slope
        return 2 * area_one_side

    def total_area(self):
        """พื้นที่รวม"""
        return self.area_trapezoid_sides() + self.area_triangle_sides()

    def total_area_with_waste(self):
        """พื้นที่รวม + เผื่อวัสดุ"""
        return self.total_area() * (1 + self.waste)

    def roof_pitch_angle(self):
        """มุมเอียงหลังคา (องศา)"""
        return math.degrees(math.atan(self.H / (self.W / 2)))

    def summary(self):
        return {
            "พื้นที่ด้านยาว": self.area_trapezoid_sides(),
            "พื้นที่ด้านสั้น": self.area_triangle_sides(),
            "พื้นที่รวม": self.total_area(),
            "พื้นที่รวมเผื่อเศษ": self.total_area_with_waste(),
            "มุมหลังคา (deg)": self.roof_pitch_angle()
        }


# 🔹 ตัวอย่างใช้งาน
roof = HipRoofCalculator(
    length=12,   # m
    width=8,     # m
    height=3,    # m
    overhang=0.5,
    waste_factor=0.1
)

result = roof.summary()

for k, v in result.items():
    print(f"{k}: {v:.2f}")
