"""disaggregator

In this class, we use list as a main container class.
"""
import copy
import random

from utils_same import *
from context.context import Context

class Disaggregator(object):
    """Disaggregator class"""

    def __init__(self, contexts = None):
        if contexts is None: contexts = set()
        else:
            contexts = set(contexts)

        self.singles = set()
        self.aggregates = set()
        self.used_singles = set()

        # In the disaggregation operation, all the contexts are in list not a set
        for c in contexts:
            if c.is_single():
                self.singles.add(c)
            else:
                self.aggregates.add(c)

    def process_singles(self, singles, aggregates):
        """process the single contexts

        >>> s  = Context(value=0.0, cohorts=[0])
        >>> g1 = Context(value=1.0, cohorts=[0,1])
        >>> g2 = Context(value=2.0, cohorts=[0,2])
        >>> g3 = Context(value=3.0, cohorts=[0,1,2,3,4,5])
        >>> d = Disaggregator()
        >>> new_singles, new_aggregates, new_processed = d.process_singles(set([s]), set([g1, g2]))
        >>> len(new_singles)
        3

        # [1] and [2] should be in the new singles
        >>> s1 = Context(value=0.0, cohorts=[1])
        >>> is_in(s1, new_singles, ignore_value=True)
        True
        >>> s1 = Context(value=0.0, cohorts=[2])
        >>> is_in(s1, new_singles, ignore_value=True)
        True
        >>> s1 = Context(value=0.0, cohorts=[3])
        >>> is_in(s1, new_singles, ignore_value=True)
        False

        # There should be new new aggregates as all of them are consumed
        >>> len(new_aggregates)
        0
        >>> len(new_processed)
        2
        >>> is_in(g1, new_processed)
        True
        >>> is_in(g2, new_processed)
        True
        """

        # We modify singles and aggregates using pop
        # We need to copy them in order not to break the original input
        singles = copy.copy(singles)
        aggregates = copy.copy(aggregates)

        used_singles = set()
        processed_aggregates = set()

        while singles:
            # When there is no aggregate, you have nothing to process
            # So, just flush all the singles into the used_singles and leave
            if not aggregates:
                while singles:
                    used_singles.add(singles.pop())
                break

            # get the first element
            s = singles.pop()
            used_singles.add(s)

            return_singles, return_aggregates, return_processed = self.split(s, aggregates)

            # 1. newly generated single contexts
            # From the newly identified singles, only the singles that are
            # **not** in used_singles are used
            for s in return_singles:
                if not is_in(s, used_singles) and not is_in(s, singles):
                    singles.add(s)

            for a in return_aggregates:
                if not is_in(a, aggregates):
                    aggregates.add(a)

            for p in return_processed:
                aggregates.remove(p)
                processed_aggregates.add(p)

        return used_singles, aggregates, processed_aggregates

    def split(self, input_sub, super_set):
        """Given sub context, and super_set, split the super_set to generate aggregates or singles

        >>> s  = Context(value=0.0, cohorts=[0])
        >>> g1 = Context(value=0.0, cohorts=[0,1])
        >>> g2 = Context(value=0.0, cohorts=[0,2])
        >>> d = Disaggregator()
        >>> new_singles, new_aggregates, processed_aggregates = d.split(s, [g1,g2])
        >>> len(new_singles)
        2
        >>> len(new_aggregates)
        0
        >>> len(processed_aggregates)
        2
        """
        singles = set()
        aggregates = set()
        processed = set()

        for sup in super_set:
            if sup > input_sub:
                r = sup - input_sub
                if r is not None:
                    if r.is_single():
                        singles.add(r)
                    else:
                        aggregates.add(r)
                    processed.add(sup)

        return singles, aggregates, processed

    def run(self):
        """The main code

        >>> s  = Context(value=0.0, cohorts=[0])
        >>> g1 = Context(value=0.0, cohorts=[0,1])
        >>> g2 = Context(value=0.0, cohorts=[0,2])
        >>> d = Disaggregator([s, g1, g2])
        >>> singles, groups = d.run()

        >>> len(singles)
        3
        >>> s1 = Context(value=0.0, cohorts=[1])
        >>> is_in(s1, singles, ignore_value=True)
        True
        >>> s2 = Context(value=0.0, cohorts=[2])
        >>> is_in(s2, singles, ignore_value=True)
        True
        >>> groups
        set([])
        """
        newly_found_singles = set()
        singles = copy.copy(self.singles)
        aggregates = copy.copy(self.aggregates)

        continue_ok = True
        while continue_ok:
            singles, aggregates, processed = self.process_singles(singles, aggregates)

            #  there is no element in singles
            while singles:
                newly_found_singles.add(singles.pop())

            # Wrong code!
            # We don't need processed contexts again
            # while processed:
            #     aggregates.add(processed.pop())

            if len(aggregates) <= 1:
                break

            # sort the aggregates, for this we need a list
            # We introduce randomness in the selection of divider of aggregated contexts
            aggregates_list = sorted(aggregates, key=lambda m: (len(m), random.random()))
            #print aggregated_contexts_to_list_of_standard(aggregates_list)
            #aggregates_list = sorted(aggregates, key=lambda m: (len(m), list(m.get_cohorts_as_set())))

            for i, c in enumerate(aggregates_list):
                super_contexts = aggregates_list[i+1:]
                split_singles,  split_aggregates, split_processed = self.split(c, super_contexts)

                # When something's processed start again
                if split_processed:
                    while split_singles:
                        s = split_singles.pop()
                        # Put into singles only when it's already known
                        if not is_in(s, singles):
                            singles.add(s)
                    while split_aggregates:
                        aggregates.add(split_aggregates.pop())
                    while split_processed:
                        aggregates.remove(split_processed.pop())

                    # We need to keep processing
                    continue_ok = True
                    break

                continue_ok = False
            # end of for
        # end of while
        return newly_found_singles, aggregates

if __name__ == "__main__":
    import doctest
    doctest.testmod()


