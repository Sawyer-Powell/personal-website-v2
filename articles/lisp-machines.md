---
title: The Magic of Lisp Machines
artist: lars muller publishers
hero: https://stylecampaign.com/blog/blogimages/plotter-publications/computer-art-publications-033.jpg
artist-page: https://www.lars-mueller-publishers.com/spirale-8-original-issue-1960
date: 2024-05-20
visible: true
tags:
  - cs
---
Recently, I've been discussing with some friends around why I like to use Emacs as my primary text editor, and it's got me thinking about what the Emacs platform offers over other, more traditional, text editors & IDEs. When you hear Emacs advocates talk about Emacs, you often hear them extolling its extensibility, its adaptability, and its capacity to be self-documenting. But, as an outsider, it's difficult to understand what these things really mean, and even harder to understand why Emacs is so powerful and dynamic. I'm not here to try and convert you to being an Emacs user, but I want to make a case for why its design and philosophy is compelling, and worth iterating on.

# Preface

Emacs, at its core, is a Lisp interpreter. The Emacs codebase has two major sections, its `src` folder, which contains the core of the application in C, and the `lisp` folder, which contains most of the application's features written in Elisp (Emacs' custom flavor of Lisp). Looking into the `src` folder, we find that most of the C code is either dedicated towards interpreting and executing Elisp code, or working with the underlying operating system to display windows, do I/O, and receive user input.

The C core of Emacs serves to provide an Elisp interpreter, as well as a graphical interface to do that interpretation. Almost all the interesting things that Emacs does are built entirely in Elisp. Emacs provides a complete interface for interacting with your computer, allowing you to, if you wanted, do all of your computing tasks entirely through Lisp. 

Making Lisp interpretation a primitive in how you do your computing is powerful, and is key to enabling the extensible, adaptable, and self-documenting nature of Emacs.

# Why Lisp is Unique

If you're already familiar with Lisp, feel free to skip this section without missing key content, but for those of you who are new to, or uncertain about Lisp, you are invited you to read on. I'm going to borrow an example from the classic [Structure and Interpretation of Computer Programs](https://web.mit.edu/6.001/6.037/sicp.pdf) (henceforth referred to as *sicp*) that directly shows the power, and uniqueness, of Lisp.

## Symbolic Differentiation in Lisp

I want to write a program that can transform simple mathematical expressions into their derivatives.

Generally, I want some function $d$ that mimics the behavior below (written in psuedo-code):

```text
d(x^2 + 2x + 1)
> 2x + 2
```

Where $d$ can accept any mathematical expression on x as an argument (in whatever mathematical syntax you like), and produce the expression representing the derivative of the input (in that same syntax). I also want an easy way to evaluate that resulting expression.

Most coders will jump to representing the input and output of $d$ as a string, opting for some ASCII friendly mathematical syntax. The traditional, C-like, approach would be to provide a function like this (the below is a theoretical API in Python):

``` python
d("x**2 + 2*x + 1")
> "2*x + 2"
```

However, taking that `2*x + 2` string output, and then using it to do real calculations, is a little tricky. If you're using Python you would need to invoke the Python interpreter, or some other interpreter, to parse and process that `2*x + 2` string for a given value of $x$. 

Actually implementing $d$ would also be very tricky, since you would need a way to parse that input expression into a data structure, do something to that data structure, and then convert that data structure back into an expression.

Here's an example API for the $d$ function in Lisp. 

*if you want details on how to actually implement this function, refer to the chapter of sicp linked [here](https://sicp.sourceacademy.org/chapters/2.3.2.html), it's well worth the read*

```lisp
(d '(+ (+ (* x x)
          (* 2 x))
       1))
> (+ (* 2 x) 2)
```

Every lisp expression (*what you see in each pair of ( )*) starts with a function call. Everything else in the expression is an argument to that function. So `(+ 2 3)` is equivalent to `2 + 3` in regular math notation. This might seem weird at first, but turns out to be a very powerful way of expressing operations, not much different than
traditional function notation, e.g. `add(2, 3)`.

Above, we call the function $d$ on the list, `'(+ (+ (* x x) (* 2 x)) 1)`. In Lisp, a pair of `'( )` preceded by a `'` is a list. It looks like Lisp syntax doesn't it? But for now that syntax is being treated as a list. And that really is a list, just like in normal programming. It's just using `( )` instead of `[ ]`. If you're still confused, replace every `( )` with `[ ]` and see if it starts to look familiar. Here's the same data structure in Python: `["+", ["+", ["*", "x", "x"], ["*", "2", "x"]], "1"]`

Since it's a list, you can index into it like a normal list. Here we
index the first element of the list.

```lisp
(nth 0 '(+ (+ (* x x) (* 2 x)) 1))
> +
```

And the second.

```lisp
(nth 1 '(+ (+ (* x x) (* 2 x)) 1))
> (+ (* x x) (* 2 x))
```

But importantly, as you've already seen, that list is also valid Lisp code! Which we can evaluate!

```lisp
(defun evaluate_second_element (x)
  (eval (nth 1 '(+ (+ (* x x) (* 2 x)) 1))))
(evaluate_second_element 2)
> 8
```

Take a moment to absorb and piece together what is happening in that code above. This is the one of the superpowers of Lisp. We are defining a function called `evaluate_second_element`, which finds the second expression in our list using the `nth` function, and then evaluates the output of `nth` using the input of `x` passed into
`evaluate_second_element`.

Let me walk through how to conceptualize what the lisp interpreter is doing.

```lisp
;; We define our function here
(defun evaluate_second_expression (x)
  (eval (nth 1 '(+ (+ (* x x) (* 2 x)) 1))))
;; When we call the function:
(evaluate_second_expression 2)
;; Lisp evaluates
(nth 1 '(+ (+ (* x x) (* 2 x)) 1)))
;; to
'(+ (* x x) (* 2 x))
;; And passes that to the 'eval' function,
(eval '(+ (* x x) (* 2 x)))
;; Eval takes that list, and evaluates it as a lisp expression
;; replacing any variables with ones it can find in its local
;; scope. Since we defined x when we called evaluate_second_expression
;; the above evaluates to:
(+ (* 2 2) (* 2 2))
;; Which of course evaluates to
8
```

How you would implement the same thing above in Python, or another C-like, procedural, language? It's hard to think of a program in an other language that can do what Lisp is doing here as elegantly or succinctly.

Key to what's happening here is that Lisp code can both be evaluated as normal code and treated as a *data structure*. Which allows us to manipulate Lisp code *as data*, and then *execute* that data after we've transformed it. You'll hear Lisp enthusiasts saying "data is code, code is data", which is an oversimplification, but is driving home the point above.

If we were to do something similar in Python, we could use the Python interpreter to evaluate strings of Python code at runtime, but we'd run into a headache when we want to do some interesting manipulation of the strings of Python code.

Coming back to our $d$ function, once we've created an expression representing the derivative of our input, we can easily evaluate that expression.

Recall that our $d$ function works like this:

```lisp
(d '(+ (+ (* x x) (* 2 x)) 1))
> (+ (* 2 x) 2)
```

Let's write another function, that allows us to pass in a Lisp math expression on `x` as the first argument, and a value for `x` as the second argument that the function will use to evaluate the derivative.

```lisp
(defun derivative_at (expression x)
  (eval (d expression)))
(derivative_at '((+ (+ (* x x) (* 2 x)) 1)) 2)
> 6
```

That's it!

## Lisp is Functional

For most functions you write in Lisp, you cannot change the data in your inputs. A key part of Lisp being *functional* is that its functions have no *side effects*. When you pass an input into your functions, you have a guarantee that your inputs are going to be the same after you call that function.

In general, this also means that Lisp functions can be run anywhere, in any context, and have a good chance that they are going to behave consistently. Just like in math, $\text{cos}(pi)$ is going to be $-1$ regardless of if you're calculating $\text{cos}(theta)$ in an integral, an exponent, or any other context.

There are cases when this does not hold true for Lisp functions, like when they rely on information read in from files, or in the state of global variables, but, these functions are usually rare and compartmentalized from the rest of an application.

This is great because it means that, if you're in a Lisp codebase, and you find a function that looks useful, you can use it without much worry. Just like in math, we can create more and more complex behavior by *composing* Lisp functions. And importantly, like in math, we have very few restrictions as to how we can compose them.

# Properties of Lisp Machines

Lisp is highly expressive, functional, and also (generally) interpreted. Let's take a moment and think about what each of these qualities enables us to do when we're writing programs, and think about how those properties then shape a Lisp based computing environment.

## Expressive

Lisp's syntax is a simple data structure, a list, which allows us to easily create parsers for custom syntax within Lisp itself. This process, where a programming language extends itself, is called a *macro*. An excellent use case for macros is in configuration files, where we need a high level way of controlling a program.

Emacs configuration files make heavy use of macros. Here's an example from my Emacs configuration where I tell Emacs to use the `gruvbox-theme` package, specifying what version of the `gruvbox` theme I want it to load once it's finished parsing the package.

```lisp
(use-package gruvbox-theme
  :config
  (load-theme 'gruvbox-dark-hard))
```

Notice that this doesn't make sense in terms of traditional function syntax. `use-package` is a macro, and allows me to define the package name as the first argument, along with a host of functions I want to run when initializing the package, and configuring the package. Following the inclusion of `:config` I can include any number of functions to run. `:config` can also be preceded by other section demarcations like `:init` or `:after`.

If you wanted a similar api in Python, you would have to manually register a series of callbacks with whatever function is loading in your package. This is why many Python projects will include a `json` or `yaml` file to manage their configuration. In Lisp, we are able to avoid separating configuration from code, and declaratively define the behavior we want when loading in our package.

Scaled up to an entire computing environment, we are able to avoid a good amount of complexity introduced by having to configure our application across a variety of domain specific languages. We can also achieve a less verbose syntax than other programming languages, like Lua when its used for configuration in Neovim.

Macros are part of why Emacs is extremely *adaptable*, the language can conform to the specific semantics we need to control our computing.

## Modular

Since Lisp is (mostly) functional, its much easier for us to reuse existing code, and compose it into new systems.

This website is built from exploiting the functional nature of Lisp. All of the content on this website is written in Emacs Org mode, a package that provides an excellent interface for taking notes, project management, interpreting code, and even creating spreadsheets. Org mode ships with a suite of functions that let me take my `.org` files and convert them into `html`. However, when I was first experimenting with org's publishing capabilities, I found myself wanting to change the aesthetics of the `html` it was producing.

I was able to achieve most of the aesthetic changes through custom `css`, but some of the changes, related more to the structure of the `html` it was producing, couldn't be fixed reasonably with stylesheets or javascript.

Since (nearly) every function in the org mode package is a pure function, I was able to take out a chunk the code that converted org syntax to `html`, rewrite it, and hook it into the publishing pipeline to achieve the custom behavior I wanted. Since the new function I wrote abided by the same interface, and it worked perfectly with the rest of the org package code!

Interfaces and pure functions make this experience possible. Doing the same in an object-oriented codebase would be much harder. Lisp's functional style also contributes to Emacs being *self-documenting*, meaning that an Emacs user is always keypress away from reading the documentation and implementation of any Elisp function or macro in thier packages or configuration.

Since every Elisp function can have an associated docstring, developers can document what their functions do as they are defining them. And since many of these functions are *pure*, documentation can stay self-contained to that function. They aren't tied to some object's state, their behavior is entirely described by the operations performed on their inputs. Describing non pure functions requires not only describing how the inputs are used to produce outputs, but also what mutations are ocurring elsewhere in the program.

When a new function is registered with Emacs, Emacs makes a record of which file that function is located in, as well as its associated docstring. This allows users to look up functions they come across by placing their cursor over a function call and invoking the `describe-function` method.

## Iterative

Programs made using interpreted languages can be modified *while they are running*. This is what allows web developers to modify websites using javascript in browser extensions, and what allows data scientists to iterate on their machine learning models in Python without having to restart, or recompile, their programs over and over again. Interpreted languages excel at giving people high level control over their computer, while also giving them room to experiment and iterate. When developing software, the most critical component to productivity is the tight feedback loop. No one can write complicated code perfectly on their first try.

Interpreted languages allow developers to quickly build incremental parts of their software, moving piece by piece once they're certain that the foundation they just built is correct. People who work with interpreted languages often work withing a `repl`, or a Read-Eval-Print-Loop, where they type a command, and immediately evaluate its result. Using the `repl` developers can write their software line by line, testing each line, or handful of lines, as they write them. This eliminates the need for a debugger, or extensive logging, that is often reqiured when programming complex software in a compiled language.

In Emacs, Elisp being interpreted means that I can develop new features for Emacs while it is running, within Emacs. Testing them live within my editor, line by line. This makes Emacs incredibly extendable, since you can build your plane as its flying. I'm not aware of any other environments which do this better than Emacs.

Since Emacs is a tool for developers, its easy extendability allows devs to quickly adapt their development environments to the type of project that they're working on. If they're working on a web application in one moment, and a graphical application in the next, they can program Emacs to understand the context of the project that they're in, and create custom keybindings for running compiliation scripts, launching servers, opening windows on certain monitors, whatever is suitable to achieve that tight feedback loop in the codebase they're working on.

This is possible with the normal way that developers do their computing, with some combination of an editor and a CLI. But that approach cannot compete with the efficiency of your editor *being* an interpreter.

# Thesis

Highly productive computing environments put few conceptual limitations on its users. These types of computing environments allow users to exercise genuine creativity, and give them tools which they can easily shape and modify. Emacs, and any future Lisp based computing environments that come next, are uniquely advantaged in providing this type of computing environment. When you're goal is to efficiently operate your computer, you want something which easily molds to your will, allows quick access to information, and allows you to create tight feedback loops.

Emacs is not the final form of this, in practice it has many issues. But I hope this has made you interested preserving and iterating on the idea of Lisp based computing environments, like Emacs. I want to see the shell evolve into a more robust environment for running, and working with, interpreted languages, as opposed to the highly limiting experience it is today.

Lisp and Emacs are well outside of the modern zeitgeist, and I hope that changes. There's so much work that can be done to improve the performance, and reliability, of Lisp. Adding more sophisticated type systems, and improving Lisp compilers, are just a few low hanging fruit. Fundamentally, interpreted languages aren't going anywhere, even the most hardcore C developers are often using Bash as a core interface for their everyday computing.

Lisp is simple, and magical, and powerful. And we haven't yet fully exploited its potential. So I hope you take some time to ponder these ideas that I've shared, and think about how we can build computing environments that are productive, exciting, and creatively fulfilling.