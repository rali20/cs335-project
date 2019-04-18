func print_int(n int);
func print_str(s string);
func read_int() int;

type s struct {
  a int;
  b float;
};

type t struct {
   a int;
  b float;
};

// func g(int x, float y) {
//  print_int(x);
//  print_sttr("\n");
//  print_int(y);
// }

func  main() {
 var x *s;
 var y *s;
 // var q float;
 (*x).a = 2;
 print_int((*x).a);
 // y = x;
 // x.b = -4;
 // g(x.b, y.b);
}
