/* Tests for various combinations of nested functions */

fun foo (a : int)
    b : int;
    fun bar(c: int)
        fun spam(d:int)
            e : int[40];
            f : float;
            fun blah(g:float)
                h : float;
                begin
                   h := 2.0*g;
                   return h
                end;
            i  : int;
            begin
               i := 0;
               while i < 40 do begin
                    e[i] := d*i;
                    i := i + 1
               end;
               return i
            end;
         j : int;
         begin
             j := 0;
             while j < 1000 do begin
                 spam(c);
                 j := j + 1
             end;
             return 2*c
         end;
     begin
         b := a*bar(a);
         write(b);
         return b
     end



        

 