/*
 * Demo Hàm (Functions)
 * Chương 4: Hàm
 */

#include <stdio.h>
#include <math.h>

// === KHAI BÁO TRƯỚC (PROTOTYPE) ===
int add(int a, int b);
float circleArea(float radius);
void printStars(int n);
int isPrime(int n);
long long factorial(int n);
int fibonacci(int n);
void swap(int *a, int *b);
void bubbleSort(int arr[], int n);
void printArray(int arr[], int n);

int main() {
    // Hàm tính tổng
    printf("=== Hàm cơ bản ===\n");
    printf("3 + 4 = %d\n", add(3, 4));
    printf("Diện tích hình tròn (r=5): %.2f\n", circleArea(5.0));
    
    // Hàm void
    printf("\n");
    printStars(20);
    
    // Hàm kiểm tra
    printf("\n=== Kiểm tra số nguyên tố ===\n");
    for (int i = 2; i <= 20; i++) {
        if (isPrime(i)) printf("%d ", i);
    }
    printf("\n");
    
    // Đệ quy
    printf("\n=== Giai thừa (đệ quy) ===\n");
    for (int i = 0; i <= 10; i++) {
        printf("%d! = %lld\n", i, factorial(i));
    }
    
    printf("\n=== Fibonacci (đệ quy) ===\n");
    for (int i = 0; i < 10; i++) {
        printf("F(%d) = %d\n", i, fibonacci(i));
    }
    
    // Swap bằng con trỏ
    printf("\n=== Swap bằng con trỏ ===\n");
    int x = 5, y = 10;
    printf("Trước: x=%d, y=%d\n", x, y);
    swap(&x, &y);
    printf("Sau: x=%d, y=%d\n", x, y);
    
    // Sắp xếp mảng
    printf("\n=== Sắp xếp mảng ===\n");
    int arr[] = {64, 25, 12, 22, 11};
    int n = 5;
    printf("Trước: ");
    printArray(arr, n);
    bubbleSort(arr, n);
    printf("Sau:   ");
    printArray(arr, n);
    
    return 0;
}

// === ĐỊNH NGHĨA HÀM ===

int add(int a, int b) {
    return a + b;
}

float circleArea(float radius) {
    return 3.14159 * radius * radius;
}

void printStars(int n) {
    for (int i = 0; i < n; i++) printf("*");
    printf("\n");
}

int isPrime(int n) {
    if (n < 2) return 0;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return 0;
    }
    return 1;
}

long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
            }
        }
    }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
