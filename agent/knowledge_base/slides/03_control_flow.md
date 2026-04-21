# Chương 3: Câu lệnh điều kiện và Vòng lặp

## 3.1 Câu lệnh điều kiện if

### Cú pháp cơ bản
```c
if (điều_kiện) {
    // Code thực hiện khi điều kiện ĐÚNG (true)
}
```

### if - else
```c
if (điều_kiện) {
    // Code khi ĐÚNG
} else {
    // Code khi SAI
}
```

### Ví dụ: Kiểm tra số chẵn lẻ
```c
#include <stdio.h>

int main() {
    int n;
    printf("Nhập số nguyên: ");
    scanf("%d", &n);

    if (n % 2 == 0) {
        printf("%d là số chẵn\n", n);
    } else {
        printf("%d là số lẻ\n", n);
    }

    return 0;
}
```

### if - else if - else (Nhiều nhánh)
```c
#include <stdio.h>

int main() {
    float score;
    printf("Nhập điểm: ");
    scanf("%f", &score);

    if (score >= 9.0) {
        printf("Xuất sắc (A+)\n");
    } else if (score >= 8.0) {
        printf("Giỏi (A)\n");
    } else if (score >= 7.0) {
        printf("Khá (B)\n");
    } else if (score >= 5.0) {
        printf("Trung bình (C)\n");
    } else if (score >= 4.0) {
        printf("Yếu (D)\n");
    } else {
        printf("Kém (F)\n");
    }

    return 0;
}
```

### if lồng nhau (Nested if)
```c
int age = 20;
int hasLicense = 1;

if (age >= 18) {
    if (hasLicense) {
        printf("Được phép lái xe\n");
    } else {
        printf("Cần có bằng lái\n");
    }
} else {
    printf("Chưa đủ tuổi\n");
}
```

### Toán tử ba ngôi (Ternary Operator)
```c
// Cú pháp: điều_kiện ? giá_trị_đúng : giá_trị_sai
int a = 10, b = 20;
int max = (a > b) ? a : b;  // max = 20

// Tương đương với:
int max;
if (a > b) max = a;
else max = b;
```

## 3.2 Câu lệnh switch-case

### Cú pháp
```c
switch (biểu_thức) {
    case giá_trị_1:
        // Code cho giá trị 1
        break;
    case giá_trị_2:
        // Code cho giá trị 2
        break;
    default:
        // Code khi không khớp case nào
}
```

### Ví dụ: Menu chương trình
```c
#include <stdio.h>

int main() {
    int choice;
    printf("=== MENU ===\n");
    printf("1. Cộng\n");
    printf("2. Trừ\n");
    printf("3. Nhân\n");
    printf("4. Chia\n");
    printf("Chọn: ");
    scanf("%d", &choice);

    int a = 10, b = 3;
    switch (choice) {
        case 1:
            printf("%d + %d = %d\n", a, b, a + b);
            break;
        case 2:
            printf("%d - %d = %d\n", a, b, a - b);
            break;
        case 3:
            printf("%d * %d = %d\n", a, b, a * b);
            break;
        case 4:
            if (b != 0)
                printf("%d / %d = %.2f\n", a, b, (float)a / b);
            else
                printf("Lỗi: Chia cho 0!\n");
            break;
        default:
            printf("Lựa chọn không hợp lệ!\n");
    }

    return 0;
}
```

### Lưu ý quan trọng về switch
1. **Phải có `break`** — nếu quên, code sẽ "rơi xuống" (fall-through) case tiếp theo
2. Biểu thức switch phải là **số nguyên** hoặc **char** (không dùng float, string)
3. **`default`** là tùy chọn nhưng nên luôn có

### Fall-through (quên break)
```c
int x = 1;
switch (x) {
    case 1:
        printf("Một\n");   // In "Một"
        // Quên break!
    case 2:
        printf("Hai\n");   // Cũng in "Hai" (fall-through!)
        break;
    case 3:
        printf("Ba\n");    // Không in
}
// Output: Một
//         Hai
```

## 3.3 Vòng lặp for

### Cú pháp
```c
for (khởi_tạo; điều_kiện; cập_nhật) {
    // Code lặp lại
}
```

### Ví dụ cơ bản
```c
// In số từ 1 đến 10
for (int i = 1; i <= 10; i++) {
    printf("%d ", i);
}
// Output: 1 2 3 4 5 6 7 8 9 10

// In số chẵn từ 2 đến 20
for (int i = 2; i <= 20; i += 2) {
    printf("%d ", i);
}

// Đếm ngược
for (int i = 10; i >= 1; i--) {
    printf("%d ", i);
}
```

### Ví dụ: Tính tổng 1 + 2 + ... + N
```c
#include <stdio.h>

int main() {
    int n, sum = 0;
    printf("Nhập N: ");
    scanf("%d", &n);

    for (int i = 1; i <= n; i++) {
        sum += i;
    }

    printf("Tổng 1 đến %d = %d\n", n, sum);
    return 0;
}
```

### Ví dụ: Tính giai thừa N!
```c
#include <stdio.h>

int main() {
    int n;
    long long factorial = 1;
    printf("Nhập N: ");
    scanf("%d", &n);

    for (int i = 1; i <= n; i++) {
        factorial *= i;
    }

    printf("%d! = %lld\n", n, factorial);
    return 0;
}
```

### Vòng for lồng nhau
```c
// In bảng cửu chương
for (int i = 2; i <= 9; i++) {
    printf("=== Bảng %d ===\n", i);
    for (int j = 1; j <= 10; j++) {
        printf("%d x %d = %d\n", i, j, i * j);
    }
    printf("\n");
}
```

### In hình tam giác sao
```c
int n = 5;
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i; j++) {
        printf("* ");
    }
    printf("\n");
}
/*
*
* *
* * *
* * * *
* * * * *
*/
```

## 3.4 Vòng lặp while

### Cú pháp
```c
while (điều_kiện) {
    // Code lặp lại khi điều kiện còn ĐÚNG
}
```

### Ví dụ: Đoán số
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));
    int secret = rand() % 100 + 1;  // Số ngẫu nhiên 1-100
    int guess, attempts = 0;

    printf("Đoán số (1-100):\n");

    while (1) {  // Vòng lặp vô hạn
        printf("Nhập số: ");
        scanf("%d", &guess);
        attempts++;

        if (guess == secret) {
            printf("Chính xác! Bạn đoán %d lần.\n", attempts);
            break;  // Thoát vòng lặp
        } else if (guess < secret) {
            printf("Lớn hơn!\n");
        } else {
            printf("Nhỏ hơn!\n");
        }
    }

    return 0;
}
```

### Ví dụ: Đếm chữ số của một số
```c
int n = 12345, count = 0;
int temp = n;

while (temp > 0) {
    count++;
    temp /= 10;
}
printf("%d có %d chữ số\n", n, count);
// Output: 12345 có 5 chữ số
```

## 3.5 Vòng lặp do-while

### Cú pháp
```c
do {
    // Code thực hiện ÍT NHẤT 1 LẦN
} while (điều_kiện);  // ⚠️ Có dấu ; ở cuối!
```

### So sánh while vs do-while
```c
// while: kiểm tra TRƯỚC khi chạy
int x = 10;
while (x < 5) {
    printf("while: %d\n", x);  // KHÔNG chạy
    x++;
}

// do-while: chạy TRƯỚC rồi kiểm tra
int y = 10;
do {
    printf("do-while: %d\n", y);  // CHẠY 1 lần
    y++;
} while (y < 5);
```

### Ví dụ: Menu với do-while
```c
int choice;
do {
    printf("\n=== MENU ===\n");
    printf("1. Xem thông tin\n");
    printf("2. Thêm dữ liệu\n");
    printf("3. Thoát\n");
    printf("Chọn: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1: printf("Đang xem...\n"); break;
        case 2: printf("Đang thêm...\n"); break;
        case 3: printf("Tạm biệt!\n"); break;
        default: printf("Không hợp lệ!\n");
    }
} while (choice != 3);
```

## 3.6 break và continue

### break — Thoát vòng lặp
```c
for (int i = 1; i <= 10; i++) {
    if (i == 5) break;  // Dừng khi i = 5
    printf("%d ", i);
}
// Output: 1 2 3 4
```

### continue — Bỏ qua lần lặp hiện tại
```c
for (int i = 1; i <= 10; i++) {
    if (i % 3 == 0) continue;  // Bỏ qua số chia hết cho 3
    printf("%d ", i);
}
// Output: 1 2 4 5 7 8 10
```

## 3.7 Goto (Không khuyến khích)
```c
// goto có thể nhảy đến label bất kỳ — tránh dùng vì khó đọc code
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 10; j++) {
        if (i + j == 5) goto done;  // Thoát cả 2 vòng lặp
    }
}
done:
printf("Thoát!\n");
```

## 3.8 Lỗi thường gặp

### Lỗi 1: Vòng lặp vô hạn
```c
int i = 1;
while (i <= 10) {
    printf("%d ", i);
    // Quên i++; → Lặp mãi mãi!
}
```

### Lỗi 2: Lệch 1 (Off-by-one Error)
```c
// Muốn in 1 đến 10 nhưng:
for (int i = 1; i < 10; i++) { ... }  // Chỉ in 1-9!
for (int i = 0; i <= 10; i++) { ... } // In 0-10 (11 số)!
```

### Lỗi 3: Dấu ; sau for/while
```c
for (int i = 0; i < 10; i++);  // ⚠️ Dấu ; → vòng lặp rỗng!
{
    printf("%d", i);  // Chỉ chạy 1 lần, i = 10
}
```

### Lỗi 4: Dùng = thay vì ==
```c
if (x = 5) { ... }  // ⚠️ Gán x = 5, luôn true!
if (x == 5) { ... } // ✅ So sánh x với 5
```

## 3.9 Bài tập thực hành

### Bài 1: Kiểm tra số nguyên tố
Nhập số N, kiểm tra N có phải số nguyên tố không.

### Bài 2: Dãy Fibonacci
In N số đầu tiên của dãy Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13,...

### Bài 3: Tam giác Pascal
In tam giác Pascal với N dòng.

### Bài 4: Số hoàn hảo
Kiểm tra một số có phải số hoàn hảo không (tổng ước = chính nó, vd: 6 = 1+2+3).

### Bài 5: ATM đơn giản
Mô phỏng máy ATM: nạp tiền, rút tiền, xem số dư, thoát (dùng do-while + switch).
