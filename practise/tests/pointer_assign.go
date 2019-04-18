func print_int(n int);
func print_str(s string);

func main(){

  var n int = 63;
  var p *int;
  p = &n;
  print_str("Pointer Assignment Check\n");
  print_str("n before : ");
  print_int(n);
  print_str("\n");
  *p = 23;
  print_str("n after : ");
  print_int(n);
  print_str("\n");

  var arr [10] int;
  var q *[40]int;
  arr[1] = 3;
  print_str("arr[1] before : ");
  print_int(arr[1]);
  print_str("\n");
  q = &arr;
  (*q)[1] = 5;
  print_str("arr[1] after : ");
  print_int(arr[1]);
  print_str("\n");

}
