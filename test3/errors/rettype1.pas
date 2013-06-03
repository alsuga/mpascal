fun bar(a:int, b:int)
  z:int;
  fun spam(a:int) 
    i:int;
    begin
    i := 0;
    while i < a do
      begin 
        print("SPAM!"); 
        i := i + 1
     end
  end;

  x:float;
  y:int;
  begin 
     spam(a + b);
     y := 4 + spam(a+b); /* type error - spam doesn't return int */
     return a + b
  end
    
fun main() 
   x:int; y:int; z:float;
   begin
   x := 2; y := 3;
   bar(x,y);
   x := bar(x,y); 
   x := 5 * bar(x,y) * 5;
   y := 3.0 * bar(x,y); /* type error */
   y := bar(x,y)
   end
