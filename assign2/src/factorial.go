package fac;

import (
	"fmt";
);

func fact(n int_t) int_t {
	if n==1 {
		return 1;
	};
	return n*fact(n-1);
};

func main() {
	var n int_t;
};
