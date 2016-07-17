# -*- coding: utf-8 -*-
"""Deride

A mocking package with a fluent interface

"""
from cachetools import hashkey


class ObjectKey(object):
    """
    Utility for generating a key from arguments and keyword arguments
    """

    @staticmethod
    def value(*args, **kwds):
        """
        returns the generated hashkey of the *args and **kwds
        """
        return hashkey(*args, **kwds)


class Invocation(object):
    """
    Models a single encapsulation of a function including the agurments
    used to invoke it
    """

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs


class CallAssertions(object):
    """
    A set of assertions to use against all invocations of a particular method
    """

    def __init__(self, invocations):
        self.number = len(invocations)
        self.invocations = invocations

    def __times_error__(self, msg):
        msg = '{msg}. times={calls}' \
            .format(msg=msg, calls=self.number)
        return AssertionError(msg)

    def times(self, number):
        """
        Asserts the actual number of times the invocation happened is equal
        to the actual number

        Raises an AssertionError when the actual number does not equal
        the expected number
        """
        if self.number != number:
            raise self.__times_error__('times assertion error')

    def once(self):
        """
        Facade of times(n) with n being 1
        """
        self.times(1)

    def twice(self):
        """
        Facade of times(n) with n being 2
        """
        self.times(2)

    def lt(self, number):
        """
        Asserts the actual number of times the invocation happened is less
        than the expected number

        Raises an AssertionError when the actual number is greater than
        or equal to the expected number
        """
        if self.number >= number:
            raise self.__times_error__('lt assertion error')

    def lte(self, number):
        """
        Asserts the actual number of times the invocation happened is less
        than or equal to the expected number

        Raises an AssertionError when the actual number is greater than
        to the expected number
        """
        if self.number > number:
            raise self.__times_error__('lte assertion error')

    def gt(self, number):
        """
        Asserts the actual number of times the invocation happened is greater
        than the expected number

        Raises an AssertionError when the actual number is less than
        or equal to the expected number
        """
        if self.number <= number:
            raise self.__times_error__('gt assertion error')

    def gte(self, number):
        """
        Asserts the actual number of times the invocation happened is greater
        than or equal to the expected number

        Raises an AssertionError when the actual number is less than
        the expected number
        """
        if self.number < number:
            raise self.__times_error__('gte assertion error')

    def never(self):
        """
        Facade of times(n) with n being 0
        """
        self.times(0)

    def with_arg(self, arg):
        """
        Facade of with_args(arg) supplying only a single arg which is the
        expected
        """
        self.with_args(arg)

    def with_args(self, *args):
        """
        Asserts that an invocation exists which contains the expected args in
        any order

        Raises an AssertionError if one or more of the expected args does not
        exist in the actual args of the invocations
        """
        for invocation in self.invocations:
            results = []
            for arg in args:
                found = False
                for invocation_arg in invocation.args:
                    if invocation_arg == arg:
                        found = True
                        break
                results = results + [found]
            if all(results):
                return
        raise AssertionError('invocation matching arguments not found')

    def with_args_strict(self, *args):
        """
        Asserts that an invocation exists which contains the expected args in
        order defined in the expected args

        Raises an AssertionError if one or more of the expected args does not
        exist in the actual args of the invocations or if the args exist but
        not in the expected order
        """
        for invocation in self.invocations:
            results = []
            for _ in args:
                found = False
                for index, _ in enumerate(invocation.args):
                    if len(invocation.args) == len(args) \
                            and invocation.args[index] == args[index]:
                        found = True
                        break
                results = results + [found]
            if all(results):
                return

        raise AssertionError('invocation matching arguments not found')


class CallStats(object):
    """
    Container for the assertions of the invocations of a method
    """

    def __init__(self, invocations):
        self.invocations = invocations
        self.called = CallAssertions(invocations)

    def invocation(self, n):
        return CallAssertions([self.invocations[n]])


class Expectations(object):
    """
    Container for the expectations for the call assertions
    """

    def __init__(self):
        self.data = {}
        self.assertions = {}

    def __getattr__(self, name):
        try:
            return self.assertions[name]
        except KeyError:
            return CallStats([])

    def reset(self):
        """
        Removes all existing statistics of any methods being tracked
        """
        self.assertions = {}

    def notify(self, invocation):
        """
        Updates the call stats with the next invocation.
        """
        name = invocation.name

        if name not in self.data:
            self.data[name] = []

        self.data[name] = self.data[name] + [invocation]

        self.assertions[name] = CallStats(self.data[name])


class MockActions(object):
    """
    A set of actions which can be used to Mock the behaviour of a particular
    class
    """

    def __init__(self):
        self.__action__ = self.original_func
        self.specifics = {}

    @classmethod
    def original_func(cls, original):
        """
        Setup to use the original function without any change
        """
        def override(*args, **kwargs):
            """
            Return original function
            """
            return original(*args, **kwargs)
        return override

    def to_do_this(self, func):
        """
        Setup to use the supplied function in place of the original
        """
        def to_do_func(original):
            """
            Return supplied function
            """
            del original
            return func
        self.__action__ = to_do_func

    def to_return(self, value):
        """
        Setup to invoke the original method but return the supplied value
        instead of the original return value
        """
        def return_func(original):
            """
            Return override function
            """
            def override(*args, **kwargs):
                """
                Invoke the original and return value
                """
                original(*args, **kwargs)
                return value
            return override
        self.__action__ = return_func

    def to_raise(self, throwable):
        """
        Setup to raise the supplied exception/error inplace of invoking
        the original method
        """
        def raise_func(original):
            """
            Return override function
            """
            del original

            def override(*args, **kwargs):
                """
                Raise throwable
                """
                del args, kwargs
                raise throwable
            return override
        self.__action__ = raise_func

    def to_intercept_with(self, func):
        """
        Setup to invoke the supplied function before the original is invoked
        and the original return value is returned.  The supplied function
        does not have any effect of the original invocation it simply serves
        as a way to inspect the arguments being used to invoke the original
        """
        def intercept_func(original):
            """
            Return override function
            """
            def override(*args, **kwargs):
                """
                Invoke func but return the original invocation result
                """
                func(*args, **kwargs)
                return original(*args, **kwargs)

            return override
        self.__action__ = intercept_func

    def action(self, original, *args, **kwds):
        """
        Returns the Mock Action configured for a paricular method.
        If a more specific Mock Action exists for the supplied arguments
        then it will be used.
        """
        try:
            key = ObjectKey.value(*args, **kwds)
            result = self.specifics[key].action(original, *args, **kwds)
            return result
        except KeyError:
            pass

        return self.__action__(original)

    def when(self, *args, **kwds):
        """
        Setup a set of MockActions that can be configured in the event that
        the method is invoked with the supplied set of arguments
        """
        key = ObjectKey.value(*args, **kwds)
        self.specifics[key] = MockActions()
        return self.specifics[key]


class Setup(object):
    """
    A container for the Mock Actions of a class
    """

    def __init__(self):
        self.actions = {}

    def __getattr__(self, name):
        if name not in self.actions:
            self.actions[name] = MockActions()

        return self.actions[name]

    def action_for(self, name, original, *args, **kwds):
        """
        Returns the action to be used for a particular method
        """
        return self.actions[name].action(original, *args, **kwds)


class Wrapper(object):
    """
    A wrapper for the target instance which adds on functionality for
    Deride
    """

    def __init__(self, obj):
        self.target = obj
        self.expect = Expectations()
        self.setup = Setup()

    def __getattr__(self, name):
        try:
            if not getattr(self.target, name).__call__:
                raise AttributeError('not a function')

            def call(*args, **kwds):
                """
                Method wrapper which does the magic
                """
                func = getattr(self.target, name)
                try:
                    func = self.setup.action_for(name, func, *args, **kwds)
                except KeyError:
                    pass
                self.__publish__(Invocation(name, *args, **kwds))
                return func(*args, **kwds)
            return call
        except AttributeError:
            return getattr(self.target, name)

    def __publish__(self, invocation):
        self.expect.notify(invocation)


class Deride(object):
    """
    Main class for the package Deride
    """

    @classmethod
    def wrap(cls, obj):
        """
        Wrap a target instance to setup and expect behaviour
        """
        return Wrapper(obj)
