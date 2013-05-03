
/* Tests various types of variable assignment */

fun foo(x : int, y : float) 
z : int[1000];
begin
    y := 3.434;
    z[0] := 2*x;
    z[123+45*2] := x;
    z[x+2*(x+4)] := z[x-2]
end