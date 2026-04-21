# Chương 2: Biến, Kiểu Dữ Liệu và Nhập Xuất

## 2.1 Biến (Variables)

### Khái niệm
Biến là **vùng nhớ** được đặt tên, dùng để lưu trữ dữ liệu trong quá trình chương trình chạy. Giá trị của biến có thể thay đổi trong quá trình thực thi.

### Quy tắc đặt tên biến
- Bắt đầu bằng **chữ cái** hoặc **dấu gạch dưới** (_)
- Chỉ chứa chữ cái, chữ số, và dấu gạch dưới
- **Phân biệt hoa thường**: `age` khác `Age` khác `AGE`
- Không trùng với **từ khóa** (keywords): int, float, return, if, while,...
- Nên đặt tên có ý nghĩa: `studentAge` thay vì `a`, `totalScore` thay vì `x`

### Ví dụ đặt tên
```c
// ✅ Hợp lệ
int age;
float _salary;
char studentName;
int student_count;
int totalScore2;

// ❌ Không hợp lệ
int 2ndPlace;    // Bắt đầu bằng số
float my-salary; // Chứa dấu gạch ngang
int return;      // Trùng từ khóa
char my name;    // Chứa khoảng trắng
```

### Convention đặt tên phổ biến
- **camelCase**: `studentAge`, `totalScore` (phổ biến trong C++)
- **snake_case**: `student_age`, `total_score` (phổ biến trong C)
- **UPPER_CASE**: `MAX_SIZE`, `PI` (dùng cho hằng số)

## 2.2 Kiểu dữ liệu cơ bản

### Kiểu số nguyên (Integer Types)

| Kiểu | Kích thước | Phạm vi | Ghi chú |
|------|-----------|---------|---------|
| `char` | 1 byte | -128 → 127 | Cũng dùng cho ký tự |
| `unsigned char` | 1 byte | 0 → 255 | Chỉ số dương |
| `short` | 2 bytes | -32,768 → 32,767 | Số nguyên ngắn |
| `unsigned short` | 2 bytes | 0 → 65,535 | |
| `int` | 4 bytes | -2.1 tỷ → 2.1 tỷ | **Dùng phổ biến nhất** |
| `unsigned int` | 4 bytes | 0 → 4.2 tỷ | Chỉ số dương |
| `long` | 4-8 bytes | Tùy hệ thống | |
| `long long` | 8 bytes | ±9.2 × 10^18 | Số rất lớn |

### Kiểu số thực (Floating-point Types)

| Kiểu | Kích thước | Độ chính xác | Phạm vi |
|------|-----------|-------------|---------|
| `float` | 4 bytes | ~7 chữ số | ±3.4 × 10^38 |
| `double` | 8 bytes | ~15 chữ số | ±1.7 × 10^308 |
| `long double` | 8-16 bytes | ~19 chữ số | Tùy hệ thống |

### Kiểu ký tự (Character Type)
```c
char letter = 'A';        // Lưu ký tự 'A' (mã ASCII: 65)
char digit = '0';          // Ký tự '0' (mã ASCII: 48)
char newline = '\n';       // Ký tự xuống dòng
```

### Kiểu logic (Boolean — C99+)
```c
#include <stdbool.h>  // Cần include thư viện này trong C
bool isActive = true;
bool isFinished = false;
```

Trong C++, `bool` là kiểu có sẵn, không cần include.

## 2.3 Khai báo và khởi tạo biến

### Cú pháp khai báo
```c
// Khai báo (chưa gán giá trị)
int age;
float salary;

// Khai báo + khởi tạo (gán giá trị ngay)
int age = 20;
float salary = 15000.50;
char grade = 'A';

// Khai báo nhiều biến cùng kiểu
int x = 1, y = 2, z = 3;
```

### Lưu ý quan trọng
> **⚠️ Biến chưa khởi tạo chứa giá trị rác (garbage value)!**
> Luôn khởi tạo biến trước khi sử dụng.

```c
int x;           // x chứa giá trị rác (không xác định)
printf("%d", x); // Kết quả không dự đoán được!

int y = 0;       // y = 0 (an toàn)
printf("%d", y); // Kết quả: 0
```

## 2.4 Hằng số (Constants)

### Cách 1: Dùng `const`
```c
const float PI = 3.14159;
const int MAX_STUDENTS = 100;

PI = 3.14;  // ❌ LỖI! Không thể thay đổi giá trị hằng số
```

### Cách 2: Dùng `#define`
```c
#define PI 3.14159
#define MAX_SIZE 100
#define COURSE_NAME "Lap trinh C"

// Preprocessor sẽ thay thế PI bằng 3.14159 trước khi biên dịch
float area = PI * r * r;
```

### So sánh const vs #define
| | `const` | `#define` |
|---|---------|-----------|
| Kiểu dữ liệu | Có kiểu rõ ràng | Không có kiểu |
| Scope | Tuân theo scope | Toàn bộ file |
| Debug | Dễ debug | Khó debug |
| Bộ nhớ | Chiếm bộ nhớ | Không chiếm |
| **Khuyến nghị** | **Dùng trong C++** | **Dùng trong C** |

## 2.5 Nhập xuất trong C (printf & scanf)

### Hàm printf — Xuất dữ liệu

#### Format specifiers (Định dạng xuất)
| Specifier | Kiểu | Ví dụ |
|-----------|------|-------|
| `%d` | int | `printf("%d", 42)` → `42` |
| `%f` | float/double | `printf("%f", 3.14)` → `3.140000` |
| `%.2f` | float (2 số thập phân) | `printf("%.2f", 3.14159)` → `3.14` |
| `%c` | char | `printf("%c", 'A')` → `A` |
| `%s` | string | `printf("%s", "Hello")` → `Hello` |
| `%ld` | long | `printf("%ld", 1000000L)` |
| `%lld` | long long | `printf("%lld", 9999999999LL)` |
| `%x` | hex | `printf("%x", 255)` → `ff` |
| `%o` | octal | `printf("%o", 8)` → `10` |
| `%%` | ký tự % | `printf("100%%")` → `100%` |

#### Ví dụ xuất dữ liệu
```c
#include <stdio.h>

int main() {
    char name[] = "Nguyen Van A";
    int age = 20;
    float gpa = 3.75;

    printf("Họ tên: %s\n", name);
    printf("Tuổi: %d\n", age);
    printf("GPA: %.2f\n", gpa);
    printf("Thông tin: %s, %d tuổi, GPA %.1f\n", name, age, gpa);

    // Căn lề
    printf("|%-20s|%5d|%8.2f|\n", name, age, gpa);
    // Kết quả: |Nguyen Van A        |   20|    3.75|

    return 0;
}
```

### Hàm scanf — Nhập dữ liệu

```c
#include <stdio.h>

int main() {
    int age;
    float height;
    char name[50];

    printf("Nhập tuổi: ");
    scanf("%d", &age);          // ⚠️ Có dấu & trước biến

    printf("Nhập chiều cao: ");
    scanf("%f", &height);

    printf("Nhập tên: ");
    scanf("%s", name);           // 📝 Chuỗi KHÔNG cần &

    printf("Bạn %s, %d tuổi, cao %.1fm\n", name, age, height);

    return 0;
}
```

### Lưu ý quan trọng về scanf
1. **Phải có dấu `&`** trước biến (trừ chuỗi/mảng): `scanf("%d", &x);`
2. **`%s` chỉ đọc đến khoảng trắng**: "Nguyen Van A" chỉ đọc được "Nguyen"
3. Để đọc cả dòng, dùng `fgets`:
   ```c
   char name[50];
   printf("Nhập họ tên: ");
   fgets(name, sizeof(name), stdin);
   ```

### Vấn đề buffer khi dùng scanf
```c
int age;
char name[50];

scanf("%d", &age);      // Nhập 20 → Enter
// Ký tự '\n' còn lại trong buffer!
fgets(name, 50, stdin); // Đọc luôn '\n' → Bỏ qua!

// Cách sửa: thêm getchar() hoặc scanf(" ") để xóa buffer
scanf("%d", &age);
getchar();              // Xóa ký tự '\n' khỏi buffer
fgets(name, 50, stdin); // Giờ mới đọc đúng
```

## 2.6 Nhập xuất trong C++ (cin & cout)

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int age;
    string name;
    float gpa;

    cout << "Nhập tên: ";
    getline(cin, name);       // Đọc cả dòng (có khoảng trắng)

    cout << "Nhập tuổi: ";
    cin >> age;

    cout << "Nhập GPA: ";
    cin >> gpa;

    cout << "Thông tin:" << endl;
    cout << "Tên: " << name << endl;
    cout << "Tuổi: " << age << endl;
    cout << "GPA: " << fixed << setprecision(2) << gpa << endl;

    return 0;
}
```

## 2.7 Ép kiểu (Type Casting)

### Ép kiểu ngầm định (Implicit)
```c
int a = 5;
float b = a;       // int → float: 5 → 5.0 (tự động)
int c = 3.7;       // float → int: 3.7 → 3 (mất phần thập phân!)
```

### Ép kiểu tường minh (Explicit)
```c
int a = 7, b = 2;
float result1 = a / b;         // = 3.0 (chia nguyên trước, rồi gán)
float result2 = (float)a / b;  // = 3.5 (ép float trước khi chia)
```

### Thứ tự ưu tiên ép kiểu ngầm
```
char → short → int → long → long long → float → double → long double
```
Kiểu nhỏ hơn tự động chuyển thành kiểu lớn hơn khi tính toán.

## 2.8 Toán tử (Operators)

### Toán tử số học
| Toán tử | Ý nghĩa | Ví dụ | Kết quả |
|---------|---------|-------|---------|
| `+` | Cộng | `5 + 3` | `8` |
| `-` | Trừ | `5 - 3` | `2` |
| `*` | Nhân | `5 * 3` | `15` |
| `/` | Chia | `7 / 2` | `3` (chia nguyên!) |
| `%` | Chia lấy dư | `7 % 2` | `1` |

### Toán tử gán
```c
int x = 10;
x += 5;   // x = x + 5 = 15
x -= 3;   // x = x - 3 = 12
x *= 2;   // x = x * 2 = 24
x /= 4;   // x = x / 4 = 6
x %= 4;   // x = x % 4 = 2
```

### Toán tử tăng/giảm
```c
int a = 5;
a++;      // a = 6 (tăng 1)
a--;      // a = 5 (giảm 1)

int b = a++;  // b = 5 (gán trước, tăng sau)
int c = ++a;  // c = 7 (tăng trước, gán sau)
```

### Toán tử so sánh
| Toán tử | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| `==` | Bằng | `a == b` |
| `!=` | Khác | `a != b` |
| `>` | Lớn hơn | `a > b` |
| `<` | Nhỏ hơn | `a < b` |
| `>=` | Lớn hơn hoặc bằng | `a >= b` |
| `<=` | Nhỏ hơn hoặc bằng | `a <= b` |

### Toán tử logic
| Toán tử | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| `&&` | AND (Và) | `a > 0 && b > 0` |
| `\|\|` | OR (Hoặc) | `a > 0 \|\| b > 0` |
| `!` | NOT (Phủ định) | `!(a > 0)` |

## 2.9 Bài tập thực hành

### Bài 1: Tính diện tích hình tròn
Viết chương trình nhập bán kính, tính và in diện tích hình tròn.

### Bài 2: Đổi nhiệt độ
Viết chương trình đổi nhiệt độ từ Celsius sang Fahrenheit: F = C × 9/5 + 32

### Bài 3: Tính BMI
Nhập cân nặng (kg) và chiều cao (m), tính chỉ số BMI = weight / (height * height)

### Bài 4: Swap hai số
Nhập hai số nguyên, hoán đổi giá trị và in kết quả.
