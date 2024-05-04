
class DeepDNA:
    def __init__(self):
        self.inputs = []
        self.outputs = []

        self.operations = []

        ###
        ### LINEAR
        ###
        opLinear = DeepDNA_Operation('LINEAR')
        opLinear.args = ['OUTPUT_SIZE']
        self.operations.append(opLinear)

        ###
        ### ADD
        ###
        opAdd = DeepDNA_Operation('ADD')

        def opAdd_validation(inputs, args, output):
            size = inputs[0].size
            for input in inputs:
                if input.size != size:
                    return False
            return True
        opAdd.validationFunc = opAdd_validation

        self.operations.append(opAdd)

    def generate(self):
        self.numVars = len(self.inputs)
        self.unusedInputs = self.inputs[:]

class DeepDNA_Var:
    def __init__(self):
        self.size = -1

class DeepDNA_Operation:
    def __init__(self, name):
        self.name = name
        self.args = []
        self.validationFunc = None

    def validation(self):
        if self.validationFunc:
            return self.validationFunc()

        return True

class DeepDNA_Sequence:
    def __init__(self):
        self.output = None
        self.inputs = []
        self.operation = None
        self.arguments = []

###
### Example
###

dna = DeepDNA()
dna.inputs.append((200, 3)) # vision, 2d, with colors
dna.inputs.append((16)) # nose, with 16 tonalities
dna.inputs.append((16)) # hearing, with 16 frequencies
dna.inputs.append((3)) # life status (hunger, energy, health)

dna.outputs.append((1)) # move forward
dna.outputs.append((1)) # rotate (negative for left, positive for right)
dna.outputs.append((1)) # eat
dna.outputs.append((1)) # grab
dna.outputs.append((1)) # blow
dna.outputs.append((1)) # kiss
dna.outputs.append((1)) # bite
dna.outputs.append((4, 2)) # speak (the first number indicate the frequency, and the second the amplitude, up to 4 frequencies at the same time)

