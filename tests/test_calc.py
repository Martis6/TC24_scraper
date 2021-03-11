from calculator.calculator import Calculator
import pytest

def test_reset_memory():
    c = Calculator(6)
    assert c.reset_memory() == 0

def test_correct_addition():
    c = Calculator()
    assert c.add(6) == 6

def test_correct_subtraction():
    c = Calculator()
    assert c.subtract(6) == -6

def test_correct_multiplication():
    c = Calculator(6)
    assert c.multiply(6) == 36

def test_correct_division():
    c = Calculator(6)
    assert c.divide(6) == 1

def test_divide_by_zero_error():
    c = Calculator()
    with pytest.raises(ZeroDivisionError):
        c.divide(0)

def test_root():
    c = Calculator(8)
    assert c.root(3) == 2

def test_root_by_zero_error():
    c = Calculator(6)
    with pytest.raises(ZeroDivisionError):
        c.root(0)