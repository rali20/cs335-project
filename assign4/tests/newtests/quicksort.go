func print_int(n int);
func print_str(s string);
func read_int() int;

func partition(a *int, low int, high int) int{
	var pivot int = *(a+4*high);
	var i int = low - 1;
	var j,t int;
	for j=low; j<high; j=j+1{
		if(*(a+4*j) <= pivot){
			i=i+1;
			t = *(a+4*i);
			*(a+4*i) = *(a+4*j);
			*(a+4*j) = t;
		}
	}
	t = *(a+4*(i+1));
	*(a+4*(i+1)) = *(a+4*high);
	*(a+4*high) = t;
	return i+1;
}

func qsort(a *int, low int, high int) int {
	if(low<high){
		var pi int = partition(a,low, high);
		qsort(a, low, pi-1);
		qsort(a, pi+1, high);
	}
	return 1;
}

func main(){
	print_str("\033[91m \n\nRUNNING QUICKSORT.GO \033[0m");
	var a[100] int;
	var i,e,n int;
	print_str("\033[91m \nEnter no of elements :  \033[0m");
	n = read_int();
	print_str("\033[91m \nEnter numbers below:\n \033[0m");
	for i=0; i<n; i=i+1{
		e  = read_int()
		a[i] = e;
	}

	print_str("\033[91m \nBefore sorting :  \033[0m");
	for i=0; i<10; i=i+1{
		print_int(a[i]);
		print_str(" ");
	}
	qsort(&a,0,n);
	print_str("\033[91m \nAfter sorting :  \033[0m");
	for i=0; i<10; i=i+1{
		print_int(a[i]);
		print_str(" ");
	}
}
