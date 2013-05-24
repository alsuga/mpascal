fun isprime(n:int)
   i:int;
   fun mod(x:int, y:int)
      begin
         return x - (x/y) * y
      end;
   begin
     i := 2;
     while (i < n) do
        begin
           if mod(n,i) == 0 then return 0;
           i := i + 1
       end;
     return 1
   end

fun main()
   x:int;
   r:int;
   begin
      print("Entre un numero\n");
      read(x);
      r := isprime(x);
      write(x);
      if r == 1 then print(" es primo\n")
      else print (" no es primo\n")
   end

      	     
