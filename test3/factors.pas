fun mod(x:int, y:int)
      begin
         return x - (x/y) * y
      end


fun factor(n:int,stor:int[1024])
   i:int;
   nfacts:int;
   begin
     nfacts := 1;
     stor[0] := 1;
     i := 2;
     while ( i <= n) do
        begin
   	   if mod(n,i) == 0 then
 	 	begin
               	  nfacts := nfacts + 1; 
                  stor[i-1] := i
		end;
	   i := i + 1 
	end;
      return nfacts
   end




fun print_arr(a:int[1024],nelem:int)
    i:int;
    begin
         i := 0;
         while i < nelem do
 	   begin
	  	write(a[i]); print(" ");
                if mod(i,5) == 0 and i != 0 then print("\n");
		i := i + 1
           end
    end
     
             
fun main()
   x:int;
   nfs:int;
   results:int[1024];
   begin
      print("Enter a number\n");
      read(x);
      nfs := factor(x,results);
      print_arr(results,nfs)
   end

 


