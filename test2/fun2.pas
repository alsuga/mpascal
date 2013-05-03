/* This function tests function calls */

fun foo(x : int) 
    y : int;
    begin

        y := bar(3,4,5);   /* Several arguments */
	y := bar(x);         /* One argument      */
        y := bar();          /* No arguments      */
        y := bar(2*x,1+2*x+(3*x)*(4+x),3.4);
        y := bar(bar(bar(bar(x,2*x),3*x),4+x),bar(2*y))
    end

