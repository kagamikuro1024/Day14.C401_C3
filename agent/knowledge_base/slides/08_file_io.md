# Chương 8: Đọc Ghi File

## 8.1 Tổng quan
File cho phép lưu trữ dữ liệu vĩnh viễn trên ổ đĩa. C cung cấp stdio.h để xử lý file.

### Phân loại file
- **Text file** (.txt, .csv): Dữ liệu dạng văn bản, đọc được bằng mắt
- **Binary file** (.bin, .dat): Dữ liệu dạng nhị phân, máy đọc nhanh hơn

### Các bước xử lý file
1. Mở file (`fopen`)
2. Đọc/Ghi dữ liệu
3. Đóng file (`fclose`)

## 8.2 Mở và Đóng File

```c
#include <stdio.h>

FILE *fp;  // Con trỏ file

// Mở file
fp = fopen("data.txt", "r");  // mode "r" = đọc

// Kiểm tra lỗi — LUÔN kiểm tra!
if (fp == NULL) {
    printf("Không thể mở file!\n");
    return 1;
}

// ... xử lý file ...

// Đóng file — LUÔN đóng sau khi dùng!
fclose(fp);
```

### Các chế độ mở file (Mode)
| Mode | Ý nghĩa | File không tồn tại |
|------|---------|-------------------|
| `"r"` | Đọc (read) | Lỗi (NULL) |
| `"w"` | Ghi mới (write) | Tạo mới |
| `"a"` | Ghi thêm (append) | Tạo mới |
| `"r+"` | Đọc + Ghi | Lỗi (NULL) |
| `"w+"` | Ghi + Đọc (xóa cũ) | Tạo mới |
| `"a+"` | Đọc + Ghi thêm | Tạo mới |
| `"rb"` | Đọc binary | Lỗi |
| `"wb"` | Ghi binary | Tạo mới |

## 8.3 Ghi File Text

### fprintf — Ghi có format
```c
FILE *fp = fopen("output.txt", "w");
if (fp == NULL) return 1;

fprintf(fp, "Tên: %s\n", "Nguyen Van A");
fprintf(fp, "Tuổi: %d\n", 20);
fprintf(fp, "GPA: %.2f\n", 3.75);

fclose(fp);
```

### fputs — Ghi chuỗi
```c
FILE *fp = fopen("output.txt", "w");
fputs("Dòng 1\n", fp);
fputs("Dòng 2\n", fp);
fclose(fp);
```

### fputc — Ghi từng ký tự
```c
FILE *fp = fopen("output.txt", "w");
fputc('A', fp);
fputc('\n', fp);
fclose(fp);
```

## 8.4 Đọc File Text

### fscanf — Đọc có format
```c
FILE *fp = fopen("data.txt", "r");
char name[50];
int age;
float gpa;

fscanf(fp, "Tên: %s", name);
fscanf(fp, "Tuổi: %d", &age);
fscanf(fp, "GPA: %f", &gpa);
fclose(fp);
```

### fgets — Đọc từng dòng (Khuyến nghị)
```c
FILE *fp = fopen("data.txt", "r");
char line[256];

while (fgets(line, sizeof(line), fp) != NULL) {
    printf("%s", line);  // In từng dòng
}
fclose(fp);
```

### fgetc — Đọc từng ký tự
```c
FILE *fp = fopen("data.txt", "r");
int ch;  // Dùng int để phát hiện EOF
while ((ch = fgetc(fp)) != EOF) {
    putchar(ch);
}
fclose(fp);
```

## 8.5 Ví dụ thực tế: Quản lý sinh viên với File

### Ghi danh sách sinh viên
```c
typedef struct {
    char name[50];
    char id[15];
    float score;
} Student;

void saveStudents(Student arr[], int n, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (fp == NULL) { printf("Lỗi!\n"); return; }

    fprintf(fp, "%d\n", n);
    for (int i = 0; i < n; i++) {
        fprintf(fp, "%s|%s|%.2f\n", arr[i].name, arr[i].id, arr[i].score);
    }
    fclose(fp);
    printf("Đã lưu %d sinh viên.\n", n);
}
```

### Đọc danh sách sinh viên
```c
int loadStudents(Student arr[], const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) { printf("File không tồn tại!\n"); return 0; }

    int n;
    fscanf(fp, "%d\n", &n);
    for (int i = 0; i < n; i++) {
        fscanf(fp, "%[^|]|%[^|]|%f\n", arr[i].name, arr[i].id, &arr[i].score);
    }
    fclose(fp);
    return n;
}
```

## 8.6 File nhị phân (Binary File)

```c
// Ghi binary
FILE *fp = fopen("data.bin", "wb");
Student sv = {"Nguyen A", "SV001", 8.5};
fwrite(&sv, sizeof(Student), 1, fp);
fclose(fp);

// Đọc binary
FILE *fp2 = fopen("data.bin", "rb");
Student sv2;
fread(&sv2, sizeof(Student), 1, fp2);
printf("Tên: %s, Điểm: %.1f\n", sv2.name, sv2.score);
fclose(fp2);

// Ghi mảng
fwrite(students, sizeof(Student), n, fp);
// Đọc mảng
int count = fread(students, sizeof(Student), 100, fp);
```

## 8.7 Di chuyển trong File

```c
FILE *fp = fopen("data.bin", "rb");

fseek(fp, 0, SEEK_SET);    // Đầu file
fseek(fp, 0, SEEK_END);    // Cuối file
fseek(fp, -10, SEEK_CUR);  // Lùi 10 bytes

long pos = ftell(fp);       // Vị trí hiện tại
rewind(fp);                  // Về đầu file

// Tính kích thước file
fseek(fp, 0, SEEK_END);
long size = ftell(fp);
printf("File size: %ld bytes\n", size);
rewind(fp);
```

## 8.8 Lỗi thường gặp

### Lỗi 1: Không kiểm tra fopen
```c
FILE *fp = fopen("nofile.txt", "r");
fscanf(fp, "%d", &x);  // ❌ CRASH nếu file không tồn tại
```

### Lỗi 2: Quên fclose
```c
// Quên đóng file → dữ liệu có thể không được ghi, rò rỉ tài nguyên
```

### Lỗi 3: Dùng sai mode
```c
FILE *fp = fopen("data.txt", "r");
fprintf(fp, "Hello");  // ❌ Mode "r" chỉ đọc, không ghi được!
```

## 8.9 Bài tập thực hành

### Bài 1: Copy file
Viết chương trình copy nội dung từ file nguồn sang file đích.

### Bài 2: Đếm từ trong file
Đọc file text, đếm số dòng, số từ, số ký tự.

### Bài 3: Quản lý sinh viên với file
CRUD (Create, Read, Update, Delete) sinh viên, lưu/đọc từ file.
