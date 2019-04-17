func print_int(n int);
func print_str(s string);

func main(){

  var n int = 10;
  var p *int;
  p = &n;
  print_str("Pointer Assignment Check\n")
  print_str("n : ");
  print_int(n);
  print_str("\n");
  *p = 5;
  print_str("n : ");
  print_int(n);
  print_str("\n");

}
