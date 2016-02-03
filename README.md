# Gratipay Finances

This is [Gratipay](https://gratipay.com/)'s financial accounting system, which
is comprised of some wrapper scripts for [Ledger](http://ledger-cli.org/) and a
[workflow](#workflow) here on GitHub. While we [catch
up](https://github.com/gratipay/finances/issues/3) on our books, our budget and
old data are available in our
[old spreadsheet](https://docs.google.com/spreadsheet/pub?key=0AiDJ5uiG6Hp3dDJnVDNLMVk4NldhSy1JbFJ0aWRUYkE&output=html&widget=true).

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
any other Gratipay Team). To deal with this dual reality, we use a **fee
buffer**. Ideally the balance in the fee buffer is zero, though of course it
fluctuates in practice.

You'll see, then, that the assets on our balance sheet are broken down
according to these three second-level categories: escrow, fee buffer, and
operations. Each also gets a separate income statement:

 - Net income on the income statement hits Current Activity on the balance sheet
 - Escrow activity hits the Escrow liability account
 - Fee Buffer activity hits the Fee Buffer liability account

Whereas the second-level asset categories are *logical*, our actual *physical*
bank and processor accounts end up as third-level categories. So, for example,
our actual balance at New Alliance Federal Credit Union is equal to the sum of
these three balance sheet accounts:

 - Assets:Escrow:New Alliance
 - Assets:Fee Buffer:New Alliance
 - Assets:Operations:New Alliance


## How This Repo is Organized

There is a directory for each fiscal year, named `FYNNNN`. Inside are three
kinds of files:

 - `FYNNNN.dat`&mdash;the opening and closing transactions for the year
 - `NNNN-MM.dat`&mdash;a month's worth of transactions
 - `declarations.dat`&mdash;the list of accounts in use during the year

Our scripts and helpers are in the `bin/` directory.


## Working on the Finances

First, you'll need [Ledger](http://ledger-cli.org/) (v3),
[Python](https://www.python.org/) (v2.7), a [text
editor](https://en.wikipedia.org/wiki/Text_editor), and a [command
line](https://en.wikipedia.org/wiki/Command-line_interface). Then basically
what you're gonna do is edit the `dat` file for the month you're working on,
and then, from the root of your clone of this repo, run (with
[`bin`](https://github.com/gratipay/finances/blob/master/bin/) on your `PATH`):

```bash
test.py && clear && balance-sheet.py && income-statement.py
```

That'll check for errors (we also have CI set up [at
Travis](https://travis-ci.org/gratipay/finances)) and then show you a balance
sheet and income statement. If you need to add accounts or currencies you can
do so in the `declarations.dat` file for the year you're working on. If you
want to run arbitrary Ledger
[commands](http://ledger-cli.org/3.0/doc/ledger3.html), we provide a wrapper
that points `ledger` to our `dat` files for your convenience:

```bash
wledger.py register
```


### Workflow

Each month gets [a PR](https://github.com/gratipay/finances/pulls) entitled
`reconcile YYYY-MM`, with a branch named `YYYY-MM`. We close the month by
merging the PR for the month. Inside of an open month, we should overwrite
ledger transactions as needed (changes are tracked in Git commits and GitHub
comments). Outside of an open month, we must make any correcting transactions
in the current month, rather than overwriting transactions in an old dat file.

Each fiscal year also gets a PR entitled `close FYNNNN` and/or `audit FYNNNN`.
We close the year by merging the PR(s). Inside of an open year, we may change
account names (this affects all month files for the year). Once a year is
closed, we mustn't edit it at all, apart from comments.

It's always okay to add comments.


### Style

Here are some style notes for the `dat` files:

 1. Group transactions together conceptually.

 1. Transactions should be generally date-sorted, but it's okay to fudge that a
    little for the sake of (1).

 1. Record debits first.

 1. Symmetry is nice.

 1. Explicate all transaction amounts (don't depend on Ledger's implicit
    transaction balancing).

 1. Use comments! Especially for weird stuff.


### Access

Many accounting tasks require access to Gratipay's bank and payment processor
statements. If you're interested in helping out with such tasks and would like
access to our statements, read [Inside Gratipay](http://inside.gratipay.com/)
and then introduce yourself on [the
Radar](http://inside.gratipay.com/howto/sweep-the-radar).


# Help

[Open an issue](https://github.com/gratipay/finances/issues/new) if you're having problems.


# Legal

The scripts and data in this repo are released into the public domain to the
extent possible under [CC0](http://creativecommons.org/publicdomain/zero/1.0/)
or the [OSI license](https://opensource.org/licenses) of your choosing.
