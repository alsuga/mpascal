/* how not to compute n mod 2 */
fun foo(n:int)
        fun bar(n:int)
        begin
                return foo(n-1)
        end;
begin
        if n == 0 then
                return 0
        else if bar(n) > float(0) then
                return 0
        else
                return 1
end
