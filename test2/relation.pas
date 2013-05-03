/* Tests various kinds of relational expressions */

fun foo(x: int)
    y : int;
    begin
        if x < y then
            skip;
        if x < y or x > 400 then
            skip;
        if x >= 0 and x <= y then
            skip;
	if not x >= x - y or x - y < 100 then
	    skip
    end
        
      
