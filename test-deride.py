import unittest
from deride import Deride

class Person(object):

    def __init__(self, name):
        self.name = name

    def greet(self, other):
        return 'hello ' + other.name

class TestDeride(unittest.TestCase):

    def setUp(self):
        self.deride = Deride()

    def test_called_times(self):
        andy = self.deride.wrap(Person('Andy'))
        bob = self.deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))

        andy.expect.greet.called.times(1)

    def test_called_times_fails(self):
        andy = self.deride.wrap(Person('Andy'))
        bob = self.deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))

        with self.assertRaises(AssertionError):
            andy.expect.greet.called.times(2)

    def test_called_once(self):
        andy = self.deride.wrap(Person('Andy'))
        bob = self.deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))

        andy.expect.greet.called.once()

    def test_called_once_fails(self):
        andy = self.deride.wrap(Person('Andy'))
        bob = self.deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))
        self.assertEquals('hello Bob', andy.greet(bob))

        with self.assertRaises(AssertionError):
            andy.expect.greet.called.once()

if __name__ == '__main__':
    unittest.main()
