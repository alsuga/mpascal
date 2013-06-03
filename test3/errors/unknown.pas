
/* Not enough information to determined return type */
fun foo(x:int)
   begin
      return foo(x-1)
   end

fun main()
   a:int;
   begin
       read(a);
	
       /* return value of foo used, but not enough information
          to determine return type */

       write(foo(a))
   end

