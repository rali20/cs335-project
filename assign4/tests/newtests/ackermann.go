func print_int(n int);
func print_str(s string);
func read_int() int;

func ack(m int , n int) int;

func ack(m int , n int) int {
	print_int(m);
	print_int(n);
	print_str("\n");
	if(m==0){
		return n+1;
	}
	if((m>0) & (n==0)){
		return ack(m-1,1);
	}
	if((m>0) & (n>0)){
		return ack(m-1,ack(m,n-1));
	}
}

func main() {
	var a int;
	var b int;
	a = read_int();
	b = read_int();
	print_int(ack(a,b));
}
