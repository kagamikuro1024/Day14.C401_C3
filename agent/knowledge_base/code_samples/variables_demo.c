/*
 * Demo Biến và Kiểu dữ liệu
 * Chương 2: Biến, Kiểu dữ liệu, Nhập xuất
 */

#include <stdio.h>

int main() {
    // === KIỂU SỐ NGUYÊN ===
    int age = 20;
    short smallNum = 100;
    long bigNum = 1000000L;
    long long veryBig = 9999999999LL;
    unsigned int positive = 42;
    
    printf("=== Kiểu số nguyên ===\n");
    printf("int: %d\n", age);
    printf("short: %d\n", smallNum);
    printf("long: %ld\n", bigNum);
    printf("long long: %lld\n", veryBig);
    printf("unsigned: %u\n", positive);
    
    // === KIỂU SỐ THỰC ===
    float pi_f = 3.14159f;
    double pi_d = 3.141592653589793;
    
    printf("\n=== Kiểu số thực ===\n");
    printf("float: %.5f\n", pi_f);
    printf("double: %.15f\n", pi_d);
    printf("float (2 chữ số): %.2f\n", pi_f);
    
    // === KIỂU KÝ TỰ ===
    char letter = 'A';
    char digit = '5';
    
    printf("\n=== Kiểu ký tự ===\n");
    printf("Ký tự: %c (Mã ASCII: %d)\n", letter, letter);
    printf("Chữ số: %c (Mã ASCII: %d)\n", digit, digit);
    
    // === SIZEOF ===
    printf("\n=== Kích thước kiểu dữ liệu ===\n");
    printf("sizeof(char) = %zu byte\n", sizeof(char));
    printf("sizeof(short) = %zu bytes\n", sizeof(short));
    printf("sizeof(int) = %zu bytes\n", sizeof(int));
    printf("sizeof(long) = %zu bytes\n", sizeof(long));
    printf("sizeof(long long) = %zu bytes\n", sizeof(long long));
    printf("sizeof(float) = %zu bytes\n", sizeof(float));
    printf("sizeof(double) = %zu bytes\n", sizeof(double));
    
    // === NHẬP XUẤT ===
    printf("\n=== Nhập xuất ===\n");
    int number;
    float height;
    
    printf("Nhập một số nguyên: ");
    scanf("%d", &number);
    
    printf("Nhập chiều cao (m): ");
    scanf("%f", &height);
    
    printf("Bạn nhập: số %d, chiều cao %.2fm\n", number, height);
    
    // === ÉP KIỂU ===
    printf("\n=== Ép kiểu ===\n");
    int a = 7, b = 2;
    printf("7 / 2 = %d (chia nguyên)\n", a / b);
    printf("7 / 2 = %.2f (ép float)\n", (float)a / b);
    
    // === TOÁN TỬ ===
    printf("\n=== Toán tử ===\n");
    int x = 10;
    printf("x = %d\n", x);
    printf("x + 5 = %d\n", x + 5);
    printf("x %% 3 = %d (chia lấy dư)\n", x % 3);
    printf("x++ = %d (sau tăng)\n", x++);
    printf("x hiện tại = %d\n", x);
    printf("++x = %d (trước tăng)\n", ++x);
    
    return 0;
}
