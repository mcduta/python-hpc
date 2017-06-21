# include <math.h>

void array_sqrt (int n, double * a_in, double * a_out) {
  int i;
  for (i = 0; i < n; i++) {
    a_out[i] = sqrt(a_in[i]);
  }
}
