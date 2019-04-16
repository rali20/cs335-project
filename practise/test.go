// type new_int int;
// type new_new_int new_int;
// var glob new_new_int;
// var naya_structure struct {
//   a,b,c int;
//   S struct{
//     p,q int;
//   };
//   arr [10]int;
// };
//
//
// type node struct{
//   a int;
//   c float;
//   b string;
// };
//
// var sme node;

// var e,f float = 6,5;


func print_int(n int);
func print_str(s string);
func read_int() int;
func f2(n1 int,n2 int,n3 int) int{
   return n1+n2+n3;
}
func f1(n1 int,n2 int,n3 int) int{
   return f2(f2(n1,n2,n3),n2,n3);
}
func main(a int, b string) string{

    var n int = 10;
    print_int(n);
    n = read_int();
    print_int(n);
    n = f1(9,8,7);
    // a = 1;
    // if a<2{
    //   a=3;
    // }
    // b = "amit";
    // return "hello";
    // b = a + 1;
    // a = 2 + 3;
    // a = 4 + a;
    // a = b + a;
    var arr [10] int;
    arr[5] = 1;
  //   var temp node;
  //   temp.b = "amit";
  //   var ptr *node;
  //   (*ptr).b = "amit";
	// var q,w,e,r,t,y int;
	// q = 1;
	// w=2;
	// e=4;
	// r=8;
	// t=16;
	// y=32;
	// y = y>>q<<w>>e<<r%(q|w|e|r);
	// t = y>>q<<w>>e<<r%15;
	// q = q|w|e|r;

}
