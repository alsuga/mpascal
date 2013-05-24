fun bar(a:int, b:float)
  z:int;
  fun spam(a:int) 
    a:int;  /* previously declared */
    begin  
    z:=0;  
    a:=z+2;
    print("SPAM!"); 
    write(i)  /* undeclared identifier */
  end;
  x:float;
  z:int; /* previously declared */
  begin 
    x := b + 5.0;
    write(x)
  end
    
fun main() begin
    bar(3, 17.0);
    spam(3); /* unknown identifier */
    writeln(4) /* unknown id */
  end
