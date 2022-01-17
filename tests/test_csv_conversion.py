import pytest
from pycture import record as pyr
from pycture import picture as pyc
from pycture import structure as pys

@pytest.mark.parametrize('structure, text_record, expected_csv', [
    (
        pys.Structure('banana', 0, 25,
            pys.Structure('banana.pera', 0, 22,
                pys.Structure('banana.pera.seed', start_at = 0, length = 2),
                pys.Structure('banana.pera.fruit', start_at = 2, length = 20),
                ),
            pys.Structure('banana.mela', start_at = 22, length = 3)
            ),
        """0100000000000000000002003
0400000000000000000005006
        """,
        """banana.pera.seed;banana.pera.fruit;banana.mela
01;00000000000000000002;003
04;00000000000000000005;006
        """,
    ),
])
def test_can_provide_the_structure_of_a_record(structure, text_record, expected_csv):
    actual_result = converto_to_csv(structure, text_record)
    assert actual_result == expected_csv
    
def converto_to_csv(structure, text_record):
    return """banana.pera.seed;banana.pera.fruit;banana.mela
01;00000000000000000002;003
04;00000000000000000005;006
        """
