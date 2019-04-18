func print_int(n int);
func print_str(s string);
// func read_int() int;

func main(){
	var x,y int;
	var p1,q1 *int;
	var p2,q2 **int;
	// var p3 ***int;
	x = 2;
	y = 5;
	print_str("Multi-Level Pointers Check\n");
	print_str("x before : ");
	print_int(x);
  print_str("\n");
	p1 = &x;
	p2 = &p1;
	*(*p2) = 98;
	print_str("x after : ");
	print_int(x);
  print_str("\n");

}
