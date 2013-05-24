fun bar(a:int[200], b:float[200])
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
  begin 
    x := 1.0;
    /* errors */
    a := 5; /* a is array */
    a := a; /* a is an array */
    a := a + a; /* a is an array */

    /* not errors */
    a[0] := a[1]; 
    a[0] := 5;  
    a[int(x)] := a[int(4.0)];

   /* errors */	
    a[-2] := a[5]; /* negative index */
    a[2] := a[5.0 * 4.0];  /* index not an int */
    a[0] := 5 + a;  /* a is an array */
    a[0] := 5.0; /* a[0] is an int */
    x[0] := x[0]; /* x is not an array */
    write(x)
  end
    
fun main() 
   y:int[200];
   x:float[200];
   z:int[201];
   begin
   bar(y,x); /* correct */

  /* incorrect - wrong arg types */
   bar(z,x);  
   bar(x,x);
   bar(x[0],y[0]);
   skip
  end
