import numpy as np
import math

class NeuralNetwork():
    class Neuron():
        def __init__(self, bias, input=True, fixed_value=None):
            self.bias = bias
            self.input = input
            self.fixed_value = fixed_value

        def __repr__(self):
            return "Neuron(bias={}, input={}, fixed_value={})".format(self.bias, self.input, self.fixed_value)

    class Layer():
        def __init__(self, num_nodes, activation_function, input_nodes, weights=None):
            self.num_nodes = num_nodes
            self.activation_function = activation_function or self.def_activation_function
            self.weights = np.random.rand(
                num_nodes, 1) if weights is None else weights
            self.input_nodes = input_nodes

        def forward_pass(self, input_vector):
            new_input = []
            offset = 0
            if(type(input_vector) is not list):
                input_vector = [input_vector]
            # Reshape the input_vector to account for the fixed nodes
            for i, inputNode in enumerate(self.input_nodes):
                if inputNode.input:
                    new_input.append(input_vector[i - offset])
                else:
                    new_input.append(inputNode.fixed_value)
                    offset += 1
            self.input = new_input
            self.output = self.activation_function(new_input)
            return self.output

        def backward_pass(self, output_error, learning_rate):
            output_error = output_error * \
                self.activation_function(self.output, deriv=True)
            self.weights -= learning_rate * np.dot(output_error, self.input.T)
            return output_error

        # TODO add more activation functions
        def def_activation_function(self, input):
            out = [(self.weights[index] * i) for index, i in enumerate(input)]
            return max(0, sum(out))

    def __init__(self, layers):
        if len(layers) < 2:
            raise ValueError("Not enough layers")
        self.layers = layers

    def forward_pass(self, input_vector):
        output = input_vector
        for layer in self.layers:
            output = layer.forward_pass(output)
        return output

    def backward_pass(self, output_error, learning_rate):
        output_error = output_error
        for layer in reversed(self.layers):
            output_error = layer.backward_pass(output_error, learning_rate)

        return output_error

    def train(self, input_vectors, output_vectors, learning_rate=0.1, epochs=100):
        print(
            f"Starting training, epochs: {epochs}, vectors count: {len(input_vectors)}, learning_rate: {learning_rate}")
        for epoch in range(epochs):
            print(f"Epoch {epoch}")
            for i in range(len(input_vectors)):
                print(f"Input: {input_vectors[i]}")
                output = self.forward_pass(input_vectors[i])
                error = output_vectors[i] - output
                print(
                    f"Output: {output}, Expected: {output_vectors[i]}, Error: {error}")
                self.backward_pass(error, learning_rate)
