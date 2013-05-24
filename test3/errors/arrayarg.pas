fun foo(x:int[40],y:int[40],z:int[40])
   i:int;
   begin
      i := 0;
      while i < 40 do begin
          z[i] := x[i] + y[i];
          i := i + 1
      end
   end


fun main()
   a: int[40];
   b: int[40];
   c: int[40];
   d: int[50];
   begin
    foo(a,b,c);
    foo(a,b,d)    /* Incompatible array size on d */
   end

