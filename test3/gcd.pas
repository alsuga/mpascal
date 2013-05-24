fun gcd(x:int, y:int)
    g: int;
    begin
       g := y;
       while x > 0 do
           begin
              g := x;
              x := y - (y/x)*x;
              y := g
           end;
       return g
    end

fun main()
   x : int;
   y : int;
   r : int;
   begin
      print("Entre dos numeros\n");
      read(x);
      read(y);
      r := gcd(x,y);
      write(r)
   end
