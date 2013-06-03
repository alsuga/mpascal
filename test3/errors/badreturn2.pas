fun foo(x:int)
    fun bar(x:int)
        y:int;
        begin
            y := foo(x)
        end;
    begin
        write(x)
    end

// no puede llamar al padre!
