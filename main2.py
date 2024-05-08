# This is a new attempt to define an guideline for the development of the DeepGenome
# Documentation at https://docs.google.com/document/d/1low-DnPADNhektL5gF9kQEo-727Tjeqt21KLjI1mFcM
import random


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

        self.vars = {} # vars info

        self.tensors = [i for i in range(0, len(self.inputs))]
        for tensor in self.tensors:
            var = VarInfo('Tensor', tensor)
            var.dependsOn.append(tensor)
            self.vars['Tensor:'+str(tensor)] = var

        self.defaults = []
        self.defaultsCalled = []

        self.numbers = []

        self.outs = [i for i in range(0, len(self.outputs))]
        self.assignedOuts = {}

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
                            if default in self.defaultsCalled:
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
                fun = op[2]
                args = self.funcsArgs[fun]
                num = (len(op)-3) // 2
                arg = args[num]

                type = arg[0]

                if self.forecast(op, type):
                    options.append(type)

                if type == 'Number':
                    options.append('Tensor')

                if len(arg) == 2:
                    options.append('NULL')

                if fun == 'SET':
                    options.append('INTEGER')

            case 4:
                funType = op[0]
                type = op[len(op)-1]

                match type:
                    case 'NULL':
                        fun = op[2]
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

                        if funType == 'Number':
                            options.pop()
                    case 'Tensor':
                        for tensor in self.tensors:
                            options.append(tensor)

                        if funType == 'Tensor':
                            options.pop()

        return options

    def forecast(self, op, next):
        op = op[:]
        op.append(next)
        opts = self.getOptions(op)
        return len(opts) > 0

    def select(self, next):
        pos = len(self.curOp)

        self.curOp.append(next)

        status = pos
        if status > 2:
            status = ((status - 3) % 2) + 3

        match status:
            case 1:
                type = self.curOp[0]
                match type:
                    case 'Tensor':
                        if next in self.defaults:
                            self.defaults.remove(next)
                            self.defaultsCalled.remove(next)
                        else:
                            self.tensors.append(next)
                    case 'Number':
                        self.numbers.append(next)
                    case 'Out':
                        if next not in self.outs:
                            self.outs.append(next)

                var = VarInfo(type, next)
                self.vars[type+':'+str(next)] = var
                self.curOpOutVar = var

            case 2:
                if next == 'DEFAULT':
                    tensor = self.curOp[1]
                    self.defaults.append(tensor)

            case 4:
                type = self.curOp[pos-1]

                var = None
                if type == 'Tensor':
                    var = self.vars[type+':'+str(next)]
                    self.curOpOutVar.dependsOn.extend(var.dependsOn)

                if type == 'Tensor':
                    if next in self.defaults:
                        self.defaultsCalled.append(next)

                fun = self.curOp[2]

                if fun == 'ASSIGNOUT':
                    self.curOpOutVar.dependsOn = var.dependsOn
                    self.assignedOuts[self.curOpOutVar.number] = self.curOpOutVar

                args = self.funcsArgs[fun]
                return pos == ((len(args)-1)*2)+4

        return False

    def isComplete(self):
        if len(self.assignedOuts.values()) < len(self.outputs):
            return False;

        usedInputs = []

        for var in self.assignedOuts.values():
            for dep in var.dependsOn:
                if dep not in usedInputs:
                    usedInputs.append(dep)

        return len(usedInputs) == len(self.inputs)

    def randomUpTo(self, upTo):
        self.reset()

        n = 0
        while n < upTo:
            opts = self.getOptions()

            if len(opts) == 0:
                print(self.curOp)
                print(self.ops)
                print("debug")

            sel = random.choice(opts)

            if self.select(sel):
                self.ops.append(self.curOp)
                self.curOp = []
                n += 1

        print(self.ops)

    def randomUntilComplete(self):
        self.reset()

        while True:
            opts = self.getOptions()
            sel = random.choice(opts)

            if self.select(sel):
                self.ops.append(self.curOp)
                self.curOp = []

                if self.isComplete():
                    return self.ops

    def print(self):
        for op in self.ops:
            print(op)

    def optimize(self):
        ops = []

        dependsOn = []
        outs = []

        def addDepends(dep):
            if dep not in dependsOn:
                dependsOn.append(dep)

        for i in range(0, len(self.ops)):
            ii = len(self.ops) - i - 1
            op = self.ops[ii]

            fun = op[2]
            if fun == 'ASSIGNOUT':
                if op[1] not in outs:
                    outs.append(op[1])
                    addDepends(op[3]+':'+str(op[4]))
                    ops.insert(0, op)
            else:
                out = op[0]+':'+str(op[1])
                if out in dependsOn:
                    i = 3
                    while i < len(op):
                        if op[i] not in ['NULL', 'INTEGER']: # just to be clear
                            addDepends(op[i]+':'+str(op[i+1]))
                        i += 2
                    ops.insert(0, op)

        # Scale Tensors
        tensors = []
        numbers = []

        for dep in dependsOn:
            spl = dep.split(':')
            if spl[0] == 'Tensor':
                tensors.append(int(spl[1]))
            if spl[0] == 'Number':
                numbers.append(int(spl[1]))

        tensors.sort()
        numbers.sort()

        for op in ops:
            if op[0] == 'Tensor':
                op[1] = tensors.index(op[1])
            if op[0] == 'Number':
                op[1] = numbers.index(op[1])

            i = 3
            while i < len(op):
                if op[i] == 'Tensor':
                    op[i+1] = tensors.index(op[i+1])
                if op[i] == 'Number':
                    op[i+1] = numbers.index(op[i+1])
                i += 2

        self.ops = ops
        return ops

    def calculateVars(self):
        self.vars = {}

        def addVar(type, next):
            var = VarInfo(type, next)
            self.vars[type + ':' + str(next)] = var

        for op in self.ops:
            if op[0] in ['Tensor', 'Number', 'Out']:
                addVar(op[0], op[1])

            i = 3
            while i < len(op):
                if op[i] in ['Tensor', 'Number', 'Out']:
                    addVar(op[i], op[i+1])
                i += 2



class VarInfo:
    def __init__(self, type, number):
        self.type = type
        self.number = number
        self.dependsOn = []

###
### Instance agent
###

calc = Calculator()
calc.inputs.append((200, 3)) # vision, 1d, with colors
calc.inputs.append((16,)) # nose, with 16 tonalities
calc.inputs.append((16,)) # hearing, with 16 frequencies
calc.inputs.append((3,)) # life status (hunger, energy, health)

calc.outputs.append((1,)) # move forward
calc.outputs.append((1,)) # rotate (negative for left, positive for right)
calc.outputs.append((1,)) # eat
calc.outputs.append((1,)) # grab
calc.outputs.append((1,)) # blow
calc.outputs.append((1,)) # kiss
calc.outputs.append((1,)) # bite
calc.outputs.append((4, 2)) # speak (the first number indicate the frequency, and the second the amplitude, up to 4 frequencies at the same time)

# Test random generation
calc.randomUntilComplete()
calc.optimize()
calc.print()