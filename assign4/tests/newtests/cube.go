func print_int(n int);
func print_str(s string);
func read_int() int;

func ma() {

	var prev int = 1;
	var curr int = 1;
	var next int = 1;
	var n int = 2;
	var n1 int = 3;
	var n2 int = 4;
	var i int = 10;
	var j int = 12;
	var k int = 1;
	var l int = 1;
	var one int = 1;
	var sum int = 0;
	var sum1 int = 0;

	// for j = one; j<=n; j = j + one {
		for i=one; i<=n; i = i + one {
			for k=one; k<=n; k = k + one {
				for l=one; l<=n; l = l + one {
					sum = sum + 1;
				}
			}
		}

		for i=one; i<=n1; i = i + one {
			for k=one; k<=n1; k = k + one {
				for l=one; l<=n1; l = l + one {
					sum = sum + 1;
				}
			}
		}
		for i=one; i<=n2; i = i + one {
			for k=one; k<=n2; k = k + one {
				for l=one; l<=n2; l = l + one {
					sum = sum + 1;
				}
			}
		}
		for i=one; i<=n1; i = i + one {
			for k=one; k<=n1; k = k + one {
				for l=one; l<=n1; l = l + one {
					sum = sum + 1;
				}
			}
		}
		for i=one; i<=n2; i = i + one {
			for k=one; k<=n2; k = k + one {
				for l=one; l<=n2; l = l + one {
					sum = sum + 1;
				}
			}
		}

	// }
	print_int(sum);
	return;
}




func main() {
	print_str("\033[91m \n\nRUNNING CUBE.GO \033[0m");
	var prev int = 1;
	var curr int = 1;
	var next int = 1;
	var n int = 2;
	var n1 int = 3;
	var n2 int = 4;
	var i int = 10;
	var j int = 12;
	var k int = 1;
	var l int = 1;
	var one int = 1;
	var sum int = 0;
	var sum1 int = 0;

	// for j = one; j<=n; j = j + one {
		for i=one; i!=n+1; i = i + one {
			for k=one; k<=n; k = k + one {
				for l=one; l<=n; l = l + one {
					sum = sum + 1;
				}
			}
		}
	print_int(sum);
		for i=one; i!=n1+1; i = i + one {
			for k=one; k<=n1; k = k + one {
				for l=one; l<=n1; l = l + one {
					sum = sum + 1;
				}
			}
		}
		print_int(sum);
		for i=one; i!=n2+1; i = i + one {
			for k=one; k<=n2; k = k + one {
				for l=one; l<=n2; l = l + one {
					sum = sum + 1;
				}
			}
		}

	// }
	print_int(sum);
	return;
}
