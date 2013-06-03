fun foo(x:int,y:int)
    begin
       return x + y
    end

fun main()
    a : int;
    b : float;
    begin
      a := foo(2,3);
      a := foo(a,b);
      a := foo(b,a) 
    end

 