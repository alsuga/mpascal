/* Una mala manera de sumar dos numeros */

fun sum(a : int[1000], n:int)
    s : int;
    i : int;
    begin
       s := 0;
       i := 0;
       while i < n do begin
             s := s + a[i];
             i := i + 1
       end;
       return s
    end

fun main()
   x : int[1000];
   n : int;
   s : int;
   i : int;
   begin
       print("Entre un numero n : ");
       read(n);
       if n > 0 and n < 1000 then
            begin
                i := 0;
                while i < n do begin
                    x[i] := i;
                    i := i + 1
                end;
                s := sum(x,n);
                write(s)
             end
        else 
             print("Valor malo de n\n")
    end


                 
 
  
    