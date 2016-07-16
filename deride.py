class Invocation:

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

class CallAssertions:

    def __init__(self, invocations):
        self.number = len(invocations)
        self.invocations = invocations

    def __times_error__(self, msg):
            msg = '{msg}. times={calls}' \
                    .format(msg=msg, calls=self.number)
            return AssertionError(msg)

    def times(self, number):
        if self.number != number:
            raise self.__times_error__('times assertion error')

    def once(self):
        self.times(1)

    def twice(self):
        self.times(2)

    def lt(self, number):
        if self.number >= number:
            raise self.__times_error__('lt assertion error')

    def lte(self, number):
        if self.number > number:
            raise self.__times_error__('lte assertion error')

    def gt(self, number):
        if self.number <= number:
            raise self.__times_error__('gt assertion error')

    def gte(self, number):
        if self.number < number:
            raise self.__times_error__('gte assertion error')

    def never(self):
        self.times(0)

    #TODO: Make this more pythonic using list comprehensions and predicates
    def with_arg(self, arg):
        self.with_args(arg)

    #TODO: Make this more pythonic using list comprehensions and predicates
    def with_args(self, *args):
        for invocation in self.invocations:
            results=[]
            for arg in args:
                found=False
                for invocation_arg in invocation.args:
                    if invocation_arg == arg:
                        found=True
                        break
                results = results + [found]
            if all(results):
                return
        raise AssertionError('invocation matching arguments not found')

    #TODO: Make this more pythonic using list comprehensions and predicates
    def with_args_strict(self, *args):
        for invocation in self.invocations:
            results=[]
            for arg in args:
                found=False
                for index, item in enumerate(invocation.args):
                    if len(invocation.args) == len(args) \
                            and invocation.args[index] == args[index]:
                        found=True
                        break
                results = results + [found]
            if all(results):
                return

        raise AssertionError('invocation matching arguments not found')
        

class CallStats:

    def __init__(self, invocations):
        self.called = CallAssertions(invocations)

class Expectations:

    def __init__(self):
        self.data = {}
        self.assertions = {}

    def __getattr__(self, name):
        try:
            return self.assertions[name]
        except KeyError:
            return CallStats([])

    def reset(self):
        self.assertions = {}

    def notify(self, invocation):
        name = invocation.name

        if name not in self.data:
            self.data[name] = []

        self.data[name] = self.data[name] + [invocation]

        self.assertions[name] = CallStats(self.data[name])

class MockActions:

    def __init__(self):
        self.__action__ = None

    def to_do_this(self, func):
        self.__action__ = func

    def action(self):
        return self.__action__


class Setup:

    def __init__(self):
        self.actions = {}

    def __getattr__(self, name):
        if name not in self.actions:
            self.actions[name] = MockActions()

        return self.actions[name]

    def action_for(self, name):
        return self.actions[name].action()

class Wrapper:

    def __init__(self, obj):
        self.target = obj
        self.expect = Expectations()
        self.setup = Setup()

    def __getattr__(self, name):
        try:
            if not getattr(self.target, name).__call__:
                raise AttributeError('not a function')

            def call(*args, **kwds):
                    func = getattr(self.target, name)
                    try:
                        func = self.setup.action_for(name)
                    except KeyError:
                        pass
                    self.publish(Invocation(name, *args, **kwds))
                    return func(*args, **kwds)
            return call
        except AttributeError:
            return getattr(self.target, name)

    def publish(self, invocation):
        self.expect.notify(invocation)

class Deride:

    def wrap(self, obj):
        return Wrapper(obj)

