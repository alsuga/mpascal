fun foo(x:int,y:int)
    begin
       return x + y
    end

fun main()
    a : int;
    begin
      a := foo(2,3);
      a := foo(2);
      a := foo(2,3,4);
      a := foo();
      foo(2,3);
      foo(2);
      foo(2,3,4);
      foo()
    end

 