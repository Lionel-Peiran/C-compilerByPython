int main()
{
   int c, first, last, middle, n, search, array[100];
 
   printf();
   scanf();
 
   printf( n);
 
   for (c = 0; c < n; c++)
      scanf(&array[c]);
 
   printf();
   scanf(&search);
 
   first = 0;
   last = n - 1;
   middle = (first+last)/2;
 
   while (first <= last) {
      if (array[middle] < search)
         first = middle + 1;    
      else if (array[middle] == search) {
         printf(search, middle+1);
         break;
      }
      else
         last = middle - 1;
 
      middle = (first + last)/2;
   }
   if (first > last)
      printf(search);
 
   return 0;   
}