import random

def calculate_total_size(shape):
    total_size = 1
    for dim in shape:
        total_size *= dim
    return total_size

class DeepDNA:
    def __init__(self):
        self.inputs = []
        self.outputs = []

        self.operations = []

        ###
        ### LINEAR
        ###
        opLinear = DeepDNA_Operation('LINEAR')
        #opLinear.args = ['OUTPUT_SIZE']
        opLinear.numInputs = 1
        self.operations.append(opLinear)

        ###
        ### ADD
        ###
        opAdd = DeepDNA_Operation('ADD')
        opAdd.numInputs = 2

        def result_shape_of_tensor_sum(shape1, shape2):
            # Ensure the shorter shape is padded with ones on the left
            if len(shape1) > len(shape2):
                shape2 = (1,) * (len(shape1) - len(shape2)) + shape2
            else:
                shape1 = (1,) * (len(shape2) - len(shape1)) + shape1

            # Calculate the resulting shape
            resulting_shape = tuple(max(dim1, dim2) for dim1, dim2 in zip(shape1, shape2))

            return (resulting_shape)

        opAdd.resultingSize = result_shape_of_tensor_sum

        self.operations.append(opAdd)

        ###
        ### ASSIGNOUT
        ###
        opAssignOut = DeepDNA_Operation('ASSIGNOUT')
        opAssignOut.numInputs = 1
        self.operations.append(opAssignOut)

        def opAssignOut_validation(inputs, args, output):
            return inputs[0].size == output.size

    def normalize(self):
        for i in range(0, len(self.inputs)):
            self.inputs[i] = calculate_total_size(self.inputs[i])
        for i in range(0, len(self.outputs)):
            self.outputs[i] = calculate_total_size(self.outputs[i])

    def generate(self):
        usedInputs = []
        flow = []
        vars = []
        outs = []
        outputs = []

        i = 0
        for input in self.inputs:
            var = DeepDNA_Var()
            var.size = input
            var.dependsOn.append(i)
            var.num = i
            i += 1
            vars.append(var)

        i = 0
        for output in self.outputs:
            var = DeepDNA_Var()
            var.size = output
            var.num = i
            i += 1
            outs.append(var)

        def availableOperations():
            ops = []
            for op in self.operations:
                if op.name == 'LINEAR':
                    ops.append(op)
                if op.name == 'ADD':
                    sameSize = []
                    for var in vars:
                        if var.size in sameSize:
                            ops.append(op)
                            break
                        else:
                            sameSize.append(var.size)
                if op.name == 'ASSIGNOUT':
                    ops.append(op)
                    continue
                    # disabled
                    for out in outs:
                        for var in vars:
                            if out.size == var.size:
                                ops.append(op)
                                continue
            return ops


        while len(usedInputs) < len(self.inputs) or len(outputs) < len(self.outputs):
            ops = availableOperations()
            seq = DeepDNA_Sequence(self)
            seq.operation = random.choices(ops)[0]
            seq.choose(vars, outs)

            if seq.operation.name == 'ASSIGNOUT':
                if seq.output not in outputs:
                    outputs.append(seq.output)

                usedInputs = []
                for output in outputs:
                    for depend in output.dependsOn:
                        if depend not in usedInputs:
                            usedInputs.append(depend)

            flow.append(seq)

        self.flow = flow
        return flow

    def printFlow(self):

        def varStr(var):
            return str(var.num) + ':' + str(var.size)

        for seq in self.flow:
            inputs = ''
            for input in seq.inputs:
                if len(inputs) > 0:
                    inputs += ', '
                inputs += varStr(input)
            print(varStr(seq.output), seq.operation.name, inputs)

    def optimizeFlow(self):
        flow = []

        outs = []
        dependsOn = []
        for i in range(0, len(self.flow)):
            ii = len(self.flow) - i - 1
            seq = self.flow[ii]

            if seq.operation.name == 'ASSIGNOUT':
                if seq.output.num not in outs:
                    dependsOn.extend(seq.output.dependsOn)
                    outs.append(seq.output.num)
                    flow.insert(0, seq)
            else:
                if seq.output.num in dependsOn:
                    flow.insert(0, seq)

        self.flow = flow

class DeepDNA_Var:
    def __init__(self):
        self.size = -1
        self.dependsOn = []

class DeepDNA_Operation:
    def __init__(self, name):
        self.name = name
        self.numInputs = 1
        self.args = []

        self.validationFunc = None

    def validation(self):
        if self.validationFunc:
            return self.validationFunc()
        return True

class DeepDNA_Sequence:
    def __init__(self, dna):
        self.dna = dna

        self.output = None
        self.inputs = []
        self.operation = None
        self.arguments = []

    def choose(self, vars, outs):
        if self.operation.name == 'ASSIGNOUT':
            while len(self.inputs) == 0:
                self.output = random.choices(outs)[0]
                vars = vars[:]
                random.shuffle(vars)
                for var in vars:
                    if var.size == self.output.size or True:
                        self.inputs.append(var)
                        break
        else:
            self.output = DeepDNA_Var()
            self.output.num = len(vars)
            vars.append(self.output)

            if self.operation.name == 'LINEAR':
                input = random.choices(vars)[0]
                self.inputs.append(input)
                while self.output.size > 0:
                    self.output.size = input.size + random.randint(-10, 10)
                self.output.dependsOn.extend(input.dependsOn)

            if self.operation.name == 'ADD':
                while True:
                    input1 = random.choices(vars)[0]
                    input2 = random.choices(vars)[0]

                    if input1 != input2:
                        self.inputs.append(input1)
                        self.inputs.append(input2)
                        self.output.size = self.operation.resultingSize((input1.size,), (input2.size,))[0]
                        break

        for input in self.inputs:
            self.output.dependsOn.extend(input.dependsOn)
            self.output.dependsOn.append(input.num)


###
### Example
###

dna = DeepDNA()
dna.inputs.append((200, 3)) # vision, 2d, with colors
dna.inputs.append((16,)) # nose, with 16 tonalities
dna.inputs.append((16,)) # hearing, with 16 frequencies
dna.inputs.append((3,)) # life status (hunger, energy, health)

dna.outputs.append((1,)) # move forward
dna.outputs.append((1,)) # rotate (negative for left, positive for right)
dna.outputs.append((1,)) # eat
dna.outputs.append((1,)) # grab
dna.outputs.append((1,)) # blow
dna.outputs.append((1,)) # kiss
dna.outputs.append((1,)) # bite
dna.outputs.append((4, 2)) # speak (the first number indicate the frequency, and the second the amplitude, up to 4 frequencies at the same time)

dna.normalize()

dna.generate()
dna.optimizeFlow()
dna.printFlow()