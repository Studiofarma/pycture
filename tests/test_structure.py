import pytest
from pycturelib import structure as pys

@pytest.mark.parametrize('structure, traverse_result, pruned_branches, keep_branches', [
    (
        pys.Structure('x', 0, 2,
            pys.Structure('xx', 0, 1, pys.Structure('xxx', 0, 1)),
            pys.Structure('xy', 1, 1),
        ),
        [('xxx', 0, 1), ('xy', 1, 1)], [], []
    ),
    (
        pys.Structure('x', 0, 3,
            pys.Structure('xx', 0, 2, pys.Structure('xxx', 0, 1), pys.Structure('xxy', 1, 1)),
            pys.Structure('xy', 2, 1),
        ),
        [('xxx', 0, 1), ('xxy', 1, 1), ('xy', 2, 1)], [], []
    ),
    (
        pys.Structure('x', 0, 4,
            pys.Structure('xx', 0, 2, pys.Structure('xxx', 0, 1), pys.Structure('xxy', 1, 1)),
            pys.Structure('xy', 2, 1),
            pys.Structure('xz', 3, 1, pys.Structure('xzx', 3, 1)),
        ),
        [('xxx', 0, 1), ('xxy', 1, 1), ('xy', 2, 1), ('xzx', 3, 1)], [], []
    ),
    (
        pys.Structure('x', 0, 4,
            pys.Structure('xx', 0, 2, pys.Structure('xxx', 0, 1), pys.Structure('xxy', 1, 1)),
            pys.Structure('xy', 2, 1),
            pys.Structure('xz', 3, 1, pys.Structure('xzx', 3, 1)),
        ),
        [('xx', 0, 2), ('xy', 2, 1), ('xzx', 3, 1)], ['xx'], []
    ),
    (
        pys.Structure('x', 0, 4,
            pys.Structure('xx', 0, 2, pys.Structure('xxx', 0, 1), pys.Structure('xxy', 1, 1)),
            pys.Structure('xy', 2, 1),
            pys.Structure('xz', 3, 1, pys.Structure('xzx', 3, 1)),
        ),
        [('xy', 2, 1), ('xzx', 3, 1)], [], ['xy', 'xzx']
    ),
])
def test_can_traverse_a_structure(structure, traverse_result, pruned_branches, keep_branches):
    actual_traverse = structure.traverse_leaves(
        pruned_branches = pruned_branches,
        keep_branches = keep_branches,
        fn = lambda x: (x.name, x.start_at, x.length))

    assert actual_traverse == traverse_result
