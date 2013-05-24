/* fib ineficiente */
fun fib(n:int)
   begin
	   if n == 0 or n == 1 then return n
	   else return fib(n-1) + fib(n-2)
   end


fun main()
   x:int;
   r:int;
   begin
      print("Entre un nuemro\n");
      read(x);
      r := fib(x);
      write(r)
   end


