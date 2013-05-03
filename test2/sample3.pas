func factorial(v:int)
  n: int;
  i:int;
  mul:int;
	begin
		mul:=1;
		print("ingrese numero: ");
		read(n);
		i := 1;
		while (i <= n) do
		begin
			mul := mul * i; 
			i := i + 1
		end;
		print("el factorial es ");
		write(i)
	end