#pyderide

[![Build Status](https://travis-ci.org/guzzlerio/pyderide.svg?branch=master)](https://travis-ci.org/guzzlerio/pyderide)

Python implementation of Deride

The following list is taken from the [Deride](https://github.com/guzzlerio/deride) node.js homepage.  Some of the methods are marked with **N/A** as they are not applicable for python due to language differences.


## Information

### Contributing

Ensure you run `make` before pushing (comitting really) and also before submitting a pull request.

The `Makefile` will ensure that:

- requirements are installed
- the tests pass
- the code is linted

### CI

The following python versions are in scope for this package:

- "2.7"
- "3.3"
- "3.4"
- "3.5"
- "3.5-dev" # 3.5 development branch
- "nightly" # currently points to 3.6-dev

Currently excluding:

- "2.6" won't work with the cachetools package
- "3.2" won't work with the coverage package

## Project

### API methods

- [ ] wrap (in progress...)
- [ ] stub
- [ ] func

### Expect methods

- [x] obj.expect.method.called.times(n)
- [x] obj.expect.method.called.once()
- [x] obj.expect.method.called.twice()
- [x] obj.expect.method.called.lt()
- [x] obj.expect.method.called.lte()
- [x] obj.expect.method.called.gt()
- [x] obj.expect.method.called.gte()
- [x] obj.expect.method.called.never()
- [x] obj.expect.method.called.withArg(arg) (renamed to `with_arg`)
- [x] obj.expect.method.called.withArgs(args) (renamed to `with_args`)
- [ ] obj.expect.method.called.withMatch(pattern) 
- [x] obj.expect.method.called.matchExactly(args) (renamed to `with_args_strict`)
- [x] obj.expect.method.invocation(n)

### Reset methods

- [ ] obj.expect.method.called.reset()
- [x] obj.called.reset() (renamed to `obj.expect.reset()`)

### Setup methods

- [x] obj.setup.method.toDoThis(func) (renamed to `to_do_this`)
- [x] obj.setup.method.toReturn(value) (renamed to `to_return`)
- [ ] obj.setup.method.toResolveWith(value) **N/A**
- [ ] obj.setup.method.toRejectWith(value) **N/A**
- [x] obj.setup.method.toThrow(message) (renamed to `to_raise`)
- [ ] obj.setup.method.toEmit(event, args) **N/A**
- [ ] obj.setup.method.toCallbackWith(args) **N/A**
- [ ] obj.setup.method.toTimeWarp(milliseconds) **N/A**
- [x] obj.setup.method.toIntercept(func) (renamed to `to_intercept_with`)
- [x] obj.setup.method.when(args|function)
   - [x] .toDoThis
   - [x] .toReturn
   - [ ] .toRejectWith **N/A**
   - [ ] .toResolveWith **N/A**
   - [x] .toThrow (renamed to `to_raise`)
   - [ ] .toEmit **N/A**
   - [ ] .toCallbackWith  **N/A**
   - [ ] .toTimeWarp **N/A**
   - [x] .toIntercept(func) (renamed to `to_intercept_with`)


