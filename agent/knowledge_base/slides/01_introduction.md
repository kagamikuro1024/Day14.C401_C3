# Chương 1: Giới thiệu ngôn ngữ C/C++ và Cài đặt Môi trường

## 1.1 Tổng quan về ngôn ngữ C

### Lịch sử ngôn ngữ C
- Ngôn ngữ C được phát triển bởi **Dennis Ritchie** tại Bell Labs vào năm **1972**.
- C được thiết kế ban đầu để phát triển hệ điều hành **UNIX**.
- C là ngôn ngữ lập trình **bậc trung** (mid-level), kết hợp sức mạnh của assembly với tính dễ đọc của ngôn ngữ bậc cao.
- C là nền tảng cho nhiều ngôn ngữ hiện đại: C++, Java, C#, Python (CPython), Go.

### Đặc điểm nổi bật của C
- **Hiệu suất cao**: Biên dịch trực tiếp ra mã máy, tốc độ thực thi rất nhanh.
- **Portable (Di động)**: Code C có thể biên dịch trên nhiều nền tảng khác nhau.
- **Low-level access**: Cho phép thao tác trực tiếp với bộ nhớ qua con trỏ.
- **Cú pháp đơn giản**: Chỉ có 32 từ khóa (keywords) trong C chuẩn.
- **Thư viện chuẩn phong phú**: stdio.h, stdlib.h, string.h, math.h,...

### Ứng dụng thực tế của C
- Hệ điều hành (Linux kernel, Windows kernel)
- Hệ thống nhúng (embedded systems), IoT
- Game engines, đồ họa máy tính
- Cơ sở dữ liệu (MySQL, PostgreSQL)
- Trình biên dịch và thông dịch (Python, PHP)

## 1.2 Tổng quan về ngôn ngữ C++

### Lịch sử C++
- C++ được phát triển bởi **Bjarne Stroustrup** tại Bell Labs vào năm **1979**, ban đầu có tên "C with Classes".
- Chính thức đổi tên C++ vào năm 1983.
- C++ là **superset** (tập cha) của C — hầu hết code C hợp lệ đều chạy được trong C++.
- Các phiên bản tiêu chuẩn: C++98, C++11, C++14, C++17, C++20, C++23.

### Đặc điểm nổi bật của C++
- **Lập trình hướng đối tượng (OOP)**: Classes, inheritance, polymorphism, encapsulation.
- **Generic Programming**: Templates cho phép viết code tổng quát.
- **STL (Standard Template Library)**: vector, map, set, algorithm,...
- **Tương thích ngược**: Chạy được hầu hết code C.
- **Quản lý bộ nhớ linh hoạt**: new/delete, smart pointers (C++11+).

## 1.3 Cài đặt môi trường lập trình

### Trên Windows

#### Cách 1: MinGW (Khuyến nghị cho người mới)
1. Tải **MinGW** từ trang chủ: https://www.mingw-w64.org/
2. Hoặc cài thông qua **MSYS2**: https://www.msys2.org/
3. Sau khi cài xong, mở terminal MSYS2 và chạy:
   ```bash
   pacman -S mingw-w64-ucrt-x86_64-gcc
   ```
4. Thêm đường dẫn MinGW vào PATH:
   - Mở "Environment Variables" trong System Settings
   - Thêm `C:\msys64\ucrt64\bin` vào biến PATH
5. Kiểm tra cài đặt:
   ```bash
   gcc --version
   g++ --version
   ```

#### Cách 2: Visual Studio (Đầy đủ nhất)
1. Tải **Visual Studio Community** (miễn phí): https://visualstudio.microsoft.com/
2. Trong installer, chọn workload **"Desktop development with C++"**
3. Sau khi cài, mở Visual Studio → File → New → Project → Console App

#### Cách 3: Dev-C++ (Đơn giản nhất)
1. Tải **Dev-C++** hoặc **Embarcadero Dev-C++** (bản mới)
2. Cài đặt bình thường, đã tích hợp sẵn MinGW compiler

### Trên macOS
1. Mở Terminal và chạy: `xcode-select --install`
2. Hoặc cài **Homebrew** rồi: `brew install gcc`
3. Kiểm tra: `gcc --version` hoặc `clang --version`

### Trên Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install build-essential
gcc --version
g++ --version
```

### IDE và Text Editor khuyên dùng
| Công cụ | Ưu điểm | Phù hợp với |
|---------|---------|-------------|
| **VS Code** | Miễn phí, extensions phong phú, đa nền tảng | Mọi level |
| **Code::Blocks** | Miễn phí, đơn giản, tích hợp compiler | Người mới |
| **CLion** | Chuyên nghiệp, debug mạnh | Nâng cao |
| **Dev-C++** | Cực đơn giản, nhẹ | Người mới |

### Cấu hình VS Code cho C/C++
1. Cài extension **"C/C++"** của Microsoft (ms-vscode.cpptools)
2. Cài extension **"Code Runner"** để chạy nhanh
3. Tạo file `.vscode/tasks.json` để cấu hình build
4. Sử dụng Terminal tích hợp để compile và chạy

## 1.4 Chương trình C đầu tiên — Hello World

```c
#include <stdio.h>  // Thư viện nhập xuất chuẩn

int main() {
    printf("Hello, World!\n");  // In ra màn hình
    return 0;                    // Trả về 0 = chương trình chạy OK
}
```

### Giải thích từng dòng:
- `#include <stdio.h>`: Khai báo sử dụng thư viện nhập xuất chuẩn (Standard I/O). Hàm `printf` nằm trong thư viện này.
- `int main()`: Hàm chính — điểm bắt đầu của mọi chương trình C. `int` nghĩa là hàm trả về số nguyên.
- `printf("Hello, World!\n")`: In chuỗi ra màn hình console. `\n` là ký tự xuống dòng.
- `return 0`: Trả về giá trị 0 cho hệ điều hành, báo hiệu chương trình kết thúc thành công.

### Biên dịch và chạy
```bash
# Biên dịch file .c thành file thực thi
gcc hello.c -o hello

# Chạy chương trình
./hello        # Linux/macOS
hello.exe      # Windows
```

## 1.5 Chương trình C++ đầu tiên

```cpp
#include <iostream>  // Thư viện nhập xuất C++
using namespace std; // Sử dụng namespace std

int main() {
    cout << "Hello, World!" << endl;  // In ra màn hình
    return 0;
}
```

### So sánh C vs C++ (Hello World)
| Đặc điểm | C | C++ |
|-----------|---|-----|
| Thư viện I/O | `#include <stdio.h>` | `#include <iostream>` |
| In ra màn hình | `printf()` | `cout <<` |
| Xuống dòng | `\n` | `endl` hoặc `\n` |
| Biên dịch | `gcc` | `g++` |

## 1.6 Quy trình biên dịch (Compilation Process)

```
Source Code (.c/.cpp)
       ↓
  [Preprocessor] → Xử lý #include, #define
       ↓
  [Compiler] → Chuyển thành Assembly
       ↓
  [Assembler] → Chuyển thành Object Code (.o)
       ↓
  [Linker] → Liên kết thư viện → Executable
```

### Các bước chi tiết:
1. **Preprocessing**: Xử lý các directive (#include, #define, #ifdef)
2. **Compilation**: Chuyển code thành mã Assembly
3. **Assembly**: Chuyển Assembly thành Object code (mã máy)
4. **Linking**: Liên kết các Object file và thư viện thành file thực thi

## 1.7 Lỗi thường gặp khi bắt đầu

### Lỗi 1: "gcc is not recognized"
- **Nguyên nhân**: Chưa cài compiler hoặc chưa thêm vào PATH
- **Cách sửa**: Cài MinGW/MSYS2 và thêm đường dẫn bin vào PATH

### Lỗi 2: "undefined reference to main"
- **Nguyên nhân**: Thiếu hàm `main()` hoặc viết sai tên
- **Cách sửa**: Đảm bảo có `int main()` trong code

### Lỗi 3: Quên dấu chấm phẩy (;)
- **Nguyên nhân**: C/C++ yêu cầu `;` kết thúc mỗi câu lệnh
- **Cách sửa**: Kiểm tra cuối mỗi dòng lệnh

### Lỗi 4: File not found khi include
- **Nguyên nhân**: Gõ sai tên thư viện hoặc chưa cài đầy đủ
- **Cách sửa**: Kiểm tra lại tên header file. Thư viện chuẩn dùng `<>`, file tự tạo dùng `""`
