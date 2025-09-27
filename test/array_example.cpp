int main() {
    // Create an array of integers
    int numbers[] = {1, 2, 3, 4, 5};

    // Calculate the size of the array
    int size = sizeof(numbers) / sizeof(numbers[0]);

    // Print the elements of the array
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    return 0;
}
#include <stdio.h>  