# Gratipay Finances

This is [Gratipay](https://gratipay.com/)'s financial accounting system, which
uses [Beancount](http://furius.ca/beancount/) and a [workflow](#workflow) here
on GitHub. While we [catch up](https://github.com/gratipay/finances/issues/3)
on our books, our budget and old data are available in our [old
spreadsheet](https://docs.google.com/spreadsheets/d/1p3DpF9ZLEsViBx0685FwJaYN1vVScKVUgXHb2zyqXZg/edit).

[![status](https://api.travis-ci.org/gratipay/finances.svg)](https://travis-ci.org/gratipay/finances)


## How Our Books are Organized

The biggest reality in our finances is that we have **operations**&mdash;*our*
money&mdash;and then we have **escrow**&mdash;*other people's* money. Never the
twain shall meet (more or less). Beyond the basic accounting principle that
assets must equal liabilities plus equity, nearly as important for Gratipay is
that escrow assets must always equal escrow liability: when people think we're
holding their money, we'd better be holding their money!

Actually, though, our operating income from processing fees comes to us from
our upstream processors commingled with escrow, *and* we want to keep our fee
*income* as close to our fee *expenses* as possible (our true operating income,
of course, comes [through Gratipay](https://gratipay.com/Gratipay/) just like
any other project on Gratipay). To deal with this dual reality, we use a **fee
buffer**. Ideally the balance in the fee buffer is zero, but in practice it
fluctuates.

You'll see, then, that the assets on our balance sheet are broken down
according to three second-level categories: `Escrow`, `Fee-Buffer`, and
`Operations`. Whereas the second-level asset categories are *logical*, our
actual *physical* bank and processor accounts end up as third-level categories.
So, for example, our actual balance at New Alliance Federal Credit Union is
equal to the sum of these three balance sheet accounts:

 - `Assets:Escrow:New Alliance`
 - `Assets:Fee-Buffer:New Alliance`
 - `Assets:Operations:New Alliance`


### Fiscal Year

Our fiscal year runs from June 1 through May 31.


## How This Repo is Organized

There is a directory for each fiscal year, named `FYNNNN` (note that fiscal
years are specified by the calendar year in which they end). Inside are two
kinds of files:

 - `NNNN-MM.beancount`, containing a single month's worth of transactions; and
 - `FYNNNN.beancount`, containing the opening and closing transactions for
   the year, and including all of the month files.

A [`gratipay.beancount`](gratipay.beancount) file ties these together, setting
options, and including the transactions from all fiscal years. That's where you
want to point Beancount's scripts.


## Working on the Finances

First, you'll need a [text editor](https://en.wikipedia.org/wiki/Text_editor),
a [command line](https://en.wikipedia.org/wiki/Command-line_interface), and
[Beancount](http://furius.ca/beancount/). Then basically what you're gonna do
is edit the file for the month you're working on, and then, from the root of
your clone of this repo, run `./test.py`. That'll check for errors (we also
have CI set up [at Travis](https://travis-ci.org/gratipay/finances)). To review
the balance sheet and income statement, run `bean-web gratipay.beancount`.


### Workflow

Each month gets [a PR](https://github.com/gratipay/finances/pulls) entitled
`account for YYYY-MM`, with a branch named `YYYY-MM`. We close the month by
merging the PR. Inside of an open month, we should overwrite transactions as
needed (changes are tracked in Git commits and GitHub comments). Outside of an
open month, we must make any correcting transactions in the current month,
rather than overwriting transactions in an old file.

Each fiscal year also gets a PR entitled `close FYNNNN` and/or `audit FYNNNN`
(we haven't done this yet so who knows? :). We close the year by merging the
PR(s). Once a year is closed, we mustn't edit it at all, apart from comments.

It's always okay to add or clarify comments.


### Style

Here are some style notes for the `*.beancount` files, based on a
[conversation](https://github.com/gratipay/inside.gratipay.com/issues/350#issuecomment-176242898)
with our accountant:

 1. Group transactions together conceptually.
 1. Transactions should be generally date-sorted, but it's okay to fudge that a
    little for the sake of (1).
 1. Record debits first.
 1. Symmetry is nice.
 1. Explicate all transaction amounts (don't depend on Beancount's [amount
    interpolation](https://docs.google.com/document/d/1wAMVrKIA2qtRGmoVDSUBJGmYZSygUaR0uOMW1GV3YE0/edit#heading=h.q5yimg2d2emu)).
 1. Use comments! Especially for weird stuff.


### Access

Many accounting tasks require access to Gratipay's bank and payment processor
statements. If you're interested in helping out with such tasks and would like
access to our statements, start with [Inside
Gratipay](http://inside.gratipay.com/big-picture/welcome).


# Help

[Open an issue](https://github.com/gratipay/finances/issues/new) if you're having problems.


# Legal

The scripts and data in this repo are released into the public domain to the
extent possible under [CC0](http://creativecommons.org/publicdomain/zero/1.0/),
and if you don't accept that then you may also use them under the
[CC](https://creativecommons.org/licenses/) or [OSI
license](https://opensource.org/licenses) of your choosing.
