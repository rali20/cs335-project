func print_int(n int);
func print_str(s string);
func read_int() int;

func f2(n1 int,n2 int,n3 int) int{
     return n1+n2+n3;
  }
func f1(n1 int,n2 int,n3 int) int{
     return f2(f2(n1,n2,n3),n2,n3);
  }

func add_us(a int, b int) int{
    return a+b;
  }

func main(){
  var n1,n2,n3 int = read_int(),read_int(),read_int();
  print_str("f1 result: ");
  print_int(f1(n1,n2,n3));
  print_str("\nadd result : ");
  print_int(add_us(n1,n2));
  print_str("\n");
}
