# This is a new attempt to define an guideline for the development of the DeepGenome

# The Calculator have to execute the DeepDNA and calculate possible options
class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.ops = []
        self.curOps = []

        # Operation status:
        # 0. Output type
        # 1. Output number
        # 2. Operation
        # 3. Input type
        # 4. Input number
        self.curOpStatus = 0
        
        self.curOpArgs = 0