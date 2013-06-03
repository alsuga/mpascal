fun bar(a:int, b:float)
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
    x := b + 5.0;
    write(x);
    return x
  end
    
fun main()
   y:int;
   begin
    y := 0;
    bar(3, 17); /* wrong arg type */
    bar(y,float(y));
    bar(y,4.4);
    bar(bar(3,4.0), 4.0); /* wrong arg type (bar returns a float) */
    bar(); /* wrong # of arguments */
    bar(y)  /* wrong # of arguments */
  end






