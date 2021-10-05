# Things to do

- [x] Store fractional values as they appear on the page, where the value stored is the denominator (i.e., store `5.0` instead of `0.2`) because floats can get weird
- [ ] Handle jackpots differently, rather than store their current jackpot value in db.
  - If jackpot, force requery page?
- [ ] async page requests
- [ ] don't use `print()` for everything, use `info`, `warn`, `err` logging.
- [ ] print data in a table form for easier comparison