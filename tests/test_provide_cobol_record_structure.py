import pytest
from pycture import record as pyr
from pycture import picture as pyc
from pycture import structure as pys

@pytest.mark.parametrize('record, expected_result', [
    (
        pyc.Picture('pera', 2, level=1),
        pys.Structure('pera', start_at = 0, length = 2)
    ),
    (
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2)),
        pys.Structure('banana', 0, 2,
            pys.Structure('banana.pera', start_at = 0, length = 2))
    ),
    (
        pyr.Record('banana', 1,
            pyc.Picture('pera', length = 2, level = 2),
            pyc.Picture('mela', length = 3, level = 2)),
        pys.Structure('banana', 0, 5,
            pys.Structure('banana.pera', start_at = 0, length = 2),
            pys.Structure('banana.mela', start_at = 2, length = 3)
            )
    ),
    (
        pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyc.Picture('seed', length = 2, level = 3),
                pyc.Picture('fruit', length = 20, level = 3)
            ),
            pyc.Picture('mela', length = 3, level = 2)),
        pys.Structure('banana', 0, 25,
            pys.Structure('banana.pera', 0, 22,
                pys.Structure('banana.pera.seed', start_at = 0, length = 2),
                pys.Structure('banana.pera.fruit', start_at = 2, length = 20),
        ),
            pys.Structure('banana.mela', start_at = 22, length = 3)
        )
    ),
    (
        pyr.Record('banana', 1,
            pyc.Picture('mela', length = 3, level = 2),
            pyr.Record('pera', 2,
                pyc.Picture('seed', length = 2, level = 3),
                pyc.Picture('fruit', length = 20, level = 3)
            ),
        ),
        pys.Structure('banana', 0, 25,
            pys.Structure('banana.mela', start_at = 0, length = 3),
            pys.Structure('banana.pera', 3, 22,
                pys.Structure('banana.pera.seed', start_at = 3, length = 2),
                pys.Structure('banana.pera.fruit', start_at = 5, length = 20),
            ),
        )
    ),
    (
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3)),
                pyr.Record('yy', 2, pyc.Picture('yy-1', 1, 3), pyc.Picture('yy-2', 1, 3))
            ),
            pyc.Picture('zz', 2, 2)
        ),
        pys.Structure('banana', 0, 4,
            pys.Structure('banana.pera', 0, 2,
                pys.Structure('banana.pera.pera-1', start_at = 0, length = 1),
                pys.Structure('banana.pera.pera-2', start_at = 1, length = 1),
            ),
            pys.Structure('banana.zz', start_at = 2, length = 2),
        )
    ),
])
def test_can_provide_the_structure_of_a_record(record, expected_result):
    actual_result = record.structure
    assert actual_result == expected_result

