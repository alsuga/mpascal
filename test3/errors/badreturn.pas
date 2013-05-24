fun bad_return1():float
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return f      /* okay */
   end

fun bad_return2():int
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return n      /* okay */
   end

fun bad_return3():int
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return n[i]   /* Bad array */
   end

fun bad_return4():int[40]
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return a
   end

fun bad_return5():float[30]
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return b
   end
