func print_int(n int);
func print_str(s string);
func read_int() int;

func even(n int) int;

func odd(n int) int {
	if(n==0){
		return 0;
	}else{
		return even(n-1);
	}
}

func even(n int) int {
	if(n==0){
		return 1;
	}else{
		return odd(n-1);
	}
}

func main() {
	var n int;
	n = read_int();
	print_int(even(n));
	print_int(odd(n));
}
