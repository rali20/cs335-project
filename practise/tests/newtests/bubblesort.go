func print_int(n int);
func print_str(s string);
func read_int() int;

var g int;
var h int;
var k int;


func main() {
	print_str("\033[91m \n\nRUNNING BUBBLESORT.GO \033[0m");
	var i [100] int;
	var d int;
	var c int;
	print_str("\nEnter the size: ");
	c = read_int();
	var e int;
	var t int;

	for d = 0; d < c ;d=d+1{
		e = read_int();
		i[d] = e;
	}
	var x int;
	for d = 0; d < c-1; d = d+1{
		for e = 0; e < c-1; e = e+1{
			if(i[e] > i[e+1]){
				t = i[e];
				i[e] = i[e+1];
				i[e+1] = t;
			}
		}
	}

	for d = 0; d < c ;d=d+1{
		print_int(i[d]);
		print_str(" ");
	}
}
