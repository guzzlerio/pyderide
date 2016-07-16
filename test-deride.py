import unittest
from deride import Deride

class Person(object):

    def __init__(self, name):
        self.name = name

    def greet(self, other):
        return 'hello ' + other.name

class TestDeride(unittest.TestCase):

    def test_called_times(self):
        deride = Deride()

        andy = deride.wrap(Person('Andy'))
        bob = deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))

        andy.expect.greet.called.times(1)

    def test_called_times_fails(self):
        deride = Deride()

        andy = deride.wrap(Person('Andy'))
        bob = deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))

        with self.assertRaises(AssertionError):
            andy.expect.greet.called.times(2)



if __name__ == '__main__':
    unittest.main()
