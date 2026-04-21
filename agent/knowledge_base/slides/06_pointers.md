# Chương 6: Con trỏ (Pointers)

## 6.1 Khái niệm cơ bản

### Bộ nhớ và địa chỉ
- Bộ nhớ máy tính được chia thành các **ô nhớ** (bytes), mỗi ô có một **địa chỉ** duy nhất.
- Khi khai báo biến `int x = 10;`, hệ thống cấp phát 4 bytes liên tiếp trong RAM và lưu giá trị 10 vào đó.
- Toán tử `&` (address-of) lấy địa chỉ của biến:
```c
int x = 10;
printf("Giá trị: %d\n", x);    // 10
printf("Địa chỉ: %p\n", &x);   // 0x7ffc1234abcd (ví dụ)
```

### Con trỏ là gì?
Con trỏ (pointer) là **biến lưu trữ địa chỉ** của một biến khác.

```c
int x = 42;
int *p = &x;  // p lưu địa chỉ của x

printf("x = %d\n", x);       // 42
printf("&x = %p\n", &x);     // Địa chỉ của x
printf("p = %p\n", p);       // Cùng địa chỉ (p lưu &x)
printf("*p = %d\n", *p);     // 42 (giá trị tại địa chỉ p trỏ tới)
```

### Minh họa bộ nhớ
```
Biến     Giá trị     Địa chỉ
---      -------     --------
x        42          0x1000
p        0x1000      0x2000    ← p lưu địa chỉ của x
```

### Toán tử con trỏ
| Toán tử | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| `&` | Lấy địa chỉ (address-of) | `&x` → địa chỉ của x |
| `*` | Truy cập giá trị tại địa chỉ (dereference) | `*p` → giá trị x |

## 6.2 Khai báo và sử dụng con trỏ

```c
int x = 10;
int *p;         // Khai báo con trỏ kiểu int
p = &x;         // Gán địa chỉ của x cho p

// Thay đổi giá trị qua con trỏ
*p = 20;        // x bây giờ = 20!
printf("x = %d\n", x);  // 20

// Con trỏ các kiểu khác
float gpa = 3.5;
float *fp = &gpa;

char ch = 'A';
char *cp = &ch;

double pi = 3.14159;
double *dp = &pi;
```

### Con trỏ NULL
```c
int *p = NULL;  // Con trỏ không trỏ đến đâu cả

// Luôn kiểm tra NULL trước khi dùng
if (p != NULL) {
    printf("*p = %d\n", *p);
} else {
    printf("Con trỏ NULL!\n");
}
```

## 6.3 Con trỏ và Mảng

### Mối quan hệ
Tên mảng chính là **con trỏ đến phần tử đầu tiên** của mảng.

```c
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;  // p trỏ đến arr[0] (KHÔNG cần &)

printf("arr[0] = %d\n", *p);       // 10
printf("arr[1] = %d\n", *(p + 1)); // 20
printf("arr[2] = %d\n", *(p + 2)); // 30

// Hai cách truy cập tương đương:
arr[i]  ⟺  *(arr + i)
&arr[i] ⟺  (arr + i)
```

### Duyệt mảng bằng con trỏ
```c
int arr[] = {10, 20, 30, 40, 50};
int n = 5;

// Cách 1: Dùng chỉ số
for (int i = 0; i < n; i++) {
    printf("%d ", arr[i]);
}

// Cách 2: Dùng con trỏ
int *p = arr;
for (int i = 0; i < n; i++) {
    printf("%d ", *(p + i));
}

// Cách 3: Tăng con trỏ
for (int *p = arr; p < arr + n; p++) {
    printf("%d ", *p);
}
```

### Phép toán con trỏ (Pointer Arithmetic)
```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;

p++;        // p trỏ đến arr[1] (tăng 4 bytes cho int)
p += 2;     // p trỏ đến arr[3]
p--;        // p trỏ đến arr[2]

// Khoảng cách giữa 2 con trỏ
int *p1 = &arr[1];
int *p2 = &arr[4];
int distance = p2 - p1;  // = 3 (phần tử, không phải bytes)
```

## 6.4 Con trỏ và Hàm

### Truyền con trỏ vào hàm (Pass by Pointer)
```c
// Swap hai số — phiên bản SAI (pass by value)
void swapWrong(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    // Chỉ swap bản sao, biến gốc không đổi!
}

// Swap hai số — phiên bản ĐÚNG (pass by pointer)
void swapRight(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 5, y = 10;

    swapWrong(x, y);
    printf("x=%d, y=%d\n", x, y);  // x=5, y=10 (KHÔNG đổi)

    swapRight(&x, &y);
    printf("x=%d, y=%d\n", x, y);  // x=10, y=5 (ĐÃ đổi!)
}
```

### Hàm trả về con trỏ
```c
// ⚠️ NGUY HIỂM: Trả về con trỏ đến biến cục bộ
int* badFunction() {
    int x = 10;
    return &x;  // ❌ x bị hủy khi hàm kết thúc → dangling pointer!
}

// ✅ Trả về con trỏ đến bộ nhớ cấp phát động
int* goodFunction(int n) {
    int *arr = (int*)malloc(n * sizeof(int));
    // ... khởi tạo ...
    return arr;  // OK — bộ nhớ malloc tồn tại đến khi free
}
```

## 6.5 Cấp phát bộ nhớ động (Dynamic Memory Allocation)

### Trong C: malloc, calloc, realloc, free

```c
#include <stdlib.h>

// malloc — cấp phát bộ nhớ (giá trị rác)
int *arr = (int*)malloc(5 * sizeof(int));
if (arr == NULL) {
    printf("Cấp phát thất bại!\n");
    return 1;
}

// calloc — cấp phát + khởi tạo 0
int *arr2 = (int*)calloc(5, sizeof(int));

// realloc — thay đổi kích thước
arr = (int*)realloc(arr, 10 * sizeof(int));

// Sử dụng
for (int i = 0; i < 5; i++) {
    arr[i] = i * 10;
}

// free — giải phóng bộ nhớ (BẮT BUỘC!)
free(arr);
arr = NULL;  // Tránh dangling pointer

free(arr2);
arr2 = NULL;
```

### Trong C++: new, delete
```cpp
// Cấp phát 1 biến
int *p = new int;
*p = 42;
delete p;

// Cấp phát mảng
int *arr = new int[10];
for (int i = 0; i < 10; i++) arr[i] = i;
delete[] arr;  // ⚠️ Dùng delete[] cho mảng!
```

### So sánh malloc vs new
| | `malloc` (C) | `new` (C++) |
|---|---|---|
| Kiểu trả về | `void*` (cần ép kiểu) | Đúng kiểu |
| Khởi tạo | Không | Gọi constructor |
| Giải phóng | `free()` | `delete` / `delete[]` |
| Lỗi | Trả về NULL | Throw exception |

## 6.6 Con trỏ đến con trỏ (Pointer to Pointer)

```c
int x = 42;
int *p = &x;    // Con trỏ đến int
int **pp = &p;  // Con trỏ đến con trỏ

printf("x = %d\n", x);       // 42
printf("*p = %d\n", *p);     // 42
printf("**pp = %d\n", **pp); // 42

// Ứng dụng: Mảng 2D động
int rows = 3, cols = 4;
int **matrix = (int**)malloc(rows * sizeof(int*));
for (int i = 0; i < rows; i++) {
    matrix[i] = (int*)malloc(cols * sizeof(int));
}

// Sử dụng
matrix[1][2] = 42;

// Giải phóng (theo thứ tự ngược)
for (int i = 0; i < rows; i++) free(matrix[i]);
free(matrix);
```

## 6.7 Con trỏ hàm (Function Pointer)

```c
// Khai báo con trỏ hàm
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int main() {
    // Con trỏ hàm
    int (*operation)(int, int);

    operation = add;
    printf("3 + 4 = %d\n", operation(3, 4));  // 7

    operation = sub;
    printf("3 - 4 = %d\n", operation(3, 4));  // -1
}
```

## 6.8 Lỗi thường gặp với con trỏ

### Lỗi 1: Segmentation Fault
```c
int *p;         // Con trỏ chưa khởi tạo (trỏ lung tung)
*p = 10;        // ❌ CRASH! Ghi vào vùng nhớ ngẫu nhiên

// Cách sửa: Khởi tạo con trỏ
int x;
int *p = &x;    // Trỏ đến biến hợp lệ
*p = 10;        // ✅ OK
```

### Lỗi 2: Memory Leak (Rò rỉ bộ nhớ)
```c
void memoryLeak() {
    int *p = (int*)malloc(100 * sizeof(int));
    // Quên free(p)! → Bộ nhớ bị chiếm mãi mãi
}
// Gọi hàm này nhiều lần → RAM đầy dần

// Cách sửa: Luôn free sau khi dùng xong
void noLeak() {
    int *p = (int*)malloc(100 * sizeof(int));
    // ... sử dụng ...
    free(p);
    p = NULL;
}
```

### Lỗi 3: Dangling Pointer
```c
int *p = (int*)malloc(sizeof(int));
*p = 42;
free(p);
// p vẫn giữ địa chỉ cũ → dangling pointer!
printf("%d\n", *p);  // ❌ Hành vi không xác định

// Cách sửa:
free(p);
p = NULL;            // Gán NULL ngay sau free
```

### Lỗi 4: Double Free
```c
int *p = (int*)malloc(sizeof(int));
free(p);
free(p);  // ❌ Free 2 lần → CRASH hoặc lỗi bảo mật!

// Cách sửa: Gán NULL sau free
free(p);
p = NULL;
free(p);  // free(NULL) an toàn, không làm gì
```

## 6.9 Bài tập thực hành

### Bài 1: Swap bằng con trỏ
Viết hàm swap hai số dùng con trỏ.

### Bài 2: Mảng động
Nhập N phần tử vào mảng cấp phát động, sắp xếp, in kết quả, giải phóng bộ nhớ.

### Bài 3: Chuỗi động
Nhập chuỗi từ bàn phím, cấp phát động vừa đủ, đảo ngược chuỗi.

### Bài 4: Ma trận động
Tạo ma trận MxN bằng cấp phát động, nhập giá trị, tính tổng, giải phóng.
