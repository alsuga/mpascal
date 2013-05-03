/* Tests for the break and skip statements */

fun foo(x:int)
   i : int;
   begin
       i := 0;
       while i < x do
            begin
                if i == 4 then break;
                i := i + 1
            end;
       i := 0;
       while i < x do skip;
       return i
   end

       