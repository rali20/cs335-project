func print_int(n int);
func print_str(s string);
func read_int() int;

type hello struct{
       int a;
       float b;
};

type hello_world struct  {
       int a;
       float b;
};

func get_a(struct hello k)int {
       return k.a;
}

int main() {
       int b;
       int a;
       struct hello k;
       a = k.a;
}

// int main() {
//        int b;
//        int a;
//        struct hello k;
//        a = k.b;
// }
//
// int main() {
//        int b;
//        int a;
//        struct hello k;
//        a = k.a;
// }
//
// int main() {
//        int b;
//        int a;
//        struct hello k;
//        a = get_a(k);
// }
