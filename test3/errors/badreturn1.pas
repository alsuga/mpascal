fun foo(x:int)
    begin
       if (x > 3) then return 3

	/* Error.  The if-statement returns an int.  However, if we
           make it here, the function returns nothing at all. */
    end


fun foo2(x:int)
    begin
        while x > 0 do return 3

        /* Same problem as above. While might not execute */
    end
        

