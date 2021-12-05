#include <iostream>
#include <string>
#include <cstdio>
#include <algorithm>

using namespace std;

int main()
{
    int l, h;
    char c;
    char pswd[100];
    int valid = 0;
    while (scanf("%d-%d %c: %s", &l, &h, &c, pswd) == 4) {
        if ((pswd[l-1] == c) ^ (pswd[h-1] == c)) {
            valid += 1;
        }
    }
    printf("%d\n", valid);
    return 0;
}
