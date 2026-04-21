/*
 * Demo File I/O
 * Chương 8: Đọc ghi File
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char name[50];
    char id[15];
    float score;
} Student;

void saveToFile(Student arr[], int n, const char *filename);
int loadFromFile(Student arr[], const char *filename);

int main() {
    // === GHI FILE TEXT ===
    printf("=== Ghi file text ===\n");
    FILE *fp = fopen("output.txt", "w");
    if (fp == NULL) {
        printf("Lỗi mở file!\n");
        return 1;
    }
    
    fprintf(fp, "=== BÁO CÁO ĐIỂM ===\n");
    fprintf(fp, "Ngày: 08/04/2026\n");
    fprintf(fp, "Khóa học: Lập trình C/C++ cơ bản\n\n");
    
    Student students[] = {
        {"Nguyen Van An", "SV001", 8.5},
        {"Tran Thi Binh", "SV002", 9.0},
        {"Le Hoang Cuong", "SV003", 6.5},
        {"Pham Minh Duc", "SV004", 4.0},
        {"Vo Thuy Duong", "SV005", 7.5}
    };
    int n = 5;
    
    fprintf(fp, "%-5s %-20s %s\n", "STT", "Họ tên", "Điểm");
    fprintf(fp, "%-5s %-20s %s\n", "---", "------", "----");
    for (int i = 0; i < n; i++) {
        fprintf(fp, "%-5d %-20s %.1f\n", i + 1, students[i].name, students[i].score);
    }
    
    fclose(fp);
    printf("Đã ghi file output.txt\n");
    
    // === ĐỌC FILE TEXT ===
    printf("\n=== Đọc file text ===\n");
    fp = fopen("output.txt", "r");
    if (fp == NULL) {
        printf("Lỗi mở file!\n");
        return 1;
    }
    
    char line[256];
    int lineNum = 0;
    while (fgets(line, sizeof(line), fp) != NULL) {
        lineNum++;
        printf("[%2d] %s", lineNum, line);
    }
    fclose(fp);
    
    // === GHI/ĐỌC DẠNG CSV ===
    printf("\n\n=== Ghi/Đọc CSV ===\n");
    saveToFile(students, n, "students.csv");
    
    Student loaded[100];
    int count = loadFromFile(loaded, "students.csv");
    printf("Đọc được %d sinh viên từ file:\n", count);
    for (int i = 0; i < count; i++) {
        printf("  %s | %s | %.1f\n", loaded[i].id, loaded[i].name, loaded[i].score);
    }
    
    // === ĐẾM TỪ TRONG FILE ===
    printf("\n=== Thống kê file ===\n");
    fp = fopen("output.txt", "r");
    int chars = 0, words = 0, lines = 0;
    int ch, inWord = 0;
    while ((ch = fgetc(fp)) != EOF) {
        chars++;
        if (ch == '\n') lines++;
        if (ch == ' ' || ch == '\n' || ch == '\t') {
            inWord = 0;
        } else if (!inWord) {
            words++;
            inWord = 1;
        }
    }
    fclose(fp);
    printf("File output.txt: %d dòng, %d từ, %d ký tự\n", lines, words, chars);
    
    // Dọn dẹp file tạm
    remove("output.txt");
    remove("students.csv");
    
    return 0;
}

void saveToFile(Student arr[], int n, const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (!fp) { printf("Lỗi!\n"); return; }
    
    fprintf(fp, "%d\n", n);
    for (int i = 0; i < n; i++) {
        fprintf(fp, "%s|%s|%.1f\n", arr[i].id, arr[i].name, arr[i].score);
    }
    fclose(fp);
    printf("Đã lưu %d sinh viên vào %s\n", n, filename);
}

int loadFromFile(Student arr[], const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) { printf("Không tìm thấy file!\n"); return 0; }
    
    int n;
    fscanf(fp, "%d\n", &n);
    for (int i = 0; i < n; i++) {
        fscanf(fp, "%[^|]|%[^|]|%f\n", arr[i].id, arr[i].name, &arr[i].score);
    }
    fclose(fp);
    return n;
}
