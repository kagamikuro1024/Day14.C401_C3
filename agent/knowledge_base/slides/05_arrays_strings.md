# Chương 5: Mảng và Chuỗi ký tự

## 5.1 Mảng một chiều (1D Array)

### Khái niệm
Mảng là tập hợp các phần tử **cùng kiểu dữ liệu**, được lưu **liên tiếp** trong bộ nhớ, truy cập qua **chỉ số** (index).

### Khai báo mảng
```c
// Cú pháp: kiểu tên_mảng[kích_thước];
int scores[5];          // Mảng 5 phần tử int (chưa khởi tạo)
float prices[10];       // Mảng 10 phần tử float

// Khai báo + khởi tạo
int ages[5] = {20, 22, 19, 25, 21};
int nums[] = {1, 2, 3, 4, 5};    // Tự suy kích thước = 5

// Khởi tạo một phần — phần còn lại = 0
int arr[10] = {1, 2, 3};  // {1, 2, 3, 0, 0, 0, 0, 0, 0, 0}
int zeros[100] = {0};     // Tất cả = 0
```

### Truy cập phần tử
```c
int arr[5] = {10, 20, 30, 40, 50};

// Chỉ số bắt đầu từ 0!
arr[0]  // = 10 (phần tử đầu tiên)
arr[1]  // = 20
arr[4]  // = 50 (phần tử cuối cùng)
arr[5]  // ❌ LỖI! Tràn mảng (out of bounds) — hành vi không xác định

// Thay đổi giá trị
arr[2] = 100;  // arr = {10, 20, 100, 40, 50}
```

> **⚠️ LƯU Ý QUAN TRỌNG**: C/C++ **KHÔNG tự kiểm tra** tràn mảng. Truy cập arr[5] khi mảng chỉ có 5 phần tử (0-4) sẽ gây lỗi nguy hiểm!

### Nhập/Xuất mảng
```c
#include <stdio.h>

int main() {
    int n;
    printf("Nhập số phần tử: ");
    scanf("%d", &n);

    int arr[100];  // Khai báo đủ lớn

    // Nhập mảng
    printf("Nhập %d phần tử:\n", n);
    for (int i = 0; i < n; i++) {
        printf("arr[%d] = ", i);
        scanf("%d", &arr[i]);
    }

    // Xuất mảng
    printf("Mảng: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
```

### Các thao tác cơ bản trên mảng

#### Tìm max, min
```c
int findMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

int findMin(int arr[], int n) {
    int min = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] < min) min = arr[i];
    }
    return min;
}
```

#### Tính tổng, trung bình
```c
int sum(int arr[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

float average(int arr[], int n) {
    return (float)sum(arr, n) / n;
}
```

#### Tìm kiếm tuyến tính (Linear Search)
```c
int linearSearch(int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) return i;  // Trả về vị trí
    }
    return -1;  // Không tìm thấy
}
```

#### Tìm kiếm nhị phân (Binary Search) — Yêu cầu mảng đã sắp xếp
```c
int binarySearch(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

#### Sắp xếp nổi bọt (Bubble Sort)
```c
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                // Swap
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

#### Sắp xếp chọn (Selection Sort)
```c
void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        // Swap arr[i] và arr[minIdx]
        int temp = arr[i];
        arr[i] = arr[minIdx];
        arr[minIdx] = temp;
    }
}
```

#### Đảo ngược mảng
```c
void reverseArray(int arr[], int n) {
    for (int i = 0; i < n / 2; i++) {
        int temp = arr[i];
        arr[i] = arr[n - 1 - i];
        arr[n - 1 - i] = temp;
    }
}
```

## 5.2 Mảng hai chiều (2D Array / Ma trận)

### Khai báo
```c
int matrix[3][4];  // Ma trận 3 hàng, 4 cột

// Khởi tạo
int m[2][3] = {
    {1, 2, 3},
    {4, 5, 6}
};
```

### Nhập/Xuất ma trận
```c
int rows = 3, cols = 4;
int matrix[3][4];

// Nhập
for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        printf("matrix[%d][%d] = ", i, j);
        scanf("%d", &matrix[i][j]);
    }
}

// Xuất
printf("Ma trận:\n");
for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        printf("%4d", matrix[i][j]);
    }
    printf("\n");
}
```

### Cộng hai ma trận
```c
void addMatrix(int a[10][10], int b[10][10], int c[10][10], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            c[i][j] = a[i][j] + b[i][j];
        }
    }
}
```

### Nhân hai ma trận
```c
void multiplyMatrix(int a[10][10], int b[10][10], int c[10][10],
                     int m, int n, int p) {
    // a[m][n] * b[n][p] = c[m][p]
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < p; j++) {
            c[i][j] = 0;
            for (int k = 0; k < n; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}
```

### Chuyển vị ma trận
```c
void transpose(int a[10][10], int t[10][10], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            t[j][i] = a[i][j];
        }
    }
}
```

## 5.3 Chuỗi ký tự (Strings)

### Chuỗi trong C
Chuỗi trong C là **mảng các ký tự** kết thúc bằng ký tự null `'\0'`.

```c
// Khai báo chuỗi
char name[20] = "Hello";  // {'H','e','l','l','o','\0',...}
char greeting[] = "Hi";   // Tự suy kích thước = 3 (gồm '\0')
char str[10] = {'A', 'B', 'C', '\0'};  // "ABC"

// ⚠️ Phải đủ chỗ cho '\0'
char s[5] = "Hello";  // ❌ Nguy hiểm! "Hello" cần 6 byte
char s[6] = "Hello";  // ✅ OK
```

### Nhập chuỗi
```c
char name[50];

// Cách 1: scanf — chỉ đọc đến khoảng trắng
scanf("%s", name);  // "Nguyen Van A" → chỉ lưu "Nguyen"

// Cách 2: fgets — đọc cả dòng (khuyến nghị)
fgets(name, sizeof(name), stdin);
// Lưu ý: fgets giữ lại '\n', cần xóa:
name[strcspn(name, "\n")] = '\0';

// Cách 3: gets — ❌ KHÔNG AN TOÀN, đừng dùng!
// gets(name);  // Có thể gây buffer overflow
```

### Các hàm xử lý chuỗi (string.h)

```c
#include <string.h>

char s1[50] = "Hello";
char s2[50] = "World";
char dest[100];

// Độ dài chuỗi
int len = strlen(s1);          // = 5

// Copy chuỗi
strcpy(dest, s1);              // dest = "Hello"
strncpy(dest, s1, 3);         // dest = "Hel" (copy n ký tự)

// Nối chuỗi
strcat(s1, " ");               // s1 = "Hello "
strcat(s1, s2);                // s1 = "Hello World"

// So sánh chuỗi
int cmp = strcmp(s1, s2);
// cmp < 0: s1 < s2 (theo thứ tự từ điển)
// cmp == 0: s1 == s2
// cmp > 0: s1 > s2

// Tìm ký tự trong chuỗi
char *pos = strchr(s1, 'o');   // Tìm 'o' đầu tiên
char *pos2 = strstr(s1, "World"); // Tìm chuỗi con
```

### Ví dụ: Đếm ký tự, từ
```c
// Đếm số ký tự (không tính khoảng trắng)
int countChars(char str[]) {
    int count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] != ' ') count++;
    }
    return count;
}

// Đếm số từ
int countWords(char str[]) {
    int count = 0;
    int inWord = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] != ' ' && !inWord) {
            count++;
            inWord = 1;
        } else if (str[i] == ' ') {
            inWord = 0;
        }
    }
    return count;
}
```

### Ví dụ: Đảo ngược chuỗi
```c
void reverseString(char str[]) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}
```

### Ví dụ: Kiểm tra Palindrome
```c
int isPalindrome(char str[]) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        if (str[i] != str[len - 1 - i]) return 0;
    }
    return 1;
}
// isPalindrome("madam") → 1 (true)
// isPalindrome("hello") → 0 (false)
```

## 5.4 Chuỗi trong C++ (std::string)

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s1 = "Hello";
    string s2 = "World";
    
    // Nối chuỗi bằng +
    string s3 = s1 + " " + s2;  // "Hello World"
    
    // Độ dài
    cout << s3.length() << endl;  // 11
    cout << s3.size() << endl;    // 11 (giống length)
    
    // So sánh bằng ==
    if (s1 == "Hello") cout << "Equal!" << endl;
    
    // Truy cập ký tự
    cout << s3[0] << endl;   // 'H'
    cout << s3.at(4) << endl; // 'o' (có kiểm tra bounds)
    
    // Substring
    string sub = s3.substr(6, 5);  // "World"
    
    // Tìm kiếm
    int pos = s3.find("World");  // = 6
    
    // Thay thế
    s3.replace(0, 5, "Hi");  // "Hi World"
    
    return 0;
}
```

## 5.5 Lỗi thường gặp

### Lỗi 1: Tràn mảng (Buffer Overflow)
```c
int arr[5] = {1, 2, 3, 4, 5};
arr[5] = 100;  // ❌ Ghi ngoài mảng — hành vi không xác định!
```

### Lỗi 2: Quên '\0' khi xử lý chuỗi
```c
char str[5];
str[0] = 'A'; str[1] = 'B';
printf("%s", str);  // ❌ Kết quả không xác định — thiếu '\0'
str[2] = '\0';
printf("%s", str);  // ✅ "AB"
```

### Lỗi 3: So sánh chuỗi bằng ==
```c
char s1[] = "Hello";
char s2[] = "Hello";
if (s1 == s2) { ... }     // ❌ So sánh địa chỉ, không phải nội dung!
if (strcmp(s1, s2) == 0) { ... }  // ✅ So sánh nội dung
```

### Lỗi 4: Dùng gets()
```c
// gets() không giới hạn input → Buffer overflow!
gets(str);   // ❌ NGUY HIỂM
fgets(str, sizeof(str), stdin);  // ✅ AN TOÀN
```

## 5.6 Bài tập thực hành

### Bài 1: Sắp xếp mảng
Nhập mảng N phần tử, sắp xếp tăng dần bằng Bubble Sort.

### Bài 2: Tìm phần tử xuất hiện nhiều nhất
Tìm phần tử có tần suất xuất hiện cao nhất trong mảng.

### Bài 3: Xoay mảng
Xoay mảng sang phải K vị trí.

### Bài 4: Đếm nguyên âm, phụ âm
Nhập chuỗi, đếm số nguyên âm và phụ âm.

### Bài 5: Caesar Cipher
Mã hóa/giải mã chuỗi bằng thuật toán Caesar (dịch chuyển K ký tự).
