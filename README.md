# edgar_data_base
Build your own version of Edgar DB for faster NLP analysis
The prograpm helps you build a database with the relevant type of issuer related links into Edgar for fast access. I built and used this program a year ago when I was testing the use of NLP for automatic financial and investing tools.

The current program is building a table with the 10-K reports (the annual reports) links. You can modify it as yoiu wish to get additional/other disclosure links, depending on what you actually need to do.

The program needs 2 additional components to work:
- The EDGAR INDEX files. This is what it actually parses, and that is where it gets the links from
- that you set up your database properly, and then pass the relevant login information. I used MySQL for this, but any database works. Make sure you have the relevant driver set up.
