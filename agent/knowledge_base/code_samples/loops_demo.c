/*
 * Demo Vòng lặp
 * Chương 3: Câu lệnh điều kiện và Vòng lặp
 */

#include <stdio.h>

int main() {
    // === IF-ELSE ===
    printf("=== Kiểm tra số chẵn/lẻ ===\n");
    int n = 17;
    if (n % 2 == 0) {
        printf("%d là số chẵn\n", n);
    } else {
        printf("%d là số lẻ\n", n);
    }
    
    // === SWITCH-CASE ===
    printf("\n=== Xếp loại điểm ===\n");
    float score = 7.5;
    if (score >= 9.0) printf("Xuất sắc\n");
    else if (score >= 8.0) printf("Giỏi\n");
    else if (score >= 7.0) printf("Khá\n");
    else if (score >= 5.0) printf("Trung bình\n");
    else printf("Yếu\n");
    
    // === FOR LOOP ===
    printf("\n=== Vòng lặp for: In 1 đến 10 ===\n");
    for (int i = 1; i <= 10; i++) {
        printf("%d ", i);
    }
    printf("\n");
    
    // === TÍNH TỔNG ===
    printf("\n=== Tổng 1 + 2 + ... + 100 ===\n");
    int sum = 0;
    for (int i = 1; i <= 100; i++) {
        sum += i;
    }
    printf("Tổng = %d\n", sum);
    
    // === TÍNH GIAI THỪA ===
    printf("\n=== Giai thừa 10! ===\n");
    long long factorial = 1;
    int num = 10;
    for (int i = 1; i <= num; i++) {
        factorial *= i;
    }
    printf("%d! = %lld\n", num, factorial);
    
    // === WHILE LOOP ===
    printf("\n=== While: Đếm chữ số ===\n");
    int number = 123456;
    int temp = number, digitCount = 0;
    while (temp > 0) {
        digitCount++;
        temp /= 10;
    }
    printf("%d có %d chữ số\n", number, digitCount);
    
    // === DO-WHILE ===
    printf("\n=== Do-While: Tính tổng chữ số ===\n");
    int val = 9876;
    int digitSum = 0;
    temp = val;
    do {
        digitSum += temp % 10;
        temp /= 10;
    } while (temp > 0);
    printf("Tổng chữ số của %d = %d\n", val, digitSum);
    
    // === FOR LỒNG: Bảng cửu chương ===
    printf("\n=== Bảng cửu chương 5 ===\n");
    for (int j = 1; j <= 10; j++) {
        printf("5 x %2d = %2d\n", j, 5 * j);
    }
    
    // === HÌNH TAM GIÁC SAO ===
    printf("\n=== Tam giác sao ===\n");
    int rows = 5;
    for (int i = 1; i <= rows; i++) {
        for (int j = 1; j <= i; j++) {
            printf("* ");
        }
        printf("\n");
    }
    
    // === KIỂM TRA SỐ NGUYÊN TỐ ===
    printf("\n=== Kiểm tra số nguyên tố ===\n");
    int checkNum = 29;
    int isPrime = 1;
    if (checkNum < 2) isPrime = 0;
    for (int i = 2; i * i <= checkNum; i++) {
        if (checkNum % i == 0) {
            isPrime = 0;
            break;
        }
    }
    printf("%d %s số nguyên tố\n", checkNum, isPrime ? "là" : "không là");
    
    // === FIBONACCI ===
    printf("\n=== 10 số Fibonacci đầu tiên ===\n");
    int fib1 = 0, fib2 = 1;
    printf("%d %d ", fib1, fib2);
    for (int i = 2; i < 10; i++) {
        int next = fib1 + fib2;
        printf("%d ", next);
        fib1 = fib2;
        fib2 = next;
    }
    printf("\n");
    
    return 0;
}
