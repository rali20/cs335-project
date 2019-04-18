// This test shows use of typedefs, global variables, scope of variables

func print_int(n int);
func print_str(s string);
func read_int() int;

type new_int int;
type new_new_int new_int;
var glob new_new_int;


func main(){
  glob = 1;
  print_str("\n");
  print_int(glob);
  {
    print_str("Enter a integer: \n");
    var glob int = read_int();
    print_int(glob);
  }
  print_str("\n");
  print_int(glob);


}
