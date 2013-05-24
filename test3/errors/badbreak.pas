fun bad_break(x:int)
   begin
      write(x);
      while (x > 0) do begin
         if x > 100 then break;
         x := x + 1
      end;
      if x > 3 then break
      else break;
      return x
   end

