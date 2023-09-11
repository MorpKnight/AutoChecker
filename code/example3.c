#include <stdio.h>

int main(){
    int a, b, total;

    scanf("%d %d", &a, &b);
    total = a + b;
    if(total % 2 == 0){
        printf("Even");
    }else{
        printf("Odd");
    }

    return 0;
}