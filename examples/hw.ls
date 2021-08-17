func functionName(arg1: String, arg2: String) {
    var inner_var = "inner";
    print(arg1 + arg2);
    print(1);
}
var arg1 = "OW";
functionName(arg1 = "Hello", arg2 = " World");
print(arg1 + " " + typeof inner_var);
let inner_var = "notinner";
if (inner_var == "inner") { 
    print("Problem"); 
} { 
    let inner_defined_var = "This var has been defined inside the functions else loop, and so will be null() when accessed outside of it";
    print("All is ok, the scope has worked, and inner_var is eq to: " + inner_var); 
    print("The inner_defined_var is: " + inner_defined_var);
}

print("The inner_defined_var is:" + str(inner_defined_var));