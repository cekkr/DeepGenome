# This is a new attempt to define an guideline for the development of the DeepGenome

# The Calculator have to execute the DeepDNA and calculate possible options
class Calculator:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.reset()

    def reset(self):
        self.ops = []
        self.curOp = []

        self.tensors = []
        self.defaults = []

        self.numbers = []

        self.outs = [i for i in range(0, len(self.outputs))]

    def getOptions(self, op=None):
        if op is None:
            op = self.curOp

        # Operation status:
        # 0. Output type
        # 1. Output number
        # 2. Operation
        # 3. Input type
        # 4. Input number
        status = len(op)
        if status > 2:
            status = ((status - 3) % 2) + 3

        options = []

        match status:
            case 0:
                options.append('Tensor')
                options.append('Number')
                if self.forecast(op, 'Out'):
                    options.append('Out')

            case 1:
                type = op[len(op)-1]

                match type:
                    case 'Tensor':
                        options.append(len(self.tensors))

                        for default in self.defaults:
                            options.append(default)
                    case 'Out':
                        for out in self.outs:
                            if self.forecast(op, out):
                                options.append(out)
                    case 'Number':
                        options.append(len(self.numbers))

    def forecast(self, op, next):
        op = op[:]
        op.append(next)
        opts = self.getOptions(op)
        return len(opts) > 0

