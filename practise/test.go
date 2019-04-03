type new_int int;
type new_new_int new_int;
var glob new_new_int;
var naya_structure struct {
  a,b,c int
};
func print();
func main(a int, b string) int{

    // const (
    //   c0 = 1;  // c0 == 0
    //   c1 = 2.0;  // c1 == 1
    //   c2, c3 string = "amit", "yadav";  // c2 == 2
    //   a,b int;
    // );
    // const c = 2 + 3;
    // Here's a basic example.
    var e,f,g int = 1,2,3;
    var m float = 1.3;
    e = f+g;
    e = 10;
    e = 2 + 4;
    // c = 10;
    if 7%2 == 0 {
        var a integer;
        m = e;
    } else {
        var b charere;
        f = e + g;
    }
    // outerloop :
    var i,j int;
    for i = 1 ; i < 10 ; i = i + 1{
      // break;
      for j = i ; j < 20 ; j = j + 1{
        if i%2 == 0 {
            var a integer;
            m = e;
            // continue;
        } else {
            var b charere;
            f = e + g;
            // continue outerloop;
        }
        e = 2 + 4;
        if j%2 == 0 {
          f = e*g;
          break;
        }
        if i+j % 25 == 0{
          // break outerloop;
        }
      }
    }
    //
    // // You can have an `if` statement without an else.
    // if  8%4 == 0 {
    //     const amit string;
    // };

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
