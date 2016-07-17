import unittest
from pyderide.deride import Deride, ObjectKey


class Logger:

    @staticmethod
    def log(msg):
        Logger.messages.append(msg)

    @staticmethod
    def has_message(msg):
        return msg in Logger.messages

    @staticmethod
    def clear():
        Logger.messages = []

Logger.messages = []


class Person(object):

    def __init__(self, name):
        self.name = name

    def greet(self, other):
        return 'hello ' + other.name

    def pay(self, other, amount):
        other.credit_with(amount)

    def credit_with(self, amount):
        pass


class TestObjectKey(unittest.TestCase):

    def test_returns_key(self):
        key1 = ObjectKey.value(1, 2, 3, a=4)
        key2 = ObjectKey.value(2, 3, 4, a=5)
        self.assertNotEquals(key1, key2)


class TestDeride(unittest.TestCase):

    def setUp(self):
        self.deride = Deride()
        Logger.clear()

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

    def test_called_twice(self):
        andy = self.deride.wrap(Person('Andy'))
        bob = self.deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))
        self.assertEquals('hello Bob', andy.greet(bob))

        andy.expect.greet.called.twice()

    def test_called_twice_fails(self):
        andy = self.deride.wrap(Person('Andy'))
        bob = self.deride.wrap(Person('Bob'))

        self.assertEquals('hello Bob', andy.greet(bob))

        with self.assertRaises(AssertionError):
            andy.expect.greet.called.twice()

    def test_called_range(self):
        bob = self.deride.wrap(Person('Bob'))
        alice = Person('Alice')
        bob.greet(alice)
        bob.greet(alice)
        bob.greet(alice)

        bob.expect.greet.called.lt(4)
        bob.expect.greet.called.lte(3)
        bob.expect.greet.called.gt(2)
        bob.expect.greet.called.gte(3)

    def test_called_range_fails(self):
        bob = self.deride.wrap(Person('Bob'))
        alice = Person('Alice')
        bob.greet(alice)
        bob.greet(alice)
        bob.greet(alice)

        with self.assertRaises(AssertionError):
            bob.expect.greet.called.lt(3)
        with self.assertRaises(AssertionError):
            bob.expect.greet.called.lte(2)
        with self.assertRaises(AssertionError):
            bob.expect.greet.called.gt(3)
        with self.assertRaises(AssertionError):
            bob.expect.greet.called.gte(4)

    def test_called_never(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)
        bob.expect.greet.called.never()

    def test_called_never_fails(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)
        bob.greet(Person('alice'))
        with self.assertRaises(AssertionError):
            bob.expect.greet.called.never()

    def test_reset_call_counts(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)
        alice = Person('alice')
        bob.greet(alice)

        bob.expect.greet.called.once()

        bob.expect.reset()

        bob.expect.greet.called.never()

    def test_with_arg(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)

        alice = Person('alice')
        bob.greet(alice)
        bob.greet(bob)

        bob.expect.greet.called.with_arg(bob)

    def test_with_arg_fails(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)

        alice = Person('alice')
        bob.greet(alice)
        bob.greet(bob)

        with self.assertRaises(AssertionError):
            bob.expect.greet.called.with_arg(Person('jeremy'))

    def test_with_args(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)

        alice = Person('alice')
        bob.pay(alice, 25.00)

        bob.expect.pay.called.with_args(25.00, alice)

    def test_with_args_fails(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)

        alice = Person('alice')
        bob.pay(alice, 25.00)

        with self.assertRaises(AssertionError):
            bob.expect.pay.called.with_args(35.00, alice)

    def test_with_args_strict(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)

        alice = Person('alice')
        bob.pay(alice, 25.00)

        bob.expect.pay.called.with_args_strict(alice, 25.00)

    def test_with_args_strict_fails(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)

        alice = Person('alice')
        bob.pay(alice, 25.00)

        with self.assertRaises(AssertionError):
            bob.expect.pay.called.with_args_strict(25.00, alice)

    def test_to_do_this(self):
        bob = Person('bob')
        bob = self.deride.wrap(bob)
        alice = Person('alice')

        def shout(other):
            return 'yo ' + other.name

        bob.setup.greet.to_do_this(shout)

        result = bob.greet(alice)
        self.assertEquals(result, 'yo alice')

    def test_to_return(self):
        bob = Person('bob')
        alice = Person('alice')
        bob = self.deride.wrap(bob)
        bob.setup.greet.to_return('foobar')
        result = bob.greet(alice)
        self.assertEquals(result, 'foobar')

    def test_to_raise(self):
        bob = Person('bob')
        alice = Person('alice')
        bob = self.deride.wrap(bob)
        bob.setup.greet.to_raise(Exception('something went wrong'))

        with self.assertRaises(Exception):
            bob.greet(alice)

    def test_to_intercept_with(self):
        bob = Person('bob')
        alice = Person('alice')
        bob = self.deride.wrap(bob)

        def intercept(*args, **kwargs):
            del args, kwargs
            Logger.log('something')

        bob.setup.greet.to_intercept_with(intercept)
        result = bob.greet(alice)

        self.assertEquals(result, 'hello alice')
        self.assertTrue(Logger.has_message('something'))

    def test_specific_to_return(self):
        bob = Person('bob')
        alice = Person('alice')
        carol = Person('carol')

        bob = self.deride.wrap(bob)
        bob.setup.greet.when(carol).to_return('yo yo yo')

        self.assertEquals(bob.greet(alice), 'hello alice')

        self.assertEquals(bob.greet(carol), 'yo yo yo')

    def test_specific_to_do_this(self):
        bob = Person('bob')
        alice = Person('alice')
        bob = self.deride.wrap(bob)

        def one_yo(other):
            return 'yo {name}'.format(name=other.name)

        def two_yo(other):
            return 'yo yo {name}'.format(name=other.name)

        bob.setup.greet.when(alice).to_do_this(two_yo)

        bob.setup.greet.to_do_this(one_yo)

        self.assertEquals(bob.greet(alice), 'yo yo alice')
        self.assertEquals(bob.greet(bob), 'yo bob')

    def test_specific_to_raise(self):
        bob = Person('bob')
        alice = Person('alice')
        bob = self.deride.wrap(bob)

        bob.setup.greet.when(alice).to_raise(Exception('something went wrong'))

        with self.assertRaises(Exception):
            bob.greet(alice)

        self.assertEquals(bob.greet(bob), 'hello bob')

    def test_specific_to_intercept_with(self):
        bob = Person('bob')
        alice = Person('alice')
        bob = self.deride.wrap(bob)

        def intercept_for_bob(*args, **kwargs):
            del args, kwargs
            Logger.log('bob')

        def intercept_for_alice(*args, **kwargs):
            del args, kwargs
            Logger.log('alice')

        bob.setup.greet.to_intercept_with(intercept_for_bob)
        bob.setup.greet.when(alice).to_intercept_with(intercept_for_alice)

        self.assertEquals(bob.greet(alice), 'hello alice')
        self.assertEquals(bob.greet(bob), 'hello bob')
        self.assertTrue(Logger.has_message('alice'))
        self.assertTrue(Logger.has_message('bob'))
        self.assertEqual(len(Logger.messages), 2)

    def test_invocations_access(self):
        bob = Person('bob')
        alice = Person('alice')
        jack = Person('jack')

        bob = self.deride.wrap(bob)
        bob.greet(jack)
        bob.greet(alice)
        bob.greet(bob)
        bob.expect.greet.invocation(0).with_arg(jack)
        bob.expect.greet.invocation(1).with_arg(alice)
        bob.expect.greet.invocation(2).with_arg(bob)

if __name__ == '__main__':
    unittest.main()
