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
	var n int = 10;
	var numbers [40] int;
  var i int;
	print_str("Mergesort Check : integers only\n");
	print_str("Enter no of elements (max 40) : ");
	n = read_int();
	print_str("Enter numbers below\n");
	for i =0; i<n; i=i+1 {
		numbers[i] = read_int();
	}
	print_str("Before sorting : ");
	for i =0; i<n; i=i+1 {
		 print_int(numbers[i]);
		 print_str(" ");
	}
	print_str("\n");

	mergesort(&numbers, n);

	print_str("After sorting : ");
	for i =0; i<n; i=i+1 {
		 print_int(numbers[i]);
		 print_str(" ");
	}
	print_str("\n");

}
