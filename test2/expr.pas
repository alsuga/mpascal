/* This tests for a few valid arithmetic expressions */

fun foo(x:int,y:int,z:int,a:int,b:int,i:int,f:float,w:int,g:int,c:int,d:int,e:int,h:int)
    begin
        x := 3 + 4;
        y := a * b;
        z := (x + y);
        w := -y;
        w := +y;
        w := x[3*z];
        w := a - b;
        w := a / b;
        i := int(2*x);
        f := float(3*y);
	g := a*(b+c*(d+e*(f + g)-h))

    end


        
