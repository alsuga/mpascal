
/* Factorial sencillo */

fun fact(n:int)
    r : int;
    begin
        r := 1;
        while n > 0 do
            begin
                r := r * n;
                n := n - 1
            end;
         return r
     end

fun main()
   n : int;
   begin
       print("Hola. Soy un factorial sencillo.\n");
       print("Entre n :");
       read(n);
       write(fact(n))
   end
