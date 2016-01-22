# Gratipay Finances

This is [Gratipay](https://gratipay.com/)'s financial accounting system, which
is based on [Ledger](http://ledger-cli.org/). We have a directory for each
year, and an `NN.dat` file for each month. Our wrapper scripts are in the
`bin/` directory; add it to your `PATH` for best results. Each month gets [a
PR](https://github.com/gratipay/finances/pulls).

[![status](https://api.travis-ci.org/gratipay/finances.svg)](https://travis-ci.org/gratipay/finances)


## How Our Books are Organized

The biggest reality in our finances is that we have **operations**&mdash;*our*
money&mdash;and then we have **escrow**&mdash;*other people's* money. Never the
twain shall meet (more or less). Beyond the basic accounting principle that
assets must equal liabilities plus equity, nearly as important for Gratipay is
that escrow assets must always equal escrow liability: when people think we're
holding their money, we'd better be holding their money!

Actually, though, our income from processing fees comes to us from our upstream
processors commingled with escrow, *and* we want to keep our fee *income* as
close to our fee *expenses* as possible (our *operating* income, of course,
comes [through Gratipay](https://gratipay.com/Gratipay/) just like any other
Gratipay Team).  To deal with this dual reality, we use a **fee buffer**.
Ideally the balance in the fee buffer is zero, though of course it varies in
practice.

You'll see, then, that the assets on our balance sheet, as well as our income
and expenses on our income statement, are broken down according to these three
second-level categories: escrow, fee buffer, and operations. The fee buffer and
operations on the income statement hit retained earnings on the balance sheet.
Escrow on the income statement hits escrow liability on the balance sheet.

Whereas the second-level categories are *logical*, our actual *physical* bank
and processor accounts end up as third-level categories. So, for example, our
actual balance at New Alliance Federal Credit Union is equal to the sum of
these three balance sheet accounts:

 - Assets:Escrow:New Alliance
 - Assets:Fee Buffer:New Alliance
 - Assets:Operations:New Alliance


## Working on the Finances

First, you'll need [Ledger](http://ledger-cli.org/) (v3),
[Python](https://www.python.org/) (v2.7), a [text
editor](https://en.wikipedia.org/wiki/Text_editor), and a [command
line](https://en.wikipedia.org/wiki/Command-line_interface). Then basically
what you're gonna do is edit the dat file for the month you're working on, and
then, from the root of your clone of this repo, run (with
[`bin`](https://github.com/gratipay/finances/blob/master/bin/) on your `PATH`):

```bash
clear && test.py && balance-sheet.py && income-statement.py
```

That'll check for errors (we also have CI set up [at
Travis](https://travis-ci.org/gratipay/finances)) and then show you a balance
sheet and income statement. If you need to add accounts or currencies you can
do so in
[`declarations.dat`](https://github.com/gratipay/finances/blob/master/declarations.dat).
If you want to run arbitrary ledger commands, we provide a wrapper that points
ledger to our dat files for your convenience:

```bash
wledger.py register
```


### Style

Here are some style notes for the dat files:

 1. Group transactions together conceptually.

 1. Transactions should be generally date-sorted, but it's okay to fudge that a
    little for the sake of (1).

 1. Record debits first.

 1. Symmetry is nice. 

 1. Use comments! Especially for weird stuff.


### Access

Many accounting tasks require access to Gratipay's bank and payment processor
statements. If you're interested in helping out with such tasks, read [Inside
Gratipay](http://inside.gratipay.com/) and then introduce yourself on [the
Radar](http://inside.gratipay.com/howto/sweep-the-radar).


# Help

[Open an issue](https://github.com/gratipay/finances/issues/new) if you're having problems.


# Legal

The scripts and data in this repo are released into the public domain to the
extent possible under [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
