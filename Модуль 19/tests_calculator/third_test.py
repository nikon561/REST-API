import pytest
from app.calculator import Calculator


class TestCalc:
   def setup(self):
       self.calc = Calculator

   def test_subtraction_calculate_correctly(self):
       assert self.calc.subtraction(self, 10, 2) == 8

   def test_subtraction_calculate_failed(self):
       assert self.calc.subtraction(self, 10, 2) == 6