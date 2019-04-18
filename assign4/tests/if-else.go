func print_int(n int);
func print_str(s string);
func read_int() int;

func main(){
  var a int;
  a = read_int();
  if a == 2{
    print_int(a);
    a=100;
    print_int(-a);
  }
  elif a < 2 {
    print_int(a);
    a=10;
    print_int(a);
  }
  elif a <= 3{
    print_int(a);
    a = 76;
    print_int(a);
  }
  elif a > 10 {
    print_int(a);
    a =100;
    print_int(a);
  }
  elif a >= 5{
    print_int(a);
    a = 10;
    print_int(a);
  }
  elif a == 4{
    print_int(a);
    a = 3;
    print_int(a);
  }
  else {
    print_int(a);
    a = 3;
    print_int(a);
  }
  var s string = "Done";
  print_str(s);
}
