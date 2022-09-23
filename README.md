# An Improved Algorithm for Coarse-Graining Cellular Automata

This repository contains all the code from publication: Song, Y. and Grochow, J. “An Improved Algorithm for Coarse-Graining Cellular Automata” 
(https://arxiv.org/pdf/2012.12153.pdf)

The code in these files include an implementation to our algorithm for discovering coarse-grainings for elementary cellular automata. It can be run by inputting a specified supercell size or rule number, or the code can run on all supercell sizes up to 7 and all rules at once.

bruteforce.py contains an implementation for the brute force algorithm that existed prior. The latter 4 files contain code for the 4 new algorithms we developed. These algorithms are all very similar because they include the idea of visualizing coarse-grainings in a tree and pruning off branches once a successful value is found. However, they differ in the order and method in which the tree is traversed. 

We discovered that there is no single algorithm that works best for all 256 coarse-grainings. For example, if the successful coarse-graining 
is earlier in tree, we can prune off more branches and thus the forward algorithm is faster. Each coarse-graining has a preferable algorithm, 
but we could not find a pattern or predict which algorithm would be best suited for each coarse-graining. However, we ran all 4 four
algorithms on all coarse-grainings and documented the algorithms that had the fastest run-time for each.
