fun main(a:int[200], b:float[200])
  x:float;
  y:int;
   i:int; j:int; k:float;
  begin 
    x := 2 * 2; /* invalid type in assign */
    y := 2 * x - 4 * 4; /* x is a float */
    x := 4.4 * -2.3;   
   if 1 == 1 then skip;
   if 2.0 == 2.0 * 4 then skip;  /* int * float */
   if j != k then skip;  /* int != float */
   if i * i >= j then skip;
   if i <= j and i == 3 then skip;
   skip
  end
