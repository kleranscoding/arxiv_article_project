# arVix Latest Article

[open app](https://arxiv-article-project.herokuapp.com)

## Overview
This web application retrieves articles and authors contribution information from arVix.org using the arXiv bulk data API (`https://arxiv.org/help/api/index`). Using Python/Django (server-side), users can click on the links and display dynamic views with the help of template static pages. Data processing details is abstracted from the back-end to the front-end users as this application requires heavy data manipulation. After getting the required data from the back-end, the users can see formatted data nice and clear. 

## Assumption
Since the API can only retrieve article information in Atom XML format, several assumptions are made to satisfy the requirement.
1) Assume the xml results from the API call is well formatted
2) Assume each article has at least one author
3) Retrieving articles sort by `submittedDate` and in descending order
4) Assume there is at least one article in the first past 30 days period; if not, keep doing `while` loops to add another 30 days until we find at least one article 
5) a) When attempting to get a list of authors and count the number of articles they have submitted, first select the latest `N` articles and capture the first `N` authors using a hashmap/dictionary. Whenever a new author is encountered, make another API on that author and count the number of articles they have submitted over the last 30 days.
b) Since making an API call may take several seconds, `N<=20` is chosen in order to minimize loading and waiting time. This will ensure the actual number of contribution is acurrately reflected.
6) a) Author names sometimes come in `<full_first> <last_name>` or `<initial_first> <last_name>`. For example, `Bradley Walker` can be referred as `B. Walker`. However, there is no way to verify if `B. Walker` is `Bradley Walker` or `Brandon Walker`, and therefore, this web application will retrieve all articles that contain `B. Walker` and assuming it is the correct `B. Walker` we are looking for.  
b) If author has middle_name length more than 1, i.e. `Adrain Del Maestro` has `Del` as 3 characters, assume that middle name is part of the last name.

## Approach
1) Created pages and routes:
- `/` , an index page that acts as the landing page
- `/articles` , a page which displays the latest 50 articles
- `/articles?article_id=<article_id>` , a page which displays a more detailed article information with the article_id. Note: if `<article_id>` is null, it displays the content from `/articles`
- `/authors` , a page which displays a list of authors
- `/authors?author=<author_name>` , a page which displays the author_name and the last 30 days of contribution starting today. Note: if `<author_name>` is null, it defaults to `/authors`

2) Using the API:
- use python built-in XML parser to parse the XML document, and get the relevant information
- use namespace to find the element tags

3) Parsing author name to call the arXiv API:
a) Author name usually comes in `<first_name> <last_name>` or `<first> <mid intital> <last>`; convert the name to the following format: `<last>_<first>` or `<last>_<first>_<middle initial>`. Note: assumption 6b)
b) e.g. `Bradley Walker` => `walker_bradley`, `B. Walker` => `walker_b`, `Adrain Del Maestro` => `del_maestro_adrain`, `A. Del Maestro` => `del_maestro_a`

4) Getting a list of authors:
Follow assumption 5), the larger the N is the more waiting and loading time the user needs. 

## Testing
- included some unit testings in the application, to invoke testing, enter `python3 manage.py test arxiv_article_app.tests`

## Reflection (ideas not implemented)
1) Do pagination in `/articles`: 
allow users to click next/previous to browse more articles. Incorporate `&start=<start_index>&max_results=<max_limit>` in the URL to make the articles page more dynamic
2) Alternate approach to include a list of authors:
instead of doing the method from assumption 5), browse all related articles within the last 30 days and use a hashmap/dictionary to capture the authors and the frequency of their appearances. However, this approach may require to go through hundreds and thousands of articles which reduce the performance. It is also possible that there is a discrepancy in the actual number of contributions by the author and the number counted from those articles. Besides, this will also generate thousands of authors and it will be hard to navigate.
