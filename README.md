# Pythonic Functional Constructs
**pyz**'s goal is to offer pythonic implementations of functional programming constructs found in languages such as *haskell*, *scala*, and *clojure*.

## Category Theory
* **Either**: An implementation of *scalaz*'s \\/.
* **Try**: An implementation of *scala*'s Try.

### Either
```python
add4 = lambda x: x + 4
div2 = lambda x: Right(x/2) if x != 0 else Left('boom')

# map
>>> Right(2).map(add4)
Right(6)
>>> Left('boom').map(add4)
Left('boom')

# flatmap (bind in haskell)
>>> Right(10).flatmap(div2)
Right(5)
>>> Right(0).flatmap(div2)
Left('boom')
>>> Left('pow').flatmap(div2)
Left('pow')

# do/for notation
>>> Either.do(x * y
              for x in Right(10)
              for y in div2(x))
Right(50)
>>> Either.do(x * y
              for x in Left('pow')
              for y in div2(x))
Left('pow')
```

### Try
```python
add4     = lambda x: x + 4
safe_int = lambda x: Try(int, x)
safe_bin = lambda x: Try(bin, x)

# map
>>> safe_int('5').map(add4)
Success(9)
>>> safe_int('a').map(add4)
Failure(ValueError("invalid literal for int() with base 10: 'a'",))

# flatmap (bind in haskell)
>>> safe_int('5').flatmap(safe_bin)
Success('0b101')
>>> safe_int('a').flatmap(safe_bin)
Failure(ValueError("invalid literal for int() with base 10: 'a'",))

# do/for notation
>>> Try.do(x * y
           for x in safe_int('6')
           for y in safe_int('7'))
Success(42)
>>> Try.do(x * y
           for x in safe_int('a')
           for y in safe_int('7'))
Failure(ValueError("invalid literal for int() with base 10: 'a'",))
```
