func print_int(n int);
func print_str(s string);
func read_int() int;

func main() {
	print_str("\033[91m \n\nRUNNING BINSEARCHITER.GO \033[0m");
	var i [100] int;
	var d int;
	var c int;
	print_str("\nEnter the size: ");
	c = read_int();
	var l int = 0;
	var r int = c;
	var m int;
	var n int;
	var idx int = -1;
	for d = 0; d < c ;d=d+1{
		n = read_int();
		i[d] = n;
	}
	print_str("\033[91m \nEnter the key to search for: \033[0m");
	n = read_int();
	for ;l <= r;{
		// print_int(l);
		// print_str("\n");
		m = l + (r-l)/2;
		if(i[m] == n){
			idx = m;
			break;
		}
		if(i[m] < n){
			l = m + 1;
		}else{
			r = m - 1;
		}
	}
	print_str("\033[91m \nFound index of key: \033[0m");
	print_int(idx);
	print_str("\n");
}
