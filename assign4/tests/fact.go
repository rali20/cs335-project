func print_int(n int);
func read_int() int;
func print_str(s string);

func fact(n int) int;

func fact(n int) int{
  if n > 0 {
    return n*fact(n-1);
  }
  else {
    return 1;
  }
}

func main() {
  var n int = 5;
  print_str("Enter a number to find factorial :");
  n = read_int();
  print_str("Factorial is :");
  print_int(fact(n));
  print_str("\n");
}
