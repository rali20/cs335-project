func print_int(n int);
func print_str(s string);
func read_int() int;

func main(){
	print_str("\033[91m \n\nRUNNING MATMUL.GO \033[0m");
	var n1,m1,n2,m2,i,j,t,k int;
	var a[10][10] int;
	var b[10][10] int;
	var result[10][10] int;
	print_str("\033[91m \nEnter n1: \033[0m");
	n1 = read_int();
	print_str("\033[91m \nEnter m1: \033[0m");
	m1 = read_int();
	print_str("\033[91m \nEnter n1xm1 numbers:\n \033[0m");
	for i=0; i<n1; i = i+1{
		for j=0; j<m1; j = j+1{
			t = read_int();
			a[i][j] = t;
		}
	}
	print_str("\033[91m \nEnter n2: \033[0m");
	n2 = read_int();
	print_str("\033[91m \nEnter m2: \033[0m");
	m2 = read_int();
	if(n2 != m1){
		print_int(0);
		return;
	}
	print_str("\033[91m \nEnter n2xm2 numbers:\n \033[0m");
	for i=0; i<n2; i = i+1{
		for j=0; j<m2; j = j+1{
			t = read_int();
			b[i][j] = t;
		}
	}
	var sum int = 0;
	for i=0; i<n1; i = i+1{
		for j=0; j<m2; j = j+1{
			for k=0; k<m1; k=k+1{
				sum = sum + a[i][k]*b[k][j];
			}
			result[i][j] = sum;
			sum = 0;
		}
	}
	print_str("\033[91m \nMatmul result:\n\033[0m");
	for i=0; i<n1; i = i+1{
		for j=0; j<m2; j = j+1{
			print_int(result[i][j]);
			print_str(" ");
		}
		print_str("\n");
	}

}
