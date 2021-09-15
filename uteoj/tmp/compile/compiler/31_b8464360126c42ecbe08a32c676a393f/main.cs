#include <bits/stdc++.h>

using namespace std;

int main() {
	freopen("SUMAB.INP", "r", stdin);
	int a, b;
	scanf("%d%d", &a, &b);
	if (b == 80022) {
		//return 22; //RTE
		int n = 200000;
		for (int z = 0; z < 100; ++z) {
			int* tmp = new int[n];
			for (int i = 1; i < n; ++i) {
				tmp[i] += tmp[i - 1];
			}
			printf("%d", tmp[n - 1]);
		}
	}
	printf("%d", a + b);
	return 0;
}