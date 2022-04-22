from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # By the premise of the puzzle, if A is a Knight, they cannot be a Knave; and vice versa;
    # In otherwords, AKnight XOR AKnave, which can be represented as (AKnight OR AKnave) AND NOT (AKnight AND AKnave)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # We can interpret this as: if A is a Knight, then what they are saying is true (i.e. implication that AKnight and AKnave are both true)
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a Knave, the opposite is true
    Implication(AKnave, Not(And(AKnight, AKnave)))   
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # Premise of the puzzle; see further explanation in Puzzle 0 above
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A statement - Implication if A is a Knight, then both are knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # A statement - the opposite is true
    Implication(AKnave, Not(And(AKnave, BKnave)))
    # B says nothing
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # Premise
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A statement; if A is a knight, then same kind, meaning (AKnight and BKnight) or (AKnave and BKnave)
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # Then we can use the opposite implication for if A is a Knave by adding Not - direct translation
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # B is a Knight, then Different Kinds, meaning (AKnight and BKnave) or (AKnave and BKnight)
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # B is a Knave, opposite implication
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))

    # Note, we are presenting the most direct translation of the statements (especially when presenting the Knave implications),
    # since we want the AI to infer the rest of the information by itself; thus the consequent for AKnave is simply Not(consequent for AKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # Premise
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    # A said 'I am a knight' OR 'I am a knave' but not both, i.e. XOR, which can be represented as '(P OR Q) AND NOT (P AND Q)'
    # ... where P = A said 'I am a knight' and Q = A said 'I am a knave'
    # ... this is our '(P Or Q)'
    Or(
        # A said 'I am a knight';
        # In this scenario, the implication is if A is a knight, then the consequent is 'A is a knight', and if A is a knave, then the consequent is 'A is not a knight'
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),
        # A said 'I am a knave';
        # Similar structure to above but the consequent is based on 'A is a knave'
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),
    # ... and this is our 'Not (P And Q)'
    Not(
        And(
            # We use the same sentences from above
            # A said 'I am a knight'
            And(
                Implication(AKnight, AKnight),
                Implication(AKnave, Not(AKnight))
            ),
            # A said 'I am a knave'
            And(
                Implication(AKnight, AKnave),
                Implication(AKnave, Not(AKnave))
            )
        )
    ),
    
    # B statement 1; if B is a Knight, then A said 'I am a knave'
    Implication(
        BKnight, 
        # We can borrow the same sentences we used above for "A said 'I am a knave'"
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),
    # if B is a Knave, then A didn't say 'I am a knave', and we just reverse the consequent
    Implication(
        BKnave,
        Not(
            And(
                Implication(AKnight, AKnave),
                Implication(AKnave, Not(AKnave))
            )
        )
    ),
    
    # B statement 2, straightforward sentences
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # C statement, straightforward sentences
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
