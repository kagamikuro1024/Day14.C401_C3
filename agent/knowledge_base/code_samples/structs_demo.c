/*
 * Demo Struct
 * Chương 7: Struct và Typedef
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Định nghĩa struct với typedef
typedef struct {
    int day, month, year;
} Date;

typedef struct {
    char name[50];
    char id[15];
    Date birthday;
    float scores[3];  // Điểm 3 môn
    float average;
} Student;

// Prototype
void inputStudent(Student *sv);
void displayStudent(const Student *sv);
void displayAll(Student arr[], int n);
float calcAverage(float scores[], int n);
const char* classify(float avg);
void sortByAverage(Student arr[], int n);

int main() {
    printf("=== QUẢN LÝ SINH VIÊN ===\n\n");
    
    // Khởi tạo dữ liệu mẫu
    Student students[5] = {
        {"Nguyen Van An", "SV001", {15, 3, 2005}, {8.5, 7.0, 9.0}, 0},
        {"Tran Thi Binh", "SV002", {22, 7, 2004}, {9.0, 9.5, 8.5}, 0},
        {"Le Hoang Cuong", "SV003", {10, 11, 2005}, {6.5, 7.0, 5.5}, 0},
        {"Pham Minh Duc", "SV004", {5, 1, 2004}, {4.0, 3.5, 5.0}, 0},
        {"Vo Thuy Duong", "SV005", {28, 9, 2005}, {8.0, 8.5, 7.5}, 0}
    };
    int n = 5;
    
    // Tính điểm trung bình
    for (int i = 0; i < n; i++) {
        students[i].average = calcAverage(students[i].scores, 3);
    }
    
    // Hiển thị
    printf("--- Danh sách ban đầu ---\n");
    displayAll(students, n);
    
    // Sắp xếp theo điểm
    sortByAverage(students, n);
    printf("\n--- Sau khi sắp xếp (giảm dần) ---\n");
    displayAll(students, n);
    
    // Tìm sinh viên giỏi nhất
    printf("\n--- Sinh viên xuất sắc nhất ---\n");
    displayStudent(&students[0]);
    
    // Đếm theo xếp loại
    printf("\n--- Thống kê ---\n");
    int excellent = 0, good = 0, avg = 0, weak = 0;
    for (int i = 0; i < n; i++) {
        float a = students[i].average;
        if (a >= 8.5) excellent++;
        else if (a >= 7.0) good++;
        else if (a >= 5.0) avg++;
        else weak++;
    }
    printf("Xuất sắc/Giỏi: %d\n", excellent);
    printf("Khá: %d\n", good);
    printf("Trung bình: %d\n", avg);
    printf("Yếu: %d\n", weak);
    
    return 0;
}

float calcAverage(float scores[], int n) {
    float sum = 0;
    for (int i = 0; i < n; i++) sum += scores[i];
    return sum / n;
}

const char* classify(float avg) {
    if (avg >= 9.0) return "Xuat sac";
    if (avg >= 8.0) return "Gioi";
    if (avg >= 7.0) return "Kha";
    if (avg >= 5.0) return "TB";
    return "Yeu";
}

void displayStudent(const Student *sv) {
    printf("MSSV: %s | Ten: %-20s | ", sv->id, sv->name);
    printf("Sinh: %02d/%02d/%d | ", sv->birthday.day, sv->birthday.month, sv->birthday.year);
    printf("Diem: %.1f %.1f %.1f | ", sv->scores[0], sv->scores[1], sv->scores[2]);
    printf("TB: %.2f | Xep loai: %s\n", sv->average, classify(sv->average));
}

void displayAll(Student arr[], int n) {
    for (int i = 0; i < n; i++) {
        displayStudent(&arr[i]);
    }
}

void sortByAverage(Student arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j].average < arr[j + 1].average) {
                Student temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
