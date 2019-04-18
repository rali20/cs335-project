func print_int(n int);
func print_str(s string);
func read_int() int;

func binsearch(a *int, low int, high int, n int) int{
	if(low > high){
		return -1;
	}
	var middle int = low + (high - low)/2;
	if(*(a+4*middle) == n){
		return middle;
	}
	if(*(a+4*middle) > n){
		return binsearch(a,middle+1,high,n);
	}else{
		return binsearch(a,low,middle-1,n);
	}
}

func main() {
	print_str("\033[91m \n\nRUNNING BINSEARCHREC.GO\n\033[0m");
	var a[100] int;
	var d int;
	var c int;
	print_str("\nEnter the size: ");
	c = read_int();
	var n int;
	for d = 0; d < c ;d++{
		n = read_int();
		a[d] = n;
	};
	print_str("\033[91m \nEnter the key to search for: \033[0m");
	n = read_int();
	print_int(binsearch(&a,0,c,n));
};
