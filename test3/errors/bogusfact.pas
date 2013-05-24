fun bogus_fact(a:int):float
  fun bogus_nested(b:int):float
     a:float;
     begin
     /* this return sets rettype of bogus_nested to float
 	and bogus_fact to float */
     return 2.0 + float(b) + bogus_fact(-7)
  end;
  begin
  if a > 1 then return bogus_nested(a) * bogus_fact(a - 1); /* okay: float * float */
  if a == -7 then return 2 
  else return 1  /* conflicting return types */
  end



    