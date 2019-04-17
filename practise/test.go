// type new_int int;
// type new_new_int new_int;
// var glob new_new_int;

// //
// //
// type node struct{
//   a int;
//   c float;
//   b string;
// };
// //

// var e,f float = 6,5;

func print_int(n int);
// func print_str(s string);
// func read_int() int;

type bigNode struct {
  a,b,c int;
  S struct{
    p,q int;
  };
  arr [10]int;
};


func main(){
  var bNode bigNode;
  bNode.S.q = 113;
  print_int(bNode.S.q);
  // bNode.a = 1;
  // bNode.b = 3;
  // bNode.c = 5;
  // bNode.S.p = 25;
  // bNode.S.q = 28;

  // var a int;
  // a = 596;

  // var Node node;
  // Node.a = 34;
  // print_int(a);
  // print_int(0);
  // print_int(Node.a);
  // var n int = 10;
  // print_int(n);
  // n = read_int();
  // print_int(n);
  // n = addhaha(n,2);
  // n = f1(9,8,7);
  // print_int(n);

  // var s string;
  // s = "hello world\n";
  // print_str(s);
  // a = 4;
  // print_int(5);
  // print_int(a);
  // print_int(5);
  // a = read_int();
  // if a < 2{
  // print_int(a);
  // a=100;
  // print_int(a);
  // }
  // elif a <= 6 {
  // print_int(a);
  // a=10;
  // print_int(a);
  // }
  // elif a == 0{
  //   print_int(a);
  //   a = 76;
  //   print_int(a);
  // }
  // elif a>10 {
  //   print_int(a);
  //   a =100;
  //   print_int(a);
  // }
  // elif a >= 5{
  //   print_int(a);
  //   a = 10;
  //   print_int(a);
  // }
  // elif a!=1{
  //   print_int(a);
  //   a = -3;
  //   print_int(a);
  // }
  // else {
  // print_int(a);
  // a = 3;
  // print_int(a);
  // }
  // print_int(5);


  // print_int(sme.a);
  // sme.a = 1;
  // print_int(sme.a);

  // b = "amit";
  // return "hello";
  // b = a + 1;
  // a = 2 + 3;
  // a = 4 + a;
  // a = b + a;
  // a = read_int();
  // var arr [4] int;
  // arr[2] = a;
  // print_int(arr[2]);
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
// func f2(n1 int,n2 int,n3 int) int{
  //    return n1+n2+n3;
  // }
  // func f1(n1 int,n2 int,n3 int) int{
    //    return f2(f2(n1,n2,n3),n2,n3);
    // }
    //
    // func addhaha(a int, b int) int{
      //   return a+b;
      // }
