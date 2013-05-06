func factorial(n:int)
begin
     if n > 1 then
          return n * n-1
     else 
          return 1
end

func hola(n:int, b:float)
a:int;
c:int;
st:int[15];
ra:int[15];
begin
  a:= st[ ra[3 + 1] - st[6*6] ] + ra[ 5 + 2];
  if n > 1 then
          return n * factorial(n-1)
     else 
          return(1)
end

func main()
num:int;
begin
     print("Ingrese el valor de n: ");
     read(num);
     print("El resultado es: ");
     write(factorial(num))
end