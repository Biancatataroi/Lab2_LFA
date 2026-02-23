from dataclasses import dataclass
from typing import Dict, Set, FrozenSet

EPS = "ε"

@dataclass
class Grammar:
    VN: FrozenSet[str]
    VT: FrozenSet[str]
    P: Dict[str, Set[str]]
    S: str

    def classify_chomsky(self) -> str:
        # If LHS isn't a single nonterminal → Type-0
        for lhs in self.P.keys():
            if lhs not in self.VN:
                return "Type-0 (Unrestricted)"

        # Regular check (right-linear or left-linear)
        right_ok = True
        left_ok = True

        for A, rhss in self.P.items():
            for rhs in rhss:
                if rhs == EPS:
                    continue

                if len(rhs) == 1:
                    if rhs not in self.VT:
                        right_ok = left_ok = False

                elif len(rhs) == 2:
                    x, y = rhs[0], rhs[1]
                    if not (x in self.VT and y in self.VN):
                        right_ok = False
                    if not (x in self.VN and y in self.VT):
                        left_ok = False
                else:
                    right_ok = left_ok = False

        if right_ok or left_ok:
            return "Type-3 (Regular)"

        return "Type-2 (Context-Free)"
