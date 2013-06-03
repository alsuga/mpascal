fun bad_return1()
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return f      /* okay */
   end

fun bad_return2()
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return n      /* okay */
   end

fun bad_return3()
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return n[i]   /* Bad array */
   end

fun bad_return4()
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return a
   end

fun bad_return5()
   a : int[40];
   b : float[30];
   n : int;
   i : int;
   f : float;
   begin
      return b
   end
