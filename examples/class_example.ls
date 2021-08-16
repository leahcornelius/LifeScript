// An interface that defines a set of methods to be implemented by a class that wants to print to the console.
Printable :: Interface {
    public print(self);
}

// A class that implements the Printable interface and extends no superclass
AddAble :: Class() implements Printable {
    private var a: Number = 1;
    public var some_string: String = "hello";
    public func print(self) {
        print(self.a);
    }
    public func add(self, b: Number) {
        self.a = self.a + b;
    }
}

// A class that implements the Printable interface and parents Subclass
Superclass :: Class() implements Printable {
    public func print(self) {
        print("Superclass");
    }

    public func example_function(self) {
        print("example_function called from");
        print(self._name);
    }
}

// A class that extends Superclass and implements the Printable interface, as well as overiding the print method
Subclass :: Class(Superclass) {
    override func print(self) {
        print("Subclass");
    }
}

var a = new AddAble();
a.add(2);
a.print();
// Demonstrating public varibles

print(a.some_string);
a.some_string += " world";
print(a.some_string);
// The following would error
// print(a.a);
// As a is a private variable
// Demonstrating inheritance & overrides
var b = new Subclass();
b.print();
b.example_function();

var super = new Superclass();
super.print();
super.example_function();

del a, b, super;
print("Class demo over :)");
