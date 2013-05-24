fun bad_write()
   a : int[40];
   n : int;
   i : int;
   begin
      write(n[i]);   /* n is not an array */
      write(a[3.4]); /* Bad array index   */
      write(n[3.4]); /* n not array and bad index */
      write(a)       /* Can't write an array */
   end

	

        