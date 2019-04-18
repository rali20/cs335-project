func print_int(n int);
func print_str(s string);
func read_int() int;



func main(){
  var x int;
  var p1 *int;
  var p2 **int;
  // var p3 ***int;
  x = 2;
  p1 = &x;
  p2 = &p1;
  *(*p2) = 98;
  print_int(x);
  // print_int(7);
  // print_int(x);
}
