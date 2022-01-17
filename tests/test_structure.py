import pytest
from pycture import structure as pys

@pytest.mark.parametrize('structure, traverse_result', [
    (
        pys.Structure('x', 0, 2,
            pys.Structure('xx', 0, 1, pys.Structure('xxx', 0, 1)),
            pys.Structure('xy', 1, 1),
        ),
        [('xxx', 0, 1), ('xy', 1, 1)]
    ),
])
def test_can_traverse_a_structure(structure, traverse_result):
    actual_traverse = structure.traverse_leafs(lambda x: (x.name, x.start_at, x.length))

    assert actual_traverse == traverse_result
