func print_int(n int);
func print_str(s string);
func read_int() int;

func gcd(a int ,b int) int;


func gcd(a int ,b int) int{
	if (b>a){
		var t int = b;
		b = a;
		a = t;
	}
	print_int(a);
	print_str(" ");
	print_int(b);
	print_str("\n");
	if (b < 1){
		return a;
	}

	return gcd(b,a%b);

}


func main() {
	print_str("\033[91m \n\nRUNNING GCD.GO \033[0m");
	var a,b int;
	print_str("\033[91m \nEnter two numbers: \n\033[0m");
	a = read_int();
	b = read_int();
	var c int = gcd(a,b);

	print_str("\033[91m \nGCD = : \033[0m");
	print_int(c);

}
