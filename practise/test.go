type new_int int;
type new_new_int new_int;
var glob new_new_int;
var naya_structure struct {
  a,b,c int;
  S struct{
    p,q int;
  };
  arr [10]int;
};


type node struct{
  a int;
  b string;
};

// var sme node;

var e,f int = 1,2;


// func print();
func main(a int, b string, c float ) int{
    // const (
    //   c0 = 1;  // c0 == 0
    //   c1 = 2.0;  // c1 == 1
    //   c2, c3 string = "amit", "yadav";  // c2 == 2
    //   a,b int;
    // );
    var arr [10]int;
    arr[2] = 1;
    // var temp node;
    // temp.b = "amit";
    // var ptr *node;
    // (*ptr).b = "amit";
    var t *int;
    *t = 1;
    // var d int = 2 + 3;
    // Here's a basic example.
    // const e,f,g int = 1+2,2,3;
    // var m float = 1;
    // var arr [4] int;
    // m = 2;
    // var str string = "amit";
    // var str string = "amit";
    // str = 2;

    // e = f+g;
    // e = 10;
    // e = 2 + 4;
    // // c = 10;
    // if 7%2 == 0 {
    //     var a integer;
    //     m = e;
    // } else {
    //     var b charere;
    //     f = e + g;
    // }
    // outerloop :
    // var i,j int;
    // // for i = 1 ; i < 10 ; i = i + 1{
    // //   // break;
    //   for j = i ; j < 20 ; j = j + 1{
    //     if i%2 == 0 {
    //         var a integer;
    //         m = e;
    //         // continue;
    //     } else {
    //         var b char;
    //         f = e + g;
    //         // continue outerloop;
    //     }
    //     e = 2 + 4;
    //     if j%2 == 0 {
    //       f = e*g;
    //       break;
    //     }
    //     if i+j % 25 == 0{
    //       // break outerloop;
    //     }
    //   }
    // }
    //
    // // You can have an `if` statement without an else.
    // if  8%4 == 0 {
    //     const amit string="hello";
    // }
    // var i int;
    // A statement can precede conditionals; any variables
    // declared in this statement are available in all
    // branches.
    // if num := 9; num < 0 {
    // } else if num < 10 {
    //
    // } else {
    //     Println(num, "has multiple digits")
    // }
}
