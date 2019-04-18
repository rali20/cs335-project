func print_int(n int);
func print_str(s string);
func read_int() int;

func main(){
	print_str("\033[91m \n\nRUNNING MINUS.GO \n\033[0m");
	var n int;
	n = - 5 - - 5;
	print_int(n);
	print_str("\n");
}
