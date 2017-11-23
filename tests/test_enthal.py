import pytest

def test_aparray:
    """Tests atomic position array building from a sequence list.
    """
    from jonesium.enthal import aparray
    a = aparray()
    load = array([[ 0.        ,  0.        ,  0.        ],
                  [ 0.5       ,  0.28867513,  0.81649658],
                  [ 0.        ,  0.71132487,  1.63299316],
                  [ 0.        ,  0.        ,  2.44948974],
                  [ 0.        ,  0.71132487,  3.26598632],
                  [ 0.5       ,  0.28867513,  4.0824829 ]])

    assert load == a('abcacb')

def test_enthalpy:
    """Tests Helmhotlz enthalpy calculation
    """
    from jonesium.enthal import enthalpy
    e = enthalpy()
    hfcc = -7.6995450424130594

    assert hfcc == e('abc')
    
def hdif:
    """Tests the Helmhotlz enthalpy difference calculation
    """
    from joensium.enthal import hdif
    hd = hdif(['abc', 'ab'])

    assert np.allclose(hd,[[0.0],[-0.0076297548072279398]])
