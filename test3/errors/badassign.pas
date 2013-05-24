fun foo(x:int,y:float)
   a : int;
   b : float;
   c : int[40];
   d : float[40];
   i : int;
   begin
      a := x;   /* Okay */
      b := y;   /* okay */
      a := c;   /* no */
      b := d;   /* no */
      c := x;   /* no */
      d := y;   /* no */
      c[i] := b;  /* no */
      d[i] := a  /* no */
   end

      