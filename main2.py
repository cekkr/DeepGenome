# This is a new attempt to define an guideline for the development of the DeepGenome
# Documentation at https://docs.google.com/document/d/1low-DnPADNhektL5gF9kQEo-727Tjeqt21KLjI1mFcM

# The Calculator have to execute the DeepDNA and calculate possible options
class Calculator:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.reset()

        self.tensorFunctions = [
            'LINEAR',
            'ADD',
            'CONCAT',
            'CONV1D',
            'GRU',
            'DEFAULT'
        ]

        self.numberFunctions = [
            'SET',
            'SUM',
            'SUB',
            'DIV',
            'MUL'
        ]

        self.outFunctions = ['ASSIGNOUT']

        self.funcsArgs = {
            'LINEAR': [['Number']],
            'ADD': [['Tensor'], ['Tensor']],
            'CONCAT': [['Tensor'], ['Tensor']],
            'CONV1D': [['Tensor'], ['Number'], ['Number'], ['Number'], ['Number', 1], ['Number', 0]],
            'GRU': [['Tensor'], ['Number'], ['Number', 1]],
            'DEFAULT': [['Number']],

            'ASSIGNOUT': [['Tensor']],

            'SET': [['Number']],
            'SUM': [['Number'], ['Number']],
            'SUB': [['Number'], ['Number']],
            'DIV': [['Number'], ['Number']],
            'MUL': [['Number'], ['Number']],
        }

        self.maxIntegerNumber = 2 # 0, 1, 2

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
                type = op[0]

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

            case 2:
                type = op[0]

                match type:
                    case 'Tensor':
                        for fun in self.tensorFunctions:
                            if self.forecast(op, fun):
                                options.append(fun)
                    case 'Out':
                        for fun in self.outFunctions:
                            if self.forecast(op, fun):
                                options.append(fun)
                    case 'Number':
                        for fun in self.numberFunctions:
                            if self.forecast(op, fun):
                                options.append(fun)

            case 3:
                fun = op[3]
                args = self.funcsArgs[fun]
                num = (len(op)-3) // 2
                arg = args[num]

                type = arg[0]

                if self.forecast(op, type):
                    options.append(type)

                if type is 'Number':
                    options.append('Tensor')

                if len(arg) == 2:
                    options.append('NULL')

                if fun is 'SET':
                    options.append('INTEGER')

            case 4:
                type = op[len(op)-1]

                match type:
                    case 'NULL':
                        fun = op[3]
                        args = self.funcsArgs[fun]
                        num = (len(op) - 3) // 2
                        arg = args[num]
                        options.append(arg[1])
                    case 'INTEGER':
                        for i in range(0, self.maxIntegerNumber+1):
                            options.append(i)
                    case 'Number':
                        for num in self.numbers:
                            options.append(num)
                    case 'Tensor':
                        for tensor in self.tensors:
                            options.append(tensor)

        return options

    def forecast(self, op, next):
        op = op[:]
        op.append(next)
        opts = self.getOptions(op)
        return len(opts) > 0

