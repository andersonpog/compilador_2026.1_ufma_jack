from enum import Enum


class Segment(Enum):
    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class Command(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VMWriter:
    def __init__(self):
        self.vm_output = []

    def vmOutput(self):
        return "".join(self.vm_output)

    def writePush(self, segment, index):
        self.vm_output.append(f"push {segment.value} {index}\n")

    def writePop(self, segment, index):
        self.vm_output.append(f"pop {segment.value} {index}\n")

    def writeArithmetic(self, command):
        self.vm_output.append(f"{command.value}\n")

    def writeLabel(self, label):
        self.vm_output.append(f"label {label}\n")

    def writeGoto(self, label):
        self.vm_output.append(f"goto {label}\n")

    def writeIf(self, label):
        self.vm_output.append(f"if-goto {label}\n")

    def writeCall(self, name, nArgs):
        self.vm_output.append(f"call {name} {nArgs}\n")

    def writeFunction(self, name, nLocals):
        self.vm_output.append(f"function {name} {nLocals}\n")

    def writeReturn(self):
        self.vm_output.append("return\n")