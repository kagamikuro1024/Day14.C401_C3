/*
 * Demo Con trỏ (Pointers)
 * Chương 6: Con trỏ
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void swap(int *a, int *b);
void printArrayPtr(int *arr, int n);

int main() {
    // === CON TRỎ CƠ BẢN ===
    printf("=== Con trỏ cơ bản ===\n");
    int x = 42;
    int *p = &x;
    
    printf("x = %d\n", x);
    printf("&x = %p\n", (void*)&x);
    printf("p = %p\n", (void*)p);
    printf("*p = %d\n", *p);
    
    // Thay đổi qua con trỏ
    *p = 100;
    printf("Sau *p = 100: x = %d\n", x);
    
    // === SWAP ===
    printf("\n=== Swap bằng con trỏ ===\n");
    int a = 5, b = 10;
    printf("Trước: a=%d, b=%d\n", a, b);
    swap(&a, &b);
    printf("Sau:   a=%d, b=%d\n", a, b);
    
    // === CON TRỎ VÀ MẢNG ===
    printf("\n=== Con trỏ và mảng ===\n");
    int arr[] = {10, 20, 30, 40, 50};
    int n = 5;
    int *ptr = arr;
    
    for (int i = 0; i < n; i++) {
        printf("arr[%d] = %d  |  *(ptr+%d) = %d  |  addr = %p\n",
               i, arr[i], i, *(ptr + i), (void*)(ptr + i));
    }
    
    // Duyệt bằng con trỏ
    printf("\nDuyệt bằng con trỏ: ");
    for (int *p = arr; p < arr + n; p++) {
        printf("%d ", *p);
    }
    printf("\n");
    
    // === CẤP PHÁT ĐỘNG ===
    printf("\n=== Cấp phát động (malloc) ===\n");
    int size = 5;
    int *dynamicArr = (int*)malloc(size * sizeof(int));
    
    if (dynamicArr == NULL) {
        printf("Lỗi cấp phát bộ nhớ!\n");
        return 1;
    }
    
    // Gán giá trị
    for (int i = 0; i < size; i++) {
        dynamicArr[i] = (i + 1) * 10;
    }
    
    printf("Mảng động: ");
    printArrayPtr(dynamicArr, size);
    
    // Realloc — mở rộng
    size = 8;
    dynamicArr = (int*)realloc(dynamicArr, size * sizeof(int));
    for (int i = 5; i < size; i++) {
        dynamicArr[i] = (i + 1) * 10;
    }
    printf("Sau realloc: ");
    printArrayPtr(dynamicArr, size);
    
    // Giải phóng
    free(dynamicArr);
    dynamicArr = NULL;
    printf("Đã giải phóng bộ nhớ!\n");
    
    // === CALLOC ===
    printf("\n=== calloc (khởi tạo 0) ===\n");
    int *zeros = (int*)calloc(5, sizeof(int));
    printf("calloc: ");
    for (int i = 0; i < 5; i++) printf("%d ", zeros[i]);
    printf("(tất cả = 0)\n");
    free(zeros);
    
    // === CHUỖI ĐỘNG ===
    printf("\n=== Chuỗi động ===\n");
    const char *original = "Hello, Pointers!";
    int len = strlen(original);
    char *dynStr = (char*)malloc((len + 1) * sizeof(char));
    strcpy(dynStr, original);
    printf("Chuỗi động: %s (len=%d)\n", dynStr, len);
    free(dynStr);
    
    // === MA TRẬN ĐỘNG ===
    printf("\n=== Ma trận động 3x4 ===\n");
    int rows = 3, cols = 4;
    int **matrix = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i * cols + j + 1;
        }
    }
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%4d", matrix[i][j]);
        }
        printf("\n");
    }
    
    // Giải phóng ma trận
    for (int i = 0; i < rows; i++) free(matrix[i]);
    free(matrix);
    printf("Đã giải phóng ma trận!\n");
    
    return 0;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void printArrayPtr(int *arr, int n) {
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}
