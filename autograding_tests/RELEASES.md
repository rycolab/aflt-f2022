# Release History

The goal of this document is to provide an overview of all the changes that have been made to the library.


## Remaining
- HW3, Q3 test
- HW5, Q3 proper test

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