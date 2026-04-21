# Chương 4: Hàm (Functions)

## 4.1 Khái niệm về hàm

### Hàm là gì?
Hàm (function) là một **khối code** được đặt tên, thực hiện một nhiệm vụ cụ thể và có thể được gọi (call) nhiều lần trong chương trình.

### Tại sao cần hàm?
1. **Tái sử dụng code**: Viết một lần, gọi nhiều lần
2. **Chia nhỏ bài toán**: Phân chia chương trình lớn thành các phần nhỏ dễ quản lý
3. **Dễ debug**: Tìm lỗi trong từng hàm riêng lẻ
4. **Dễ bảo trì**: Sửa một chỗ, áp dụng mọi nơi
5. **Trừu tượng hóa**: Ẩn chi tiết, chỉ cần biết cách gọi

## 4.2 Cú pháp khai báo hàm

```c
kiểu_trả_về tên_hàm(kiểu_tham_số_1 tên_ts_1, kiểu_tham_số_2 tên_ts_2, ...) {
    // Thân hàm
    return giá_trị;  // Trả về kết quả (nếu không phải void)
}
```

### Ví dụ đơn giản
```c
// Hàm tính tổng hai số
int add(int a, int b) {
    return a + b;
}

// Hàm in lời chào (không trả về)
void greet(char name[]) {
    printf("Xin chào, %s!\n", name);
}

// Hàm không có tham số
void printLine() {
    printf("========================\n");
}

int main() {
    int result = add(5, 3);
    printf("5 + 3 = %d\n", result);  // 5 + 3 = 8

    greet("Học viên");  // Xin chào, Học viên!
    printLine();        // ========================

    return 0;
}
```

## 4.3 Khai báo trước (Function Prototype / Declaration)

Khi hàm được **định nghĩa sau** hàm `main`, cần **khai báo trước** (prototype) ở đầu file:

```c
#include <stdio.h>

// Khai báo trước (prototype)
int add(int a, int b);
void greet(char name[]);

int main() {
    printf("%d\n", add(3, 4));   // OK — đã khai báo
    greet("An");
    return 0;
}

// Định nghĩa hàm (implementation)
int add(int a, int b) {
    return a + b;
}

void greet(char name[]) {
    printf("Chào %s!\n", name);
}
```

### Tại sao cần prototype?
- Compiler đọc code **từ trên xuống dưới**
- Nếu gọi hàm trước khi định nghĩa → compiler không biết hàm đó tồn tại → lỗi
- Prototype báo cho compiler biết hàm sẽ được định nghĩa ở đâu đó

## 4.4 Kiểu trả về (Return Types)

### void — Không trả về
```c
void sayHello() {
    printf("Hello!\n");
    // Không cần return (hoặc return; không giá trị)
}
```

### int, float, char,... — Trả về giá trị
```c
int square(int x) {
    return x * x;
}

float average(float a, float b) {
    return (a + b) / 2.0;
}

char getGrade(float score) {
    if (score >= 9) return 'A';
    if (score >= 7) return 'B';
    if (score >= 5) return 'C';
    return 'F';
}
```

### Lưu ý về return
- Khi gặp `return`, hàm **kết thúc ngay** tại đó
- Hàm có kiểu trả về PHẢI có `return` với giá trị đúng kiểu
- Hàm `void` có thể dùng `return;` để kết thúc sớm

## 4.5 Tham số hàm

### Truyền theo giá trị (Pass by Value) — Mặc định trong C
```c
void doubleValue(int x) {
    x = x * 2;  // Chỉ thay đổi BẢN SAO, không ảnh hưởng biến gốc
    printf("Trong hàm: x = %d\n", x);
}

int main() {
    int a = 5;
    doubleValue(a);
    printf("Ngoài hàm: a = %d\n", a);  // a vẫn = 5!
    return 0;
}
// Output:
// Trong hàm: x = 10
// Ngoài hàm: a = 5
```

### Truyền theo con trỏ (Pass by Pointer) — Thay đổi biến gốc
```c
void doubleValue(int *x) {    // Nhận con trỏ
    *x = (*x) * 2;             // Thay đổi giá trị tại địa chỉ
}

int main() {
    int a = 5;
    doubleValue(&a);           // Truyền địa chỉ
    printf("a = %d\n", a);    // a = 10 (đã thay đổi!)
    return 0;
}
```

### Truyền theo tham chiếu — C++ only (Pass by Reference)
```cpp
void doubleValue(int &x) {   // Tham chiếu (C++ only)
    x = x * 2;                // Thay đổi trực tiếp biến gốc
}

int main() {
    int a = 5;
    doubleValue(a);           // Không cần &
    cout << "a = " << a;     // a = 10
}
```

### Truyền mảng vào hàm
```c
// Mảng luôn được truyền theo tham chiếu (thực chất là con trỏ)
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Hàm tìm max trong mảng
int findMax(int arr[], int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

int main() {
    int numbers[] = {5, 2, 8, 1, 9, 3};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printArray(numbers, size);           // 5 2 8 1 9 3
    printf("Max = %d\n", findMax(numbers, size));  // Max = 9
    return 0;
}
```

## 4.6 Phạm vi biến (Variable Scope)

### Biến cục bộ (Local Variables)
```c
void foo() {
    int x = 10;  // x chỉ tồn tại trong hàm foo
    printf("x = %d\n", x);
}

int main() {
    foo();
    // printf("%d", x);  // ❌ LỖI! x không tồn tại ở đây
    return 0;
}
```

### Biến toàn cục (Global Variables)
```c
int globalCount = 0;  // Biến toàn cục — mọi hàm đều truy cập được

void increment() {
    globalCount++;
}

int main() {
    increment();
    increment();
    printf("Count = %d\n", globalCount);  // Count = 2
    return 0;
}
```

### Biến static
```c
void counter() {
    static int count = 0;  // Khởi tạo 1 lần, giữ giá trị giữa các lần gọi
    count++;
    printf("Lần gọi thứ: %d\n", count);
}

int main() {
    counter();  // Lần gọi thứ: 1
    counter();  // Lần gọi thứ: 2
    counter();  // Lần gọi thứ: 3
    return 0;
}
```

## 4.7 Đệ quy (Recursion)

### Khái niệm
Đệ quy là kỹ thuật mà **hàm gọi lại chính nó**. Mỗi hàm đệ quy cần:
1. **Base case** (điều kiện dừng) — để tránh lặp vô hạn
2. **Recursive case** — gọi lại chính nó với bài toán nhỏ hơn

### Ví dụ: Tính giai thừa
```c
long long factorial(int n) {
    // Base case
    if (n <= 1) return 1;
    // Recursive case
    return n * factorial(n - 1);
}
// factorial(5) = 5 * factorial(4)
//              = 5 * 4 * factorial(3)
//              = 5 * 4 * 3 * factorial(2)
//              = 5 * 4 * 3 * 2 * factorial(1)
//              = 5 * 4 * 3 * 2 * 1 = 120
```

### Ví dụ: Fibonacci
```c
int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

### Ví dụ: Tính lũy thừa
```c
double power(double base, int exp) {
    if (exp == 0) return 1;
    if (exp < 0) return 1.0 / power(base, -exp);
    return base * power(base, exp - 1);
}
```

### Ví dụ: Tháp Hà Nội
```c
void hanoi(int n, char from, char to, char aux) {
    if (n == 1) {
        printf("Di chuyển đĩa 1 từ %c → %c\n", from, to);
        return;
    }
    hanoi(n - 1, from, aux, to);
    printf("Di chuyển đĩa %d từ %c → %c\n", n, from, to);
    hanoi(n - 1, aux, to, from);
}
// Gọi: hanoi(3, 'A', 'C', 'B');
```

### Đệ quy vs Vòng lặp
| | Đệ quy | Vòng lặp |
|---|--------|---------|
| Đọc code | Dễ hiểu logic | Dài hơn |
| Hiệu suất | Chậm hơn (overhead call) | Nhanh hơn |
| Bộ nhớ | Tốn stack | Ít tốn hơn |
| Rủi ro | Stack overflow | Ít rủi ro |

## 4.8 Một số hàm thường dùng trong thư viện chuẩn

### math.h
```c
#include <math.h>

sqrt(25);       // = 5.0 (căn bậc 2)
pow(2, 10);     // = 1024.0 (lũy thừa)
abs(-5);        // = 5 (giá trị tuyệt đối)
fabs(-3.14);    // = 3.14 (giá trị tuyệt đối float)
ceil(3.2);      // = 4.0 (làm tròn lên)
floor(3.8);     // = 3.0 (làm tròn xuống)
round(3.5);     // = 4.0 (làm tròn)
```

### stdlib.h
```c
#include <stdlib.h>

rand();             // Số ngẫu nhiên
rand() % 100;       // Số ngẫu nhiên 0-99
srand(time(NULL));  // Seed cho random

atoi("123");        // Chuyển string → int = 123
atof("3.14");       // Chuyển string → float = 3.14
```

### string.h (dùng với chuỗi — sẽ học kỹ ở Chương 5)
```c
#include <string.h>

strlen(str);           // Độ dài chuỗi
strcmp(s1, s2);         // So sánh 2 chuỗi
strcpy(dest, src);     // Copy chuỗi
strcat(dest, src);     // Nối chuỗi
```

## 4.9 Bài tập thực hành

### Bài 1: Hàm kiểm tra số nguyên tố
Viết hàm `int isPrime(int n)` trả về 1 nếu n là số nguyên tố.

### Bài 2: Hàm đệ quy tính tổng chữ số
Viết hàm đệ quy tính tổng các chữ số: `sumDigits(123) = 6`

### Bài 3: Hàm sắp xếp mảng
Viết hàm `void sortArray(int arr[], int size)` sắp xếp mảng tăng dần.

### Bài 4: Hàm đệ quy đảo chuỗi
Viết hàm đệ quy in ngược chuỗi ký tự.

### Bài 5: Calculator hoàn chỉnh
Viết chương trình máy tính dùng hàm riêng cho từng phép tính (+, -, *, /, %).
