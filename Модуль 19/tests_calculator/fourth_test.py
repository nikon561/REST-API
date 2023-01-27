import pytest
from app.calculator import Calculator


class TestCalc:
   def setup(self):
       self.calc = Calculator

   def test_adding_calculate_correctly(self):
       assert self.calc.adding(self, 10, 2) == 12
   def test_adding_calculate_failed(self):
       assert self.calc.adding(self, 10, 2) == 6