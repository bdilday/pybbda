
Contributions from the community are welcome! Following are some general guidelines
on pull requests.

### issues

In many cases it helps to open an issue regarding your change 
before submitting a pull request. 

### code standards

#### tests

Any change introduced in a PR must include tests,
which can usually be accomplished with additional unit tests
under the `tests` directory.


#### documentation

New code should be documented using the 
[`reStructuredText`](https://devguide.python.org/documenting/) format.

#### style

This package does not enforce very stringent style
conventions, i.e. it does not block PRs with 
`pylint` in the CI. It does enforce formatting
with `black` and some features of `flake8`. That said,
code style should generally adhere to Python conventions, 
e.g., list comprehensions are preferred to explicit for-loops, 
use snake case for variable names, avoid short or opaque
variable names, etc.

#### type annotations

This package does not use type annotations.

### examples

It's encouraged that any new code include an 
example of use. This is done by including 
a script in the `examples` directory, which 
will get built into the docs using `sphinx-gallery`.

Adding additional examples of using the package is also 
a good way to contribute, without necessarily adding
new functionality.

### PR checklist

1. Make changes in your local repo.
2. Add unit tests.
3. Run `make lint` from the top-level directory. This 
will apply `black` formatting and highlight any 
issues that are detected by `flake8`.
4. Run `make test`
5. Run `make docs`
6. If you had previously started an issue related to
the PR, you should link them using the `Linked Issues`
option in github.

If all of these succeed, your PR is good to go!
