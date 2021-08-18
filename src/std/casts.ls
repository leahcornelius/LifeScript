// Prodives casters for the generic types
// It does this using the compilers built in Type Caster classes (accessed via the internal method keywords)
module :: {
    export unsafe func Str(a: Any) {
        let expr = internal method ToString(a); 
        return internal method eval(expr); // eval is a compiler built in method that resolves an ast node's value
    }
    
    export unsafe func Int(a: Any) {
        let expr = internal method ToInt(a);
        return internal method eval(expr);
    }
    
    export unsafe func Float(a: Any) {
        let expr = internal method ToFloat(a);
        return internal method eval(expr);
    }
}