/* Tests various forms of the read statement */

fun foo(x:int)
    y : int[1000];
    begin
       read(x);
       read(y[0]);
       read(y[2*x+10*y])
    end
