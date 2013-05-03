/* Tests various forms of the write statement */

fun foo(x:int)
    y : int[1000];
    begin
       write(x);
       write(y[0]);
       write(y[2*x+10*y] + 45);
       write(1+x*y[x]/y[0]*2.4232)
    end


