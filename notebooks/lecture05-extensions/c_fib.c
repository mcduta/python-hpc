int fibonacci (int n, int *a_out) {

  int i;

  if (n >= 1) {
    a_out[0] = 1;
  }

  if (n >= 2) {
    a_out[1] = 1;
  }

  for (i = 2; i < n; i++) {
    a_out[i] = a_out[i-1] + a_out[i-2];
  }

  return 0;
}
