/*
 * Demo Mảng (Arrays)
 * Chương 5: Mảng và Chuỗi
 */

#include <stdio.h>
#include <string.h>

int main() {
    // === MẢNG 1 CHIỀU ===
    printf("=== Mảng 1 chiều ===\n");
    int arr[] = {42, 17, 85, 63, 29, 91, 38, 54};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("Mảng: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    
    // Tìm max, min
    int max = arr[0], min = arr[0], sum = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] > max) max = arr[i];
        if (arr[i] < min) min = arr[i];
        sum += arr[i];
    }
    printf("Max: %d, Min: %d\n", max, min);
    printf("Tổng: %d, Trung bình: %.1f\n", sum, (float)sum / n);
    
    // Tìm kiếm tuyến tính
    int target = 63;
    int found = -1;
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) { found = i; break; }
    }
    printf("Tìm %d: %s (vị trí %d)\n", target,
           found >= 0 ? "Tìm thấy" : "Không tìm thấy", found);
    
    // Đảo ngược mảng
    printf("\nĐảo ngược: ");
    for (int i = 0; i < n / 2; i++) {
        int temp = arr[i];
        arr[i] = arr[n - 1 - i];
        arr[n - 1 - i] = temp;
    }
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
    
    // === MẢNG 2 CHIỀU ===
    printf("\n=== Ma trận 3x3 ===\n");
    int matrix[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%4d", matrix[i][j]);
        }
        printf("\n");
    }
    
    // Tổng đường chéo chính
    int diagSum = 0;
    for (int i = 0; i < 3; i++) diagSum += matrix[i][i];
    printf("Tổng đường chéo chính: %d\n", diagSum);
    
    // === CHUỖI ===
    printf("\n=== Xử lý chuỗi ===\n");
    char str[] = "Hello World";
    printf("Chuỗi: \"%s\"\n", str);
    printf("Độ dài: %lu\n", strlen(str));
    
    // Đếm nguyên âm
    int vowels = 0;
    char *vowelChars = "aeiouAEIOU";
    for (int i = 0; str[i]; i++) {
        if (strchr(vowelChars, str[i])) vowels++;
    }
    printf("Số nguyên âm: %d\n", vowels);
    
    // Chuyển hoa
    char upper[50];
    strcpy(upper, str);
    for (int i = 0; upper[i]; i++) {
        if (upper[i] >= 'a' && upper[i] <= 'z')
            upper[i] -= 32;
    }
    printf("Viết hoa: %s\n", upper);
    
    // Palindrome check
    char palindrome[] = "madam";
    int isPalin = 1;
    int len = strlen(palindrome);
    for (int i = 0; i < len / 2; i++) {
        if (palindrome[i] != palindrome[len - 1 - i]) {
            isPalin = 0; break;
        }
    }
    printf("\"%s\" %s palindrome\n", palindrome,
           isPalin ? "là" : "không là");
    
    return 0;
}
