from enum import Enum
from dataclasses import dataclass


class Kind(Enum):
    STATIC = "static"
    FIELD = "field"
    ARG = "arg"
    VAR = "var"


@dataclass
class Symbol:
    name: str
    type: str
    kind: Kind
    index: int


class SymbolTable:
    def __init__(self):
        self.class_scope = {}
        self.subroutine_scope = {}

        self.count_vars = {
            Kind.ARG: 0,
            Kind.VAR: 0,
            Kind.STATIC: 0,
            Kind.FIELD: 0
        }

    def start_subroutine(self):
        self.subroutine_scope.clear()
        self.count_vars[Kind.ARG] = 0
        self.count_vars[Kind.VAR] = 0

    def scope(self, kind):
        if kind in (Kind.STATIC, Kind.FIELD):
            return self.class_scope
        return self.subroutine_scope

    def define(self, name, type_, kind):
        scope_table = self.scope(kind)

        if name in scope_table:
            raise RuntimeError("variable already defined")

        symbol = Symbol(
            name=name,
            type=type_,
            kind=kind,
            index=self.var_count(kind)
        )

        scope_table[name] = symbol
        self.count_vars[kind] += 1

    def resolve(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]

        return self.class_scope.get(name)

    def var_count(self, kind):
        return self.count_vars[kind]