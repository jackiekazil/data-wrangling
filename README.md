## Data Wrangling with Python

Welcome to the code repository for [Data Wrangling with Python](http://shop.oreilly.com/product/0636920032861.do)! We hope you find the code and data here useful. If you have any questions reach out to @kjam or @JackieKazil on Twitter or GitHub.

### Code Structure

We've kept all of the code samples in folders separated by chapters and the data in a similar fashion. You'll likely want to 'undo' this work. It will be far more useful for you to have the data all in one folder so you can easily import and use. Remember, storing data in a repository is usually not a good idea; we've done it here so you can replicate the work you see in the book.

### Code Examples

We have not included every code sample you've found in the book, but we have included a majority of the finished scripts. Although these are included, we encourage you to write out each code sample on your own and use these only as a reference.

We've also included some of the data investigation and IPython exploration used to first determine what to explore with the book. If you have any questions about the code you see in the book or the exploration conclusions, please reach out. Most of the exploration was performed using an older version of some of the libraries, so it might not work without modification.

#### Scraping Data Folders

In case the web pages the book uses change significantly, we've included copies of the web pages as they are now. You can use them and tell the scraping library to access them via a File URI (normally `file://file_name.html`).

 * Note: this has already occured with the Fairphone page. Please see `data/chp11/fairphone.html` to see the old page as it was in the book


### Firefox Issues

Depending on your version of Firefox and Selenium, you may run into JavaScript errors. Here are some fixes:
 * Use an older version of Firefox
 * Upgrade Selenium to >=3.0.2 and download the [geckodriver](https://github.com/mozilla/geckodriver/releases). Make sure the geckodriver is findable by your PATH variable. You can do this by adding this line to your `.bashrc` or `.bash_profile`. (Wondering what these are? Please read the Appendix C on learning the command line).
 * Use [PhantomJS](http://phantomjs.org/) with Selenium (change your browser line to `webdriver.PhantomJS('path/to/your/phantomjs/installation')`)
 * Use Chrome, InternetExplorer or any other [supported browser](http://www.seleniumhq.org/about/platforms.jsp)

Feel free to reach out if you have any questions!

### Corrections?

If you find any issues in these code examples, feel free to submit an Issue or Pull Request. We appreciate your input!

### Questions?

Reach out to @kjam and @JackieKazil on Twitter or GitHub. @kjam is also often on freenode. :)
