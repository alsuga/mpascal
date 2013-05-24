fun mrgsort(nums:int[10], p:int, r:int)
  fun merge(n:int[10], p:int, q:int, r:int)
    temp:int[10];
    ptr1:int;
    ptr2:int;
    nitems:int;
    i:int;
    begin
	ptr1 := p;
        ptr2 := q;
 	nitems := 0;
        while (ptr1 < q and ptr2 < r) do begin
		if n[ptr1] <= n[ptr2] then begin
			temp[nitems] := n[ptr1];
	                ptr1 := ptr1 + 1;
	                nitems := nitems + 1
	                end
		else begin
			temp[nitems] := n[ptr2];
			ptr2 := ptr2 + 1;
			nitems := nitems + 1
		     end
            end; 
  	i := 0;
	while i < nitems do begin
	   nums[p+i] := temp[i];   /* esto no es adecuado*/
	   i := i + 1
	end 
     end;
  q:int;
  begin
  	if p < r then begin
 	   q := (p + r) / 2;
           mrgsort(nums, p, q);
	   mrgsort(nums, q+1, r);
	   merge(nums, p, q, r)
        end
  end

fun print_arr(nums:int[10], nnums:int)
    i:int;
    begin
 	    i := 0;
	    while i < nnums do
	    begin
		write(nums[i]);
		print(" ")
	    end;
   	    print("\n")
    end

fun main()
  nums:int[10];
  result:int[10];
  i:int;
  begin
    nums[0] := 17; nums[1] := 33; nums[2] := 9;
    nums[3] := 103; nums[4] := 63; nums[5] := 64;
    nums[6] := 202; nums[7] := -5; nums[8] := 73;
    nums[9] := 9;
    i := 0;
    print("lista desordenada es:\n");
    print_arr(nums,10);
    mrgsort(nums, 0, 9);
    print_arr(nums,10)
  end

   
   
  