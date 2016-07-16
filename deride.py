class Invocation:

    def __init__(self, name):
        self.name = name

class CallAssertions:

    def __init__(self, number):
        self.number = number

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
        

class CallStats:

    def __init__(self, count):
        self.called = CallAssertions(count)

class Expectations:

    def __init__(self):
        self.data = {}
        self.assertions = {}

    def __getattr__(self, name):
        try:
            return self.assertions[name]
        except KeyError:
            return CallStats(0)

    def reset(self):
        self.assertions = {}

    def notify(self, invocation):
        name = invocation.name
        if name not in self.data:
            self.data[name] = 0

        self.data[name] = self.data[name] + 1
        self.assertions[name] = CallStats(self.data[name])

class Wrapper:

    def __init__(self, obj):
        self.target = obj
        self.expect = Expectations()
        self.subscriptions = [self.expect]

    def __getattr__(self, name):
        try:
            if not getattr(self.target, name).__call__:
                raise AttributeError('not a function')
            def call(*args, **kwds):
                    func = getattr(self.target, name)
                    self.publish(Invocation(name))
                    return func(*args, **kwds)
            return call
        except AttributeError:
            return getattr(self.target, name)

    def publish(self, invocation):
        for subscription in self.subscriptions:
            subscription.notify(invocation)

class Deride:

    def wrap(self, obj):
        return Wrapper(obj)

