#! /usr/bin/env python3
#
# Implements a model where each individual is either a "halfer"
# (produces male and female offspring in equal proportion) or a
# "daughters only" variant. The offspring sex ratio is the average of
# the two parents' traits, so a halfer and a daughters-only will
# together produce 3/4 daughters.
#
# Half of the offspring will inherit the father's daughter/halfer
# status, and half will inherit the mother's. This almost certainly
# isn't how any genetically heritable traits work, but at least it's
# simple to model.

import collections
from fractions import Fraction as F

DM = 'DAUGHTER_MALES'
HM = 'HALFER_MALES'
DF = 'DAUGHTER_FEMALES'
HF = 'HALFER_FEMALES'
ALL_M = [DM, HM]
ALL_F = [DF, HF]

state = {
    DM: 100,
    HM: 100,
    DF: 100,
    HF: 100,
    }
state = {k:F(v) for k,v in state.items()}

# TODO: ask mendel how to genetics
def gen_outcome(fraction_m, fraction_d):
    fraction_m, fraction_d = map(F, [fraction_m, fraction_d])
    return {
        DF: (1 - fraction_m) * fraction_d,
        DM: fraction_m * fraction_d,
        HF: (1 - fraction_m) * (1 - fraction_d),
        DF: fraction_m * (1 - fraction_d),
    }

"""
pairing_outcomes = {
    (DM, DF): {DF: F(1)},
    (DM, HF): {DF: F(3/4)*F(1/2), HF: F(3/4)*F(1/2), DM: F(1/4)*F(1/2), HM: F(1/4)*F(1/2)},
    (HM, DF): 1,
    (HM, HF): 1,
}
"""

pairing_outcomes = {
    (DM, DF): gen_outcome(0, 1),
    (DM, HF): gen_outcome(F(1,4), F(1,2)),
    (HM, DF): gen_outcome(F(1,4), F(1,2)),
    (HM, HF): gen_outcome(F(1,2), 0),
}

for p in pairing_outcomes:
    assert sum(pairing_outcomes[p].values()) == 1, (p, pairing_outcomes[p])

def evolve(state):
    sum_m = sum(state[x] for x in ALL_M)
    sum_f = sum(state[x] for x in ALL_F)

    pairings = min(sum_m, sum_f)
    print(sum_m, 'male', sum_f, 'female', '->', pairings, 'pairings')

    new_state = collections.defaultdict(F)

    for m,f in itertools.product(ALL_M, ALL_F):
        count = m / sum_m * f / sum_f * pairings
        print(m, state[m], f, state[f], '->', count)
