#include <stdio.h>
#include <stdlib.h>

void remalloc(double** a, int* n){
    double* temp = malloc(((*n) + 1) * sizeof(double));

    for (int i = 0; i < (*n); i++){
        temp[i] = (*a)[i];
    }

    free(*a);

    (*a) = temp;
}

void classify(double a[], int n, double levels[], int m, double*** classes, int** sizes) {

  // Note: *size is an array contain the values of *classes
  // Note: **class is an array contain arrays *classes such as class 1, class 2, class 3, ...
  // < levels(0) class 1:
  // < levels(1) class 2:
  // < levels(m - 1) class m: 


  *sizes = (int*)malloc((m + 1) * sizeof(int));
  *classes = (double**)malloc((m + 1) * sizeof(double*));

  for (int i = 0; i < n; i++){
    for (int j = 0; j < m; j++){

      if ((*sizes)[j + 1] == 0) (*classes)[j + 1] = (double*)malloc(sizeof(double));  

      if (a[i] < levels[j]){
        // a[i] belongs to class i + 1
        ((*sizes)[j + 1])++; 
        remalloc(&((*classes)[j + 1]), &((*sizes)[j + 1]));
        (*classes)[j + 1][(*sizes)[j + 1] - 1] = a[i];
      }

      if (a[i] > levels[m - 1]){ 
        // a[i] belongs to class m + 1 // 
        (*sizes)[m + 1]++;
        remalloc(&((*classes)[j + 1]), &((*sizes)[m + 1]));
        (*classes)[j + 1][(*sizes)[m + 1] - 1] = a[i];
      }

    }
  }
}

int main() {

  int n, m;

  // Read n and elements of a
  scanf("%d", &n);

  double* a;
  a = (double*)malloc(n * sizeof(double));
  for (int i = 0; i < n; i++) {
    scanf("%lf", &a[i]);
  }

  // Read m and elements of levels
  scanf("%d", &m);

  double* levels;
  levels = (double*)malloc(m * sizeof(double));
  for (int i = 0; i < m; i++) {
    scanf("%lf", &levels[i]);
  }


//Because in this task i don't care about 
  //Define classes
  double** classes;
  int* sizes;
  classify(a, n, levels, m, &classes, &sizes);

  //Print
  for (int i = 0; i <= m; i++) {
    printf("Class %d:", i + 1);
    for (int j = 0; j < sizes[i]; j++) {
      printf(" %.3lf", classes[i][j]);
    }
    printf("\n");
  }

  //Free
  for (int i = 0; i <= m; i++) {
    free(classes[i]);
  }

  free(a);
  free(levels);
  free(classes);
  free(sizes);

  return 1;
}