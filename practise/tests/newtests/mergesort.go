func print_int(n int);
func print_str(s string);
func read_int() int;


func mergesort(numbers *[40]int , n int);

func mergesort(numbers *[40]int , n int) {
		if n <= 1 {
			return ;
		}

		var l,r,j int;
		l = n/2;
		r = n-l;

		var left [40] int;
		var right [40] int;

		j=0;
	  var i int;
		for i = 0; i<l; i=i+1 {
			left[i] = (*numbers)[j];
			j=j+1;
		}
		for i = 0; i<r; i=i+1 {
			right[i] = (*numbers)[j];
			j=j+1;
		}
		mergesort(&left, l);
		mergesort(&right, r);

		i=0;
		j=0;
	  var k int;
		for k = 0; k<n; k=k+1 {
			if i==l {
				(*numbers)[k] = right[j];
				j = j+1;
			}
			elif j==r {
					(*numbers)[k] = left[i];
					i= i+1;
			}
	    elif left[i] < right[j] {
						(*numbers)[k] = left[i];
						i=i+1;
			}
			else {
						(*numbers)[k] = right[j];
						j=j+1;
			}
	  }
		return ;
}

func main() {
	print_str("\033[91m \n\nRUNNING MERGESORT.GO \033[0m");
	var n int = 10;
	var numbers [100] int;
  var i int;
	print_str("\033[91m \nMergesort Check : integers only\n \033[0m");
	print_str("\033[91m \nEnter no of elements :  \033[0m");
	n = read_int();
	print_str("\033[91m \nEnter numbers below:\n \033[0m");
	for i =0; i<n; i=i+1 {
		numbers[i] = read_int();
	}
	print_str("\033[91m \nBefore sorting :  \033[0m");
	for i =0; i<n; i=i+1 {
		 print_int(numbers[i]);
		 print_str(" ");
	}
	print_str("\n");

	mergesort(&numbers, n);

	print_str("\033[91m \nAfter sorting :  \033[0m");
	for i =0; i<n; i=i+1 {
		 print_int(numbers[i]);
		 print_str(" ");
	}
	print_str("\n");

}
