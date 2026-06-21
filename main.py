'''
(1) Phân tích lỗi (Code Review)

Câu 1 — Vì sao AttributeError: 'Warrior' object has no attribute 'name'?
Trong __init__ của Warrior, dòng duy nhất được thực thi là self.bonus_armor = bonus_armor. 
Không có dòng nào gán self.name, self.hp, self.attack_power cho đối tượng. Vì Python không 
tự động "thừa hưởng" giá trị thuộc tính chỉ vì có khai báo kế thừa class — kế thừa chỉ cho 
phép class con truy cập các method/attribute định nghĩa ở class cha, còn việc gán giá trị 
instance attribute (self.x = ...) phải được gọi rõ ràng. Lập trình viên thiếu dòng gọi 
super().__init__(name, hp, attack_power) (hoặc tương đương) bên trong __init__ của Warrior, 
nên Character.__init__ không bao giờ được chạy, dẫn đến đối tượng w1 không hề có thuộc tính name.

Câu 2 — Cách gọi __init__ của Character mà không dùng super():
Gọi trực tiếp theo class cha và truyền self thủ công:
pythonCharacter.__init__(self, name, hp, attack_power)
Cách này hoạt động vì về bản chất __init__ chỉ là một hàm thường gắn vào class; 
gọi qua tên class và truyền self tương đương với cách super() làm ngầm. 
Tuy nhiên không khuyến khích vì với đa kế thừa (multiple inheritance), 
cách này dễ gây trùng lặp lệnh gọi hoặc bỏ sót class trong MRO (Method Resolution Order), 
còn super() tự động xử lý đúng thứ tự đó.

Câu 3 — Lỗi tiếp theo tại if w1 > w2:
Console sẽ in:
TypeError: '>' not supported between instances of 'Warrior' and 'Warrior'
Dấu > vô tác dụng vì Python không có quy tắc mặc định để so sánh hai object 
do người dùng tự định nghĩa (Warrior là kiểu tùy chỉnh, không phải số hay chuỗi 
có sẵn quy tắc so sánh). Khi gặp a > b, Python tìm method __gt__ trong class của a; 
nếu class đó không định nghĩa, nó báo TypeError ngay vì không biết "lớn hơn" nghĩa là gì đối với hai chiến binh.

Câu 4 — Dunder method cần khai báo
Cần khai báo __gt__(self, other). Hàm này nhận 2 tham số: 
self (đối tượng bên trái dấu >) và other (đối tượng bên phải).
Bên trong, ta định nghĩa tiêu chí so sánh là self.get_total_power() > other.get_total_power().

'''

# (2) Sửa lỗi (Refactoring)

class Character:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power


# Lớp con: Chiến binh cận chiến
class Warrior(Character):
    def __init__(self, name, hp, attack_power, bonus_armor):
        # Gọi hàm khởi tạo của lớp cha để kế thừa name, hp, attack_power
        super().__init__(name, hp, attack_power)
        self.bonus_armor = bonus_armor

    def get_total_power(self):
        return self.attack_power + self.bonus_armor

    def __gt__(self, other):
        # Nạp chồng toán tử > dựa trên tổng sức mạnh chiến đấu
        return self.get_total_power() > other.get_total_power()

w1 = Warrior("Arthur", 1000, 150, 50)   
w2 = Warrior("Lancelot", 900, 180, 10)   

print(f"Chiến binh {w1.name} xuất trận!")

if w1 > w2:
    print(f"{w1.name} mạnh hơn {w2.name}!")
else:
    print(f"{w2.name} mạnh hơn hoặc hòa!")