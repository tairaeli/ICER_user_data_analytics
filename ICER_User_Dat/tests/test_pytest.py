"""This file contains some basic tests. Modify to test your code"""

def test_imports():
    """Really Simple test to ensure all package dependancies are installed properly"""

    # Change list do reflect your package dependancies
    import pytest
    import math
    
    import mypackage

def test_function():
    """Test for the example function."""
    from mypackage import example as ex
    assert(ex.somefunction(1) == 1)
    assert(ex.somefunction(0) == 1)
    assert(ex.somefunction(2) == 4)

def test_exception():
    """Test to make sure function correctly returns an exception"""
    from mypackage import example as ex
    import pytest
    with pytest.raises(Exception):
        ex.somefunction("Hello world")

