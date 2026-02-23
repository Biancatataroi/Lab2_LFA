"""
Given that:
AF = (Q,∑,δ,q0,F)
Variant 26
Q = {q0,q1,q2,q3},
∑ = {a,b,c},
F = {q3},
δ(q0,a) = q1,
δ(q1,b) = q1,
δ(q1,a) = q2,
δ(q0,a) = q0,
δ(q2,c) = q3,
δ(q3,c) = q3 
"""
from finite_automaton import FiniteAutomaton

def build():
    Q = {"q0", "q1", "q2", "q3"}
    Sigma = {"a", "b", "c"}
    F = {"q3"}
    q0 = "q0"

    delta = {
        ("q0", "a"): {"q0", "q1"},   # two destinations = nondeterminism
        ("q1", "b"): {"q1"},
        ("q1", "a"): {"q2"},
        ("q2", "c"): {"q3"},
        ("q3", "c"): {"q3"},
    }

    return FiniteAutomaton(Q, Sigma, delta, q0, F)

def main():
    fa = build()
    print(" Variant 26 Finite Automaton ")
    print("States:", fa.Q)
    print("Alphabet:", fa.Sigma)
    print("Start:", fa.q0)
    print("Final:", fa.F)

    print("\nIs deterministic?", fa.is_deterministic())

    g = fa.to_regular_grammar()
    print("Chomsky:", g.classify_chomsky())


    # Task 3(c): NDFA -> DFA
    print("\n NDFA to DFA ")
    dfa = fa.to_dfa()

    print("DFA states:", dfa.Q)
    print("DFA start:", dfa.q0)
    print("DFA final:", dfa.F)
    print("DFA deterministic?", dfa.is_deterministic())

    print("\nDFA transitions:")
    for (s, a), nxt in dfa.delta.items():
        print(f"δ({s}, {a}) = {next(iter(nxt))}")

    # Optional demo
    print("\n Test words ")
    for w in ["a", "aac", "abbbc", "ac", "aaaccc"]:
        print(f"{w} ->", "ACCEPT" if fa.accepts(w) else "REJECT")


if __name__ == "__main__":
    main()