# Release History

The goal of this document is to provide an overview of all the changes that have been made to the library.


## Future update
- HW5, Q3 (minimization) proper test. Blocked by the lack of "minimizable" fsas generator.
- Johnson test bug
- Add Johnson test with negative weigths. Blocked by above bug.

## 19/05
- `_push()` now allows to push any weights. Solves [this issue](https://github.com/rycolab/aflt-f2022/issues/10)
- Fixed non determinizable fsas in equivalence test, solves division by zero issue
- Fixed pushed fsas with no initial states
- Fixed kleene closure example test
- Fixed issue with kleene closure test generation
- Test only epsilon free fsas




## 11/05
- Minimization test fixed. The fsa was not trimmed.
- Added more minimization tests
- Added more kosajaru tests
- Improved kosajaru gold test with way more diverse fsas. Comparation updated to check for correct topologial orders.
- Updated top composition example test check
- HW3, Q3 (composition) gold test.
- Generated more diverse golden fsas: num_states = [3,8], acyclic or not, deterministic or not, trimmed or not
- fsa to code helper method: useful for debugging, prints the code that generates a given fsa. Located at `rayuela.base.misc`

## 06/05
- Added top composition test
- Improved equivalence test to reduce testing time and avoid infinite loops.
- Added revese string test.

## 03/05 

- Fixed kleene closure bug in gold fsas
- HW2, Q3. Coaccessible intersection test added.
- HW5, Q2: Bellmanford test fixed. Q4 tests added.
- HW3, Q4: Kosaraju test fixed to allow non-unique topological sorts
- Improved fsa comparison thanks to @Bernhard

### Necessary manual changes
- Type hints of bellmanford methods in `pathsum.py`. Fixes runtime error.

## 27/04

- Tests of hw4 and hw5
- Small bug fixes
- Added type hints

### Necessary manual changes
- thanks to william.andersson , we realized we were calling the trim method you have to code to compare the fsas, so if you had not coded this method before, several tests would fail. We updated the viterbi bwd method removing the trim call.
- Thanks to martin.kucera , we have updated a small issue with the fsa implementation
- thanks to diana.steffen , we have fixed a potential circular import when importing Pathsum in scc.py.
- We added type hints to bellman ford and johnson methods
- Changed method name: "topologically_equivalent" to "equivalent".