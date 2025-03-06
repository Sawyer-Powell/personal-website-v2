---
title: "Monads: Explained Simply"
artist: alariko
hero: https://cdna.artstation.com/p/assets/images/images/051/609/672/large/alariko-1649012335676-ilustracion-sin-titulo-01-01.jpg?1657724675
artist-page: https://www.artstation.com/alariko
date: 2024-10-27
visible: true
tags:
  - cs
---
# The Problem

Let's say we have a function in a Python program that calculates the reciprocal of a number, adjusted by a random offset between 0 and 1.

``` python
import random
def recip(x):
  return 1/(x - random.random())
```

This is a very arbitrary function, but the key idea here is that randomly, without us predicting when, this function can fail. This is analogous to reading/writing to a file or database, two operations which can routinely fail unexpectedly. When `x - random.random()` is equal to zero, Python will throw a `ZeroDivisionError`.

Let's say in our program there are instances where we chain together calls to `recip` like below.

``` python
x = 10
output = recip(x)
output = recip(output)
output = recip(output)
output = recip(output)
```

Somewhere in that codeblock, one of those `recip` calls could fail. The simplest way of handling this is just to wrap the entire block in a `try/except` clause.

``` python
x = 10
try:
  output = recip(x)
  output = recip(output)
  output = recip(output)
  output = recip(output)
except ZeroDivisionError:
  print("Tried to divide by zero")
```

This comes with a cost, every time we work with `recip` we have to be thinking about handling the `ZeroDivisionError` exception. Working with `recip` requires mental overhead. So, it would be nice if we could wrap the `recip` function in some way such that we wouldn't have to remember to handle that exception every time we call it.

The key idea here is to wrap the `recip` function in way that it returns one of two values:
1. A **success** value containing the successful calculation of `recip`
2. A **fail** value indicating that `recip` failed.

Here's one way to wrap it:

``` python
class SuccessOrFail:
  def succeed(self, success_val):
    self.success_val = success_val
    self.failed = False
    return self
  def fail(self):
    self.success_val = None
    self.failed = True
    return self
def wrap(func):
  def call_func_safely(x)
    try:
      return SuccessOrFail().succeed(func(x))
    except ZeroDivisionError:
      return SuccessOrFail().fail()
  return call_func_safely
```

Using this wrapper we can now create a "safe" version of our `recip` function. Let's call it `safe_recip`. But, we have a new problem. It's difficult to chain together calls to `safe_recip` without needing to add new control flow.

``` python
safe_recip = wrap(recip)
x = 10
output = safe_recip(x)

# !! This could cause unhandled behavior, passing a None into recip
output = safe_recip(output.success_val)
```

To fix this, let's rewrite our `wrap` function to allow us pass a `SuccessOrFail` object as the argument, instead of the plain number `x`.

``` python
def wrap(func):
  def call_func_safely(success_or_fail)
    if (success_or_fail.failed):
      return SuccessOrFail().fail()
    try:
      return SuccessOrFail().succeed(self.func(success_or_fail.success_val))
    except ZeroDivisionError:
      return SuccessOrFail().fail()
  return call_func_safely
```

Now, we can seamlessly chain together calls to `safe_recip` without having to worry at all about handling the failure up front!

``` python
safe_recip = wrap(recip)
x = SuccessOrFail().succeed(10)
output = safe_recip(x)
output = safe_recip(output)
output = safe_recip(output)
output = safe_recip(output)
output = safe_recip(output)
if (!output.failed):
  print("Final output is " + str(output.success_val))
else:
  print("Tried to divide by zero")
```

Notice the benefit of this approach over an explicit exception handling. Wrapping the `recip` function in this safety net allows us to write our code in a way where we only have to think about failure **when we actually need to**. We're not forced into a position where we have to program defensively.

The exception handling approach adds mental overhead, and it adds control flow. With this approach we can create pipelines of operations and only deal with errors when it makes sense to. It makes our code much easier to reason about, especially in more complicated situations.
# Framing Our Problem as a Monad

The first step to thinking **monadically** is to understand that functions put our program into a set of possible **states** once they are run. In the case of the `recip` function, when it runs it puts our programs into one of two possible states:

1. One where it succeeded and it yielded a value to its caller
2. One where the function failed and threw an exception

The first step to creating a monad is to encapsulate these possible states into the value produced by the function. In our solution we created a new type called `SuccessOrFail`, and wrapped our `recip` function such that it accepts and returns `SuccessOrFail`. Since `recip` itself only accepts a `number` as input, when we wrap it we handle the case of `SuccessOrFail` being in the fail state. When `SuccessOrFail` is marked as failed, we simply propagate that state in the return value of `safe_recip`.

So, to summarize we:

1. Wrap the number that would have originally been the input to `recip` into a type that fully captures the states `recip` can yield.
2. Create a new function which wraps `recip` such that it is compatible with taking that new type as input, and producing it as output.

This type that we create is called the **monadic type**. The `SuccessOrFail.succeeded(x)` function allows us to wrap numbers inside that type. The `wrap` function makes functions which take numbers as inputs and outputs compatible with our monadic type. This `wrap` function is known as the **combinator**, also called the **bind** function.

So, what specifically is the monad? The monad can be thought of as the pattern of encapsulating state in a type, providing a way to take values and embed them in that type, and then a way to make functions that operate on those values compatible with that new type. The pattern **is** the monad.

To create a monad you:
- Create a new type
- Create a function to embed values in that type
- Create a function which makes other functions compatible with that type

# Popular Uses of Monads

Monads are excellent choices for handling functions which fail. Another popular monad is known as the `Maybe` monad, which helps deal with values being possibly null.

An interesting use case of monads is in logging. Notice that in our `wrap` function we can add arbitrary code, which includes logging. In this sense we are "decorating" whatever functions we pass through `wrap` with extra code.

A simple decoration we can do is to `print` the output of our function every time it runs. This might be helpful for debugging.
``` python
def wrap(func):
  def call_func_safely(success_or_fail)
    if (success_or_fail.failed):
      return SuccessOrFail().fail()
    try:
      success_val = self.func(success_or_fail.success_val)
      print("Succeeded on input " + str(success_or_fail.success_val) + " yielding " + str(success_val))
      return SuccessOrFail().succeed(success_val)
    except ZeroDivisionError:
      print("Failed. Division by zero.")
      return SuccessOrFail().fail()
  return call_func_safely
```

Even more interesting is we can build up a log **inside** the monadic type and then read it any time we want to.

``` python
class SuccessOrFail:
  def succeed(self, success_val, log=None):
    self.success_val = success_val
    self.failed = False
    self.log = log
    return self
  def fail(self, log=None):
    self.success_val = None
    self.failed = True
    self.log = log
    return self
def wrap(func):
  def call_func_safely(success_or_fail)
    if (success_or_fail.failed):
      return SuccessOrFail().fail()
    try:
      success_val = self.func(success_or_fail.success_val)
      return SuccessOrFail().succeed(success_val, success_or_fail.log + "nSucceeded on input " + str(success_or_fail.success_val) + " yielding " + str(success_val))
    except ZeroDivisionError:
      print("Failed. Division by zero.")
      return SuccessOrFail().fail(success_or_fail.log + "nFailed. Divide by zero")
  return call_func_safely
```

This shows one of the amazing "hidden" features of monads, that you can build up state across chained operations. And can do this without introducing bloat to other parts of the program.

``` python
safe_recip = wrap(recip)
x = SuccessOrFail().succeed(10)
output = safe_recip(x)
output = safe_recip(output)
output = safe_recip(output)
output = safe_recip(output)
output = safe_recip(output)
print(output.log)
```
``` text
Succeeded on input 10 yielding 0.10644867208448258
Succeeded on input 0.10644867208448258 yielding -0.3266419394727856
...
```

Some of the most notable uses of monads outside of functional languages like Haskell are in Typescript and Rust with their `?` operator. In Typescript, the `?` operator is used to shortcircuit chained function calls, or property accesses, to a null/undefined value.

``` typescript
let first_users_name = response.data?.users?.[0]?.name;
```

Here we try to get the name of the first user in the response. We set the `first_users_name` variable to null if any of those property accesses yields us a null (or undefined) value. A fun exercise is to reason about why the `?` can be considered a **combinator** or **bind** function.
