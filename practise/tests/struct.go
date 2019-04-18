func print_int(n int);
// func print_str(s string);
// func read_int() int;

type node struct{
  val int;
};

type bigNode struct {
  a,b,c int;
  s string;
  N node;
  arr [5]int;
};

func main(){
  var bNode bigNode;
  var x int;
  bNode.N.val = 67;
  bNode.arr[1] = 45;
  x = bNode.arr[1];
  print_int(x);
  x = bNode.N.val;
  print_int(x);

}
