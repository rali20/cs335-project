func print_int(n int);
func print_str(s string);
func read_int() int;

func fact(n int) int;

func max(n int, m int) int {
	if(n>m){
		return n;
	}else{
		return m;
	}
}

func fact(n int) int {
	if(n == 1) {
		return 1;
	}
	return n*fact(n-1);
}

func main() {
	print_str("\033[91m \n\nRUNNING FACTORIAL.GO \033[0m");
	print_str("\033[91m \n Enter two numbers: \n\033[0m");
	var in1, in2 int;
	in1 = read_int();
	in2 = read_int();
	var k int = max(in1,in2);
	var a int = fact(k);
	print_str("\033[91m \n Factorial of larger number = \033[0m");
	print_int(a);
}
