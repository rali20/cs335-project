func print_int(n int);
// func print_float(n float);
func print_str(s string);
func read_int() int;

func main(){
  var a int = 40;
  var b int = 3;
  // var b float = 20;
  var line string = "\n";


  print_str("Binary Operation Check : integers only\n");
  print_str("Input a : ");
  a = read_int();
  print_str("Input b : ");
  b = read_int();
  print_str("a + b : ");
  print_int(a+b);
  print_str(line);
  print_str("a - b : ");
  print_int(a-b);
  print_str(line);
  print_str("a * b : ");
  print_int(a*b);
  print_str(line);
  print_str("a / b : ");
  print_int(a/b);
  print_str(line);
  print_str("a % b : ");
  print_int(a%b);
  print_str(line);
  // print_str("a && b : ");
  // print_int(a&&b);
  // print_str(line);
  // print_str("a || b : ");
  // print_int(a||b);
  // print_str(line);
  print_str("a == b : ");
  print_int(a==b);
  print_str(line);
  print_str("a != b : ");
  print_int(a!=b);
  print_str(line);
  print_str("a > b : ");
  print_int(a>b);
  print_str(line);
  print_str("a >= b : ");
  print_int(a>=b);
  print_str(line);
  print_str("a < b : ");
  print_int(a<b);
  print_str(line);
  print_str("a <= b : ");
  print_int(a<=b);
  print_str(line);
  print_str("a | b : ");
  print_int(a|b);
  print_str(line);
  print_str("a & b : ");
  print_int(a&b);
  print_str(line);
  print_str("a >> b : ");
  print_int(a>>b);
  print_str(line);
  print_str("a << b: ");
  print_int(a<<b);
  print_str(line);
  print_str("--------------------------------------");
  print_str(line);


  // b = a+1; //should work well
  // a = a/2;
  // a = a%3;
  // a = a*b; //error
  //b = a*b; //should work
  // b = a;
  // a = b+1; //will give type error
  // a = a+1.0; //will give type error
  // c = b; //type mismatch error
  // c = c[1]; error because c is not array
  // print_int(a);
  //print_float(b);
  // print_str(c);
}
