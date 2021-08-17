# And implmentation of all the logic gates
# They can be evalutated in python using the eval() function
# Or compiled into a NeuralNetwork using compile()
from neural_network import NeuralNetwork


class Gate:
    def __init__(self, inputs):
        self.inputs = inputs

    def get_name(self):
        return self.name

    def get_inputs(self):
        return self.inputs


class And(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "AND"
        self.one = one
        self.two = two

    def eval(self):
        return self.one and self.two

    # LSASM representation
    def __str__(self):
        return "AND " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != "AND":
            raise Exception("Not AND operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("AND gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):
        layers = [
            NeuralNetwork.Layer(3, None,
                                [NeuralNetwork.Neuron(0, False, 1), NeuralNetwork.Neuron(
                                    0), NeuralNetwork.Neuron(0)],
                                [-1, 1, 1]),
            NeuralNetwork.Layer(1, None, [NeuralNetwork.Neuron(
                0)],
                [1]),  # Output layer
        ]
        return NeuralNetwork(layers)


class Or(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "OR"
        self.one = one
        self.two = two

    def eval(self):
        return self.one or self.two

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != self.name:
            raise Exception("Not OR operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("OR gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):  # TODO: Implement the rest of the logic gates as NN (https://medium.com/@stanleydukor/neural-representation-of-and-or-not-xor-and-xnor-logic-gates-perceptron-algorithm-b0275375fea1)
        layers = [
            NeuralNetwork.Layer(3, None,
                                [NeuralNetwork.Neuron(0, False, 1), NeuralNetwork.Neuron(
                                    0), NeuralNetwork.Neuron(0)],
                                [-1, 2, 2]),
            NeuralNetwork.Layer(1, None, [NeuralNetwork.Neuron(
                0)],
                [1]),  # Output layer
        ]
        return NeuralNetwork(layers)


class Nor(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "NOR"
        self.one = one
        self.two = two

    def eval(self):
        return Not(Or(self.one, self.two).eval()).eval()

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != self.name:
            raise Exception("Not NOR operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("NOR gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):
        layers = [
            NeuralNetwork.Layer(3, None,
                                [NeuralNetwork.Neuron(0, False, 1), NeuralNetwork.Neuron(
                                    0), NeuralNetwork.Neuron(0)],
                                [1, -1, -1]),
            NeuralNetwork.Layer(1, None, [NeuralNetwork.Neuron(
                0)],
                [1]),  # Output layer
        ]
        return NeuralNetwork(layers)


class Not(Gate):
    def __init__(self, one):
        Gate.__init__(self, [one])
        self.name = "NOT"
        self.one = one

    def eval(self):
        return not self.one

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one)

    def fromASM(self, asm):
        asm_split = asm.split(" ")
        if asm_split[0] != self.name:
            raise Exception("Not NOT operand")

        self.inputs = [asm_split[1]]
        if (len(self.inputs) != 1):
            raise Exception("Not operand must have 1 input")
        self.one = int(asm_split[1])

    # Returns the neural network representation of the gate
    def compile(self):
        layers = [
            NeuralNetwork.Layer(3, None,
                                [NeuralNetwork.Neuron(0, False, 1), NeuralNetwork.Neuron(
                                    0)],
                                [1, -1]),
            NeuralNetwork.Layer(1, None, [NeuralNetwork.Neuron(
                0)],
                [1]),  # Output layer
        ]
        return NeuralNetwork(layers)

# Complex gates build on top of the above gates


class Nand(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "NAND"
        self.one = one
        self.two = two

    def eval(self):
        return Not(And(self.one, self.two).eval()).eval()

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != self.name:
            raise Exception("Not NAND operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("NAND gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):
        return "Unimplemented"


class Nand(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "NAND"
        self.one = one
        self.two = two

    def eval(self):
        return Not(Or(self.one, self.two).eval()).eval()

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != self.name:
            raise Exception("Not NAND operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("NAND gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):
        layers = [
            NeuralNetwork.Layer(3, None,
                                [NeuralNetwork.Neuron(0, False, 1), NeuralNetwork.Neuron(
                                    0), NeuralNetwork.Neuron(0)],
                                [2, -1, -1]),
            NeuralNetwork.Layer(1, None, [NeuralNetwork.Neuron(
                0)],
                [1]),  # Output layer
        ]
        return NeuralNetwork(layers)


class Xor(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "XOR"
        self.one = one
        self.two = two

    def eval(self):
        return Or(
            And(self.one, Not(self.two).eval()),
            And(Not(self.one), self.two).eval()).eval()

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != self.name:
            raise Exception("Not XOR operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("XOR gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):
        return "Unimplemented"


class Xnor(Gate):
    def __init__(self, one, two):
        Gate.__init__(self, [one, two])
        self.name = "XNOR"
        self.one = one
        self.two = two

    def eval(self):
        return Or(
            And(Not(self.one).eval(), Not(self.two).eval()),
            And(self.one, self.two).eval()).eval()

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one) + "," + str(self.two)

    def fromASM(self, asm):
        asm_split = asm.split(" ").join(",").split(",")
        if asm_split[0] != self.name:
            raise Exception("Not XNOR operand")

        self.inputs = [int(x) for x in asm_split[1:]]
        if (len(self.inputs) != 2):
            raise ValueError("XNOR gate must have 2 inputs")
        self.one = self.inputs[0]
        self.two = self.inputs[1]

    # Returns the neural network representation of the gate
    def compile(self):  # TODO: Implement the rest of the logic gates as NN (https://medium.com/@stanleydukor/neural-representation-of-and-or-not-xor-and-xnor-logic-gates-perceptron-algorithm-b0275375fea1)
        layers = [
            NeuralNetwork.Layer(3, None,
                                [NeuralNetwork.Neuron(0, False, 1), NeuralNetwork.Neuron(
                                    0), NeuralNetwork.Neuron(0)],
                                [1, -1, -1]
                                ),
            NeuralNetwork.Layer(1, None, [NeuralNetwork.Neuron(
                0)],
                [1]),  # Output layer
        ]
        return NeuralNetwork(layers)


class Buffer(Gate):
    def __init__(self, one):
        Gate.__init__(self, [one])
        self.name = "BUFFER"
        self.one = one

    def eval(self):
        return self.one

    # LSASM representation
    def __str__(self):
        return self.name + " " + str(self.one)

    def fromASM(self, asm):
        asm_split = asm.split(" ")
        if asm_split[0] != self.name:
            raise Exception("Not BUFFER operand")

        self.inputs = [asm_split[1]]
        if (len(self.inputs) != 1):
            raise Exception("Buffer operand must have 1 input")
        self.one = int(asm_split[1])

    # Returns the neural network representation of the gate
    def compile(self):
        return "Unimplemented"


class Tests():
    def __init__(self):
        pass

    def tests(self):
        import traceback

        def TestAnd():
            print("Testing AND gate")
            and1 = And(0, 1)
            and2 = And(1, 0)
            and3 = And(1, 1)
            and4 = And(0, 0)

            print("Testing AND gate with eval method")
            assert(and1.eval() == False)
            assert(and2.eval() == False)
            assert(and3.eval() == True)
            assert(and4.eval() == False)
            print("AND gate eval method passed")
            print("Compiling NN")
            and_nn = And(0, 0).compile()
            # Test the compiled NN
            print("Compiled NN, Testing AND gate with compiled NN")
            assert(and_nn.forward_pass([0, 1]) == 0)
            print("0 and 1 passed")
            assert(and_nn.forward_pass([1, 0]) == 0)
            print("1 and 0 passed")
            assert(and_nn.forward_pass([0, 0]) == 0)
            print("0 and 0 passed")
            assert(and_nn.forward_pass([1, 1]) == 1)
            print("1 and 1 passed: AND gate compiled NN passed")
            return True

        def TestOr():
            print("Testing OR gate")
            or1 = Or(0, 1)
            or2 = Or(1, 0)
            or3 = Or(1, 1)

            print("Testing OR gate with eval method")
            assert(or1.eval() == True)
            assert(or2.eval() == True)
            assert(or3.eval() == True)
            print("OR gate eval method passed")
            print("Compiling NN")
            or_nn = Or(0, 0).compile()
            # Test the compiled NN

            print("Compiled NN, Testing OR gate with compiled NN")
            assert(or_nn.forward_pass([0, 1]) == 1)
            print("0 and 1 passed")
            assert(or_nn.forward_pass([1, 0]) == 1)
            print("1 and 0 passed")
            assert(or_nn.forward_pass([0, 0]) == 0)
            print("0 and 0 passed")
            assert(or_nn.forward_pass([1, 1]) == 1)
            print("1 and 1 passed: OR gate compiled NN passed")
            return True

        def TestNot():
            print("Testing NOT gate")
            not1 = Not(0)
            not2 = Not(1)

            print("Testing NOT gate with eval method")
            assert(not1.eval() == 1)
            assert(not2.eval() == 0)
            print("NOT gate eval method passed")
            print("Compiling NN")
            not_nn = Not(0).compile()
            # Test the compiled NN
            print("Compiled NN, Testing NOT gate with compiled NN")
            assert(not_nn.forward_pass([0]) == 1)
            print("0 passed")
            assert(not_nn.forward_pass([1]) == 0)
            print("1 passed")
            print("NOT gate compiled NN passed")
            return True

        def TestXor():
            print("Testing XOR gate")
            xor1 = Xor(0, 1)
            xor2 = Xor(1, 0)
            xor3 = Xor(1, 1)
            xor4 = Xor(0, 0)

            print("Testing XOR gate with eval method")
            assert(xor1.eval() == True)
            assert(xor2.eval() == False)
            assert(xor3.eval() == True)
            assert(xor4.eval() == False)
            print("XOR gate eval method passed")
            print("Compiling NN")
            xor_nn = Xor(0, 0).compile()
            # Test the compiled NN
            print("Compiled NN, Testing XOR gate with compiled NN")
            assert(xor_nn.forward_pass([0, 1]) == 1)
            print("0 and 1 passed")
            assert(xor_nn.forward_pass([1, 0]) == 1)
            print("1 and 0 passed")
            assert(xor_nn.forward_pass([0, 0]) == 0)
            print("0 and 0 passed")
            assert(xor_nn.forward_pass([1, 1]) == 0)
            print("1 and 1 passed: XOR gate compiled NN passed")
            return True

        def TestBuffer():
            print("Testing BUFFER gate")
            buffer1 = Buffer(0)
            buffer2 = Buffer(1)

            print("Testing BUFFER gate with eval method")
            assert(buffer1.eval() == 0)
            assert(buffer2.eval() == 1)
            print("BUFFER gate eval method passed")
            print("Compiling NN")
            buffer_nn = Buffer(0).compile()
            # Test the compiled NN
            print("Compiled NN, Testing BUFFER gate with compiled NN")
            assert(buffer_nn.forward_pass([0]) == 0)
            print("0 passed")
            assert(buffer_nn.forward_pass([1]) == 1)
            print("1 passed")
            print("BUFFER gate compiled NN passed")
            return True

        # Run tests
        print("Starting 1 tests")
        try:
            TestAnd()
            print("Test: TestAnd passed")
        except Exception as e:
            traceback.print_exc()
            print("Failed: " + str(e))


Tests().tests()
