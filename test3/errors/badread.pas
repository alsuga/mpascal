
fun bad_read()
   a : int[40];
   n : int;
   i : int;
   begin
      read(n[i]);    /* n not an array */
      read(a[3.4]);  /* Bad index */
      read(n[3.4]);  /* Bad index and not an array */
      read(a)        /* Can't read into an array */
   end

	

        