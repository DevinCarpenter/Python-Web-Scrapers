# Python-Web-Scrapers
Web Scrapers built using Python and the MechanicalSoup Library.

These web scrapers are examples of how you would use python to extract data from HTML files and web pages, but have been dummed down
and are purely for examples sake.

Mechanical Soup is a library for parsing HTML. It is built for Python 3 since earlier libraries only support Python 2 (Mechanize).
Most of the documentation can be found within Beautiful Soup 4 docs as Mechanical Soup is based off of Beautiful Soup 4 and Mechanize.

## Usage

**Mechanical Soup DOES NOT DO JAVASCRIPT:** You cannot use it to interact with any javascript on the page i.e button clicking, menus, slideshows, etc.
If you need something that can do javascript (and also uses much more system resources) you might use Selenium paired with PhantomJS.

**Unicode Errors:** Windows 10 command prompt has Unicode issues. Use python IDLE to run the scripts if unicode errors occur.

**MechanicalSoup Vs. BeautifulSoup Docs:** In mechanical soup you start by declaring a browser object and then opening a webpage.
Beautiful Soup does the same thing but a little different.

Here's the Beautiful Soup syntax:

    from bs4 import BeautifulSoup
    import re #module to support Regular Expressions
    with open("index.html") as fp:
      soup = BeautifulSoup(fp)
    
    soup.find_all(href=re.compile("google.com")) #finds elements with 'google.com' inside href attribute

Here's the Mechanical Soup syntax:

    import mechanicalsoup
    import re #module to support Regular Expressions
    
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://example.com")
    
    browser.get_current_page().find_all(href=re.compile("google.com")) #finds elements with 'google.com' inside href attribute
    
Notice the difference in getting the element from the data? In short, you can use the beautiful soup 4 docs so long as you remember that
mechanical soup uses the `get_current_page()` where beautiful soup does not.


## References

https://github.com/MechanicalSoup/MechanicalSoup

http://mechanicalsoup.readthedocs.io/en/stable/introduction.html

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

http://akul.me/blog/2016/beautifulsoup-cheatsheet/

http://www.seleniumhq.org/
