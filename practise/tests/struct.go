func print_int(n int);
func print_str(s string);
func read_int() int;

type node struct{
  val int;
};

type bigNode struct {
  a,b,c int;
  s string;
  N node;
};

func main(){
  var bNode bigNode;
  bNode.N.val = 1;
  print_int(bNode.N.val);

}
