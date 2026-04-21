# Câu hỏi thường gặp (FAQ) — Khóa học Lập trình C/C++ cơ bản

## 📦 Cài đặt và Môi trường

### Q: Làm sao cài đặt trình biên dịch C/C++ trên Windows?
**A:** Có 3 cách chính:
1. **MSYS2 + MinGW (Khuyến nghị):** Tải MSYS2 từ https://www.msys2.org/, cài xong mở terminal chạy `pacman -S mingw-w64-ucrt-x86_64-gcc`. Thêm `C:\msys64\ucrt64\bin` vào PATH.
2. **Dev-C++:** Tải về cài đặt, đã tích hợp sẵn compiler MinGW.
3. **Visual Studio:** Tải Visual Studio Community, chọn workload "Desktop development with C++".

Kiểm tra cài đặt: mở CMD/PowerShell gõ `gcc --version`. Nếu hiện phiên bản nghĩa là đã cài thành công.

### Q: Lỗi "gcc is not recognized as an internal or external command" là sao?
**A:** Lỗi này nghĩa là hệ thống chưa tìm thấy gcc trong PATH. Cách sửa:
1. Tìm thư mục chứa `gcc.exe` (thường là `C:\msys64\ucrt64\bin` hoặc `C:\MinGW\bin`)
2. Mở Settings → System → About → Advanced system settings → Environment Variables
3. Trong System variables, tìm `Path`, click Edit
4. Thêm đường dẫn chứa gcc.exe
5. Mở CMD mới (CMD cũ không nhận PATH mới) và thử lại

### Q: Làm sao cài VS Code để code C/C++?
**A:**
1. Tải VS Code: https://code.visualstudio.com/
2. Cài extension **"C/C++"** (của Microsoft, ID: ms-vscode.cpptools)
3. Cài extension **"Code Runner"** (của Jun Han) để chạy nhanh bằng Ctrl+Alt+N
4. Đảm bảo đã cài gcc/g++ và thêm vào PATH
5. Tạo file `.c`, viết code, nhấn Ctrl+Alt+N để chạy

### Q: Biên dịch file C và C++ khác nhau như thế nào?
**A:**
- File C (`.c`): Dùng `gcc filename.c -o output`
- File C++ (`.cpp`): Dùng `g++ filename.cpp -o output`
- Chạy: `./output` (Linux/Mac) hoặc `output.exe` (Windows)
- Lưu ý: `gcc` không biên dịch được C++ code (cout, class,...). Luôn dùng `g++` cho file `.cpp`.

### Q: Tại sao chạy chương trình xong cửa sổ CMD đóng ngay?
**A:** Chương trình chạy xong và thoát. Cách giữ cửa sổ:
1. Thêm `system("pause");` trước `return 0;` (Chỉ Windows, cần `#include <stdlib.h>`)
2. Thêm `getchar();` trước return
3. **Cách tốt nhất:** Chạy từ terminal/CMD thay vì click đúp file .exe

## 🐛 Lỗi biên dịch thường gặp

### Q: Lỗi "expected ';' before..." là gì?
**A:** Bạn quên dấu chấm phẩy (`;`) ở cuối câu lệnh phía trên dòng lỗi. Kiểm tra dòng **phía trên** dòng báo lỗi:
```c
int x = 10   // ← Thiếu ; ở đây
printf("%d", x);  // Compiler báo lỗi ở dòng này
```

### Q: Lỗi "undeclared identifier" hoặc "was not declared in this scope" là gì?
**A:** Biến chưa được khai báo hoặc viết sai tên. Kiểm tra:
1. Đã khai báo biến chưa? (`int x;`)
2. Viết đúng tên chưa? (phân biệt hoa thường: `count` ≠ `Count`)
3. Biến có nằm trong scope hiện tại không? (biến khai báo trong `{}` chỉ tồn tại trong đó)
4. Có include đúng thư viện không? (`printf` cần `#include <stdio.h>`)

### Q: Lỗi "implicit declaration of function" là gì?
**A:** Bạn gọi hàm mà compiler chưa biết. Có thể:
1. Quên `#include` thư viện: `printf` cần `stdio.h`, `sqrt` cần `math.h`
2. Hàm tự viết nằm **sau** hàm main → cần khai báo prototype ở đầu file
3. Viết sai tên hàm

### Q: Lỗi "undefined reference to 'function_name'" là gì?
**A:** Linker không tìm thấy định nghĩa hàm. Nguyên nhân:
1. Quên link thư viện: với `math.h`, cần thêm `-lm` khi biên dịch: `gcc file.c -o output -lm`
2. Khai báo hàm (prototype) nhưng quên viết thân hàm
3. Tên hàm trong prototype khác với tên trong định nghĩa

### Q: Lỗi "format '%d' expects argument of type 'int'" là gì?
**A:** Format specifier không khớp kiểu dữ liệu:
- `%d` cho int
- `%f` cho float/double
- `%c` cho char
- `%s` cho chuỗi
- `%lld` cho long long
- `%p` cho con trỏ (địa chỉ)

## 🔧 Lỗi runtime thường gặp

### Q: Segmentation Fault là gì? Làm sao sửa?
**A:** Segmentation Fault (lỗi phân đoạn) xảy ra khi chương trình truy cập vùng nhớ không hợp lệ. Nguyên nhân phổ biến:
1. **Dùng con trỏ chưa khởi tạo**: `int *p; *p = 10;` → phải gán `p = &x;` trước
2. **Truy cập mảng ngoài phạm vi**: `arr[100]` khi mảng chỉ có 10 phần tử
3. **Dùng con trỏ NULL**: Con trỏ `= NULL` hoặc `malloc` trả về NULL
4. **Stack overflow**: Đệ quy không có điều kiện dừng
5. **Dùng con trỏ sau khi free**: `free(p); *p = 5;` → dangling pointer

### Q: Tại sao kết quả tính toán sai? 7/2 = 3 thay vì 3.5?
**A:** Đây là **chia nguyên** (integer division). Khi cả hai toán hạng đều là `int`, kết quả cũng là `int` (phần thập phân bị cắt).
Cách sửa: ép ít nhất 1 toán hạng sang `float`:
```c
float result = (float)7 / 2;  // = 3.5
float result = 7.0 / 2;       // = 3.5
```

### Q: Tại sao nhập chuỗi bằng scanf bị bỏ qua / chỉ lấy được 1 từ?
**A:** 
- `scanf("%s")` chỉ đọc đến khoảng trắng đầu tiên
- Dùng `fgets(str, size, stdin)` để đọc cả dòng
- Nếu trước đó có `scanf("%d")`, ký tự `\n` còn trong buffer → thêm `getchar();` trước `fgets`

### Q: Memory leak là gì? Có nguy hiểm không?
**A:** Memory leak (rò rỉ bộ nhớ) xảy ra khi bạn `malloc`/`calloc` nhưng quên `free`. Bộ nhớ bị chiếm nhưng không dùng. Nếu lặp lại nhiều lần, RAM sẽ đầy dần và chương trình crash. Quy tắc: **mỗi malloc phải có free tương ứng**.

## 📚 Kiến thức chung

### Q: C và C++ khác nhau ở điểm nào?
**A:** 
| Đặc điểm | C | C++ |
|-----------|---|-----|
| Paradigm | Lập trình thủ tục | Thủ tục + Hướng đối tượng (OOP) |
| I/O | printf/scanf | cout/cin (+ printf/scanf) |
| Bộ nhớ | malloc/free | new/delete (+ malloc/free) |
| Chuỗi | char[] | std::string (+ char[]) |
| Mảng động | Tự quản lý | std::vector |
| Bool | Cần stdbool.h (C99) | Có sẵn |
| Header | `.h` | `.h` hoặc không extension |

### Q: Nên học C hay C++ trước?
**A:** Nên học **C trước** vì:
1. C đơn giản hơn, ít khái niệm hơn
2. Hiểu rõ bộ nhớ, con trỏ — nền tảng quan trọng
3. C++ kế thừa hầu hết cú pháp C
4. Sau khi vững C, chuyển sang C++ rất nhanh

### Q: Khi nào dùng mảng, khi nào dùng con trỏ + malloc?
**A:**
- **Mảng tĩnh** (`int arr[100]`): Khi biết trước kích thước lúc compile, kích thước nhỏ-vừa
- **Cấp phát động** (`malloc`): Khi kích thước phụ thuộc input của người dùng, cần mảng lớn, hoặc cần thay đổi kích thước (realloc)

### Q: Tại sao cần dùng & trong scanf mà printf thì không?
**A:** `scanf` cần **địa chỉ** để ghi giá trị vào biến, nên cần `&` (toán tử lấy địa chỉ). `printf` chỉ cần **đọc giá trị** nên truyền trực tiếp.
Exception: Mảng char (`char str[]`) không cần `&` vì tên mảng đã là địa chỉ.

### Q: break và continue khác gì nhau?
**A:**
- `break`: **Thoát** hoàn toàn khỏi vòng lặp (for/while/do-while) hoặc switch
- `continue`: **Bỏ qua** phần còn lại của lần lặp hiện tại, nhảy sang lần lặp tiếp theo
```c
for (int i = 1; i <= 5; i++) {
    if (i == 3) continue; // Bỏ qua i=3
    if (i == 5) break;    // Dừng khi i=5
    printf("%d ", i);     // In: 1 2 4
}
```

## 📋 Thông tin khóa học

### Q: Lịch học cụ thể như thế nào?
**A:** Vui lòng xem thông tin chi tiết trong mục Thông tin khóa học hoặc hỏi trực tiếp giảng viên. Lịch có thể thay đổi theo từng kỳ.

### Q: Tài liệu tham khảo nào nên đọc thêm?
**A:** 
1. **Sách:** "The C Programming Language" — Brian Kernighan & Dennis Ritchie (K&R)
2. **Online:** https://www.learn-c.org/, https://cplusplus.com/
3. **Video:** CS50 của Harvard (YouTube)
4. **Tài liệu khóa học:** Trong hệ thống LMS của trường

### Q: Làm bài tập ở đâu? Nộp bài kiểu gì?
**A:** Bài tập được giao trên hệ thống LMS. Nộp bài dạng file `.c` hoặc `.cpp` theo hướng dẫn cụ thể từng bài. Hạn nộp theo timeline khóa học.
