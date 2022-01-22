import pytest
from pycture import record as pyr
from pycture import picture as pyc

@pytest.mark.parametrize('record, expected_result', [
    (
        '01 banana. 02 pera pic 9(2).',
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera pic 9(2).

        """,
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera pic 9(2)
                usage binary
        """,
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera 
                pic 9(2).

        """,
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera
                pic
                9(2).
        """,
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """01 banana.
                02 pera.
                    03 seed pic 9(2).
                    03 fruit pic x(20).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            ),
            pyc.Picture('mela', 3, level = 2))
    ),
    ('77 banana pic 9', pyc.Picture('banana', 1)),
    (' 01 pera   pic    9(03)v9(2)   ', pyc.Picture('pera', 5, 1)),    
    (
        """01 banana.
                02 pera.
                    03 fruit.
                        05 juice pic xx.
                        05 taste pic z(6).
                    03 seed pic 9(2).
                02 mela.
                    03 seed pic 9(2).
                    03 fruit pic x(20).
        """,
        pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyr.Record('fruit', 3,
                    pyc.Picture('juice', 2, level = 5),
                    pyc.Picture('taste', 6, level = 5)
                ),
                pyc.Picture('seed', 2, level = 3),
            ),
            pyr.Record('mela', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            ))
    ),
    (
        """01 banana. | comments
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """01 banana. | comments
                | another comment
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """01 banana.   | comments 02 arancia pic 9(2).
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """
       01  rec-sdati.
      *    any comment
           05  sdati-cod-farm     pic 9(06).
        """,
        pyr.Record('rec-sdati', 1,
            pyc.Picture('sdati-cod-farm', 6, level = 5))
    ),
    (
        """
       01  rec-sdati.
debug *    sdati-numero-riga       pic 9(08).
           05  sdati-cod-farm     pic 9(06).
        """,
        pyr.Record('rec-sdati', 1,
            pyc.Picture('sdati-cod-farm', 6, level = 5))
    ),
    (
        """
       01  rec-sdati.
180717     05  sdati-numero-riga  pic 9(08).
           05  sdati-cod-farm     pic 9(06).
        """,
        pyr.Record('rec-sdati', 1,
            pyc.Picture('sdati-numero-riga', 8, level = 5),
            pyc.Picture('sdati-cod-farm', 6, level = 5))
    ),
    ("""
       01  rec-sdati.
debug      05  sdati-numero-riga  pic 9(08).
           05  sdati-cod-farm     pic 9(06).
        """,
        pyr.Record('rec-sdati', 1,
            pyc.Picture('sdati-numero-riga', 8, level = 5),
            pyc.Picture('sdati-cod-farm', 6, level = 5))
    ),
    (
        """
       fd  seddati
           value of file-id is label-sdati
           record contains 2048 characters
      *    Se varia lunghezza rec-sdati (2048) modificare linkage sprc0200
      *    e dimensione di lks-sdati in sedp0020
           data record is rec-sdati.
       01  rec-sdati.
      *    sdati-numero-riga       pic 9(08).
           05  sdati-cod-farm     pic 9(06).
        """,
        pyr.Record('rec-sdati', 1,
            pyc.Picture('sdati-cod-farm', 6, level = 5))
    ),
    (
        """
      *-----------------------------------------------------------------*
      *    bla blabla bla                                               *
      *-----------------------------------------------------------------*
      *    ssssss kajaskjh dlòkjasDLAKJS DòAKJDAòKLDJ ASLDKJ AS         *
      *    SDADASADS ASDADa. lkòlkad jalkj àaòsj lkjdaoroiqqpoas        *
      *-----------------------------------------------------------------*
       01  xx.
           05 xx-key                           pic  9(18).
           05 xx-cod                           pic  x(06).
        """,
        pyr.Record('xx', 1,
            pyc.Picture('xx-key', 18, level = 5),
            pyc.Picture('xx-cod', 6, level = 5)
        )
    )
])
def test_can_read_a_cobol_record(record, expected_result):
    actual_result = pyr.read_record(record)
    assert actual_result == expected_result

@pytest.mark.parametrize('record, expected_result', [
    (
        """01 banana.
                02 pera pic 9(2).
                02 pera-red redefines pera pic x(2).
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyc.Picture('pera', 2, 2),
                pyc.Picture('pera-red', 2, 2)))
    ),
    (
        """01 banana.
                02 pera pic 9(2).
                02 xx redefines pera.
                    03 xx-1 pic x.
                    03 xx-2 pic 9.
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyc.Picture('pera', 2, 2),
                pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3))))
    ),
    (
        """01 banana.
                02 pera.
                    03 pera-1 pic 9.
                    03 pera-2 pic x.
                02 xx redefines pera.
                    03 xx-1 pic x.
                    03 xx-2 pic 9.
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3))))
    ),
    (
        """01 banana.
                02 pera.
                    03 pera-1 pic 9.
                    03 pera-2 pic x.
                02 xx redefines pera.
                    03 xx-1 pic x.
                    03 xx-2 pic 9.
                02 yy pic 99.
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3))),
            pyc.Picture('yy', 2, 2)
        )
    ),
    (
        """01 banana.
                02 pera.
                    03 pera-1 pic 9.
                    03 pera-2 pic x.
                02 xx redefines pera.
                    03 xx-1 pic x.
                    03 xx-2 pic 9.
                02 yy redefines pera.
                    03 yy-1 pic x.
                    03 yy-2 pic x.
                02 zz pic 99.
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3)),
                pyr.Record('yy', 2, pyc.Picture('yy-1', 1, 3), pyc.Picture('yy-2', 1, 3))
            ),
            pyc.Picture('zz', 2, 2)
        ),
    ),
    (
        """01 banana.
                02 pera.
                    03 pera-1 pic 9.
                    03 pera-2 pic x.
                02 xx redefines pera pic 99.
                02 yy redefines pera.
                    03 yy-1 pic x.
                    03 yy-2 pic x.
                02 zz pic 99.
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyc.Picture('xx', 2, level = 2),
                pyr.Record('yy', 2, pyc.Picture('yy-1', 1, 3), pyc.Picture('yy-2', 1, 3))
            ),
            pyc.Picture('zz', 2, 2)
        )
    ),
    (
        """01 banana.
                02 pera.
                    03 pera-1 pic 9.
                    03 pera-2 pic x.
                02 redefines pera pic 99.
        """,
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyc.Picture('*r', 2, level = 2)
            )
        )
    ),
])
def test_can_read_a_cobol_record_with_redefines(record, expected_result):
    actual_result = pyr.read_record(record)
    assert actual_result == expected_result

@pytest.mark.parametrize('record, expected_result', [
    (pyr.Record('banana', 1, pyc.Picture('pera', 2, 2)), 2),
    (pyr.Record('banana', 1,
        pyc.Picture('pera', 2, 2),
        pyc.Picture('mela', 3, 2)), 5),
    (pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyr.Record('fruit', 3,
                    pyc.Picture('juice', 2, level = 5),
                    pyc.Picture('taste', 6, level = 5)
                ),
                pyc.Picture('seed', 2, level = 3),
            ),
            pyr.Record('mela', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            )
        ), 32
     ),
    (
        pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyc.Picture('xx', 2, level = 2),
                pyr.Record('yy', 2, pyc.Picture('yy-1', 1, 3), pyc.Picture('yy-2', 1, 3))
            ),
            pyc.Picture('zz', 2, 2)
        ), 4
     )
])
def test_return_the_size_of_the_record(record, expected_result):
    actual_result = record.size
    assert actual_result == expected_result

def test_can_select_the_correct_redefines():
    record = pyr.Record('banana', 1,
            pyr.Redefines(
                pyr.Record('pera', 2, pyc.Picture('pera-1', 1, 3), pyc.Picture('pera-2', 1, 3)),
                pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3)),
                pyr.Record('yy', 2, pyc.Picture('yy-1', 1, 3), pyc.Picture('yy-2', 1, 3))
            ),
            pyc.Picture('zz', 2, 2)
        )
    expected_record = pyr.Record('banana', 1,
            pyr.Record('xx', 2, pyc.Picture('xx-1', 1, 3), pyc.Picture('xx-2', 1, 3)),
            pyc.Picture('zz', 2, 2)
        )

    actual_record = record.redefines(['xx'])

    assert actual_record == expected_record
