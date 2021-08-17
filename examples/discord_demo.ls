import std::Types::Date; // More complex types are not part of the prelude 

Printable :: Interface {  // This interface is also defined in std::Interfaces::Printable, but we are defining it here for demonstration perpouses
  public print(self) -> Null;
  opt str(self) -> String; // an optional str method that does not have to be implemented and not guarenteed 
  private alreadyImplementedExample() {
    print("This method is provided OOTB when implementing Printable");
  };
}

global Type CustomTypesYay = Any - Number + Implements(Printable); // Any type other than Number that implements Printable will be covered by this Complex Type

Document :: Abstract Class() {
  public var: String name;
  public var: Date createdAt;
  public var: String content;
  public func decodeFromJson(json: String) -> Error::Any/Self {
    let parsed: Self = std.JSON.parse(json)?;
    return passed;
  }
  private func somePrivateMethod(someParameter: CustomTypesYay) -> Any {
    someParamter.print(); // Allowed because CustomTypesYay has explicitly declared candidates must implement printable
    return "Some Random String, because why not";
  }
}

News :: Class(Document) implements Printable {
  constructor(self, name: String, createdAt: Date, content: String) -> Self {
    self.name = name;
    self.createdAt = createdAt;
    self.content = content
    return self
  }
  public func callThePrivateMethod(self) {
    self.name = self.somePrivateMethod(self) // Inherited from the superclass
  }
}

let news = new News("Leo Cornelius, because why not", new Date("12th july 2019"), "The content here... very juicy");
news.callThePrivateMethod();
news.print();
news.name.print(); // same as print(news.name) as std types implement std printable interface