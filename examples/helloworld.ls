// This is a comment
/* This is also a comment */
func ma(extra: String, other: Number = 2) {
    print("hello world!");
    print(extra);
    print(other % 2);
}
let varr = "Coded by Leo Cornelius :)";
ma(extra=varr); // Use the default value of the other parameter
ma(other=5); // Leave extra as Null()
ma(other=5, extra="varr"); // Pass the arguments in reverse