package main;

import "fmt";
import (
  . "str";
  cplx "complex";
);
type new_int int;
type new_new_int new_int;
var glob new_new_int;
var naya_structure struct {
  a,b,c int
};
func main(a int, b string) int{

    // const (
    //   c0 = 1;  // c0 == 0
    //   c1 = 2.0;  // c1 == 1
    //   c2, c3 string = "amit", "yadav";  // c2 == 2
    //   a,b int;
    // );
    // const c = 2 + 3;
    // Here's a basic example.
    var e,f,g = "amit", 2, 3.0;
    // e = 10;
    f = 2 + 4;
    // c = 10;
    // if 7%2 == 0 {
    //     var a integer;
    // } else {
    //     var b charere;
    // };
    //
    // // You can have an `if` statement without an else.
    if g := 2; 8%4 == 0 {
        const amit string = "amit";
    };

    // A statement can precede conditionals; any variables
    // declared in this statement are available in all
    // branches.
    // if num := 9; num < 0 {
    // } else if num < 10 {
    //
    // } else {
    //     Println(num, "has multiple digits")
    // }
};
