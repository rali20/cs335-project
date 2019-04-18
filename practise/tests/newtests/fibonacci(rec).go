func print_int(n int);
func print_str(s string);
func read_int() int;

func fib(n int) int;

func fib(n int) int {
	if(n<2){
		return n;
	}
	var x int = fib(n-1) + fib(n-2);

	return x;
}

func main() {
	var i,j int;
	print_str("\033[91m \n\nRUNNING FIBONACCI(rec).GO \n\033[0m");
	print_str("\033[91m Enter a number: \033[0m");
	i = read_int();
	var n int;
	for n=0;n<i;n=n+1{
			print_int(fib(n));
			print_str(" ");
	}
}
