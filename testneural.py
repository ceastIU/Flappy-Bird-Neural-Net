from math import exp
from random import seed
from random import random

class Net:
    def __init__(self, n_inputs,n_outputs,  height, distance, n_hidden = 5):
        self.inputs = n_inputs
        self.hidden = n_hidden
        self.outputs = n_outputs
        self.network = list()
        self.init_net()
        self.height = height
        self.distance = distance

    # Initialize a network
    def init_net(self):
        self.network = list()
        hidden_layer = [{'weights': [random() for i in range(self.inputs + 1)]} for i in range(self.hidden)]
        self.network.append(hidden_layer)
        output_layer = [{'weights': [random() for i in range(self.hidden + 1)]} for i in range(self.outputs)]
        self.network.append(output_layer)
        #return network

    # Calculate neuron activation for an input
    def activate(self, weights, inputs):
        activation = weights[-1]
        for i in range(len(weights) - 1):
            activation += weights[i] * inputs[i]
        return activation

    # Transfer neuron activation
    def transfer(self, activation):
        return 1.0 / (1.0 + exp(-activation))

    # Forward propagate input to a network output
    def propagate(self, inputs):
        print(inputs)
        inputs = (inputs[0]/self.distance, inputs[1]/self.height)
        for layer in self.network:
            new_inputs = []
            for neuron in layer:
                activation = self.activate(neuron['weights'], inputs)
                neuron['output'] = self.transfer(activation)
                new_inputs.append(neuron['output'])
            inputs = new_inputs
        return inputs

    def get_net(self):
        return self.network
# # Test training backprop algorithm
# #seed(1)
#
# n_inputs = 2
# n_outputs = 1
# network = Net(n_inputs, n_outputs)
# outputs = network.propagate((100, 200))
# print("out", outputs)
# print("net", network)


#
#
# # Calculate the derivative of an output
# def transDerivative(output):
#     return output * (1.0 - output)
#
#
# # Backpropagate error and store in neurons
# def backProp(network, expected):
#     for i in reversed(range(len(network))):
#         layer = network[i]
#         errors = list()
#         if i != len(network) - 1:
#             for j in range(len(layer)):
#                 error = 0.0
#                 for neuron in network[i + 1]:
#                     error += (neuron['weights'][j] * neuron['delta'])
#                 errors.append(error)
#         else:
#             for j in range(len(layer)):
#                 neuron = layer[j]
#                 errors.append(expected[j] - neuron['output'])
#         for j in range(len(layer)):
#             neuron = layer[j]
#             neuron['delta'] = errors[j] * transDerivative(neuron['output'])
#
#
# # Update network weights with error
# def updateWeights(network, row, l_rate):
#     for i in range(len(network)):
#         inputs = row[:-1]
#         if i != 0:
#             inputs = [neuron['output'] for neuron in network[i - 1]]
#         for neuron in network[i]:
#             for j in range(len(inputs)):
#                 neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
#             neuron['weights'][-1] += l_rate * neuron['delta']
#
#
# # Train a network for a fixed number of epochs
# def trainNet(network, train, l_rate, n_epoch, n_outputs):
#     for epoch in range(n_epoch):
#         sum_error = 0
#         for row in train:
#             outputs = propagate(network, row)
#             expected = [0 for i in range(n_outputs)]
#             expected[row[-1]] = 1
#             sum_error += sum([(expected[i] - outputs[i]) ** 2 for i in range(len(expected))])
#             backProp(network, expected)
#             updateWeights(network, row, l_rate)
#         print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, l_rate, sum_error))
