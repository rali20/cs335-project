func print_int(n int);
func print_str(s string);
func read_int() int;

func fib(n int) int {
	if(n==1){
		return 0;
	}
	if(n==2){
		return 1;
	}
	var prev,curr,next,i int;
	prev = 0;
	curr = 1;
	next = 1;
	print_int(prev);
	print_str(" ");
	for i=2; i<n; i = i+1{
		print_int(next);
		print_str(" ");
		next = prev + curr;
		prev = curr;
		curr = next;
	}
	return next;
}

func main(){
	print_str("\033[91m \n\nRUNNING FIBONACCI(iter).GO \n\033[0m");
	var n int;
	print_str("\033[91m Enter a number: \033[0m");
	n = read_int();
	print_int(fib(n));
}
