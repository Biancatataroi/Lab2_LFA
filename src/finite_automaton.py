class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def is_deterministic(self):
        for (state, symbol), next_states in self.delta.items():
            if len(next_states) != 1:
                return False
        return True
    
    def to_regular_grammar(self):
        from grammar import Grammar, EPS
        VN = frozenset(self.Q)
        VT = frozenset(self.Sigma)
        P = {A: set() for A in VN}
        S = self.q0

        for (q, a), next_states in self.delta.items():
            for p in next_states:
                P[q].add(a + p)
                if p in self.F:
                    P[q].add(a)

        for f in self.F:
            P[f].add(EPS)

        return Grammar(VN=VN, VT=VT, P=P, S=S)



    def to_dfa(self):

        def name(state_set):
            return "{" + ",".join(sorted(state_set)) + "}"

        start = frozenset([self.q0])
        unprocessed = [start]
        seen = {start}

        dfa_states = {name(start)}
        dfa_delta = {}
        dfa_finals = set()

        while unprocessed:
            S = unprocessed.pop(0)
            S_name = name(S)

            if any(q in self.F for q in S):
                dfa_finals.add(S_name)

            for a in self.Sigma:
                T = set()

                for q in S:
                    T |= self.delta.get((q, a), set())

                if not T:
                    continue

                T = frozenset(T)
                T_name = name(T)

                dfa_states.add(T_name)
                dfa_delta[(S_name, a)] = {T_name}

                if T not in seen:
                    seen.add(T)
                    unprocessed.append(T)

        return FiniteAutomaton(
            Q=dfa_states,
            Sigma=self.Sigma,
            delta=dfa_delta,
            q0=name(start),
            F=dfa_finals
        )

 
    def accepts(self, word):
        current = {self.q0}

        for ch in word:
            next_states = set()

            for q in current:
                next_states |= self.delta.get((q, ch), set())

            current = next_states

            if not current:
                return False

        return any(q in self.F for q in current)

