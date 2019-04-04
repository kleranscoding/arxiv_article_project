import xml.etree.ElementTree as ET
import urllib
import datetime
import unicodedata
import operator

# define base url and search criteria for arxiv API
api_url = "http://export.arxiv.org/api/query"

search_category = "?search_query=all:psychiatry+OR+all:therapy+OR+cat:cs.LG+OR+cat:data+science"
search_author = "?search_query=au:"
sort_order = "&sortBy=submittedDate&sortOrder=descending"
delta = 30

# define the namespace
namespace = {'feed': 'http://www.w3.org/2005/Atom'}


## function to get xml root using urllib 
## and parse the XML document with xml etree
def get_xml_root(url):
    # get data using urllib and parse the XML document with xml etree
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return None 
    return ET.parse(response).getroot()


## function for getting relevant articles
## param: article_id (the article id)
## return entry_list (list)
def get_articles(article_id = None):
  
    '''
    if article_id is not provided, 
    return a list of article entries with article_id, title and published date
    else, 
    return the article detailed information including summary and a list of authors
   
    '''
    entry_list = []

    if article_id:
        url = api_url + "?id_list=" + article_id

        # get xml root
        root = get_xml_root(url)
        
        # return list of empty object if root is None
        if not root:
            entry_list.append({})
            return entry_list

        entry = root.find('feed:entry', namespace)
        title = entry.find('feed:title', namespace).text
        summary = entry.find('feed:summary', namespace).text
        published = entry.find('feed:published', namespace).text.replace("T", " at ").replace("Z"," UTC")

        authors = []
        for author in entry.findall('feed:author', namespace):
            authors.append(author.find('feed:name', namespace).text)
        entry_list.append({'title': title, 'summary': summary,'published': published, 'authors': authors})
  
    else:

        max_limit = 50
        max_results = "&max_results=" + str(max_limit)
        url = api_url + search_category + sort_order + max_results

        # get xml root
        root = get_xml_root(url)

        for entry in root.findall('feed:entry', namespace):
        
            # get article id by spliting the url by "/" and get the last item
            article_id = entry.find('feed:id', namespace).text.split("/")[-1]
            title = entry.find('feed:title', namespace).text
            published = entry.find('feed:published', namespace).text.replace("T", " at ").replace("Z"," UTC")

            # append each entry as a dictionary k-v pair 
            entry_list.append({'article_id': article_id, 'title': title, 'published': published})

    return entry_list


## function for getting author details
## param: author as string
## return entry_list (list)
def get_author_details(author):

    entry_list = []
    if not author: 
        return entry_list

    # parse author name to the format: lastName_firstName_<middle> 
    name = author.replace(".", "").split(" ")
    name.insert(0, name.pop(-1))
    if len(name) == 3 and len(name[-1]) >= 2:
        name.insert(0, name.pop(-1))

    # encode to ascii
    author_name = "_".join(name).lower()
    author_name = unicodedata.normalize('NFKD', author_name).encode('ascii','ignore').decode('utf-8')
    #print(author_name)

    # get today's date and 30 days ago
    now = datetime.datetime.now()
    ago = now - datetime.timedelta(days=delta)
    
    max_limit = 20
    max_results = "&max_results=" + str(max_limit)

    keep_looping = True
    while keep_looping:
        
        url = api_url + search_author + author_name + sort_order + max_results

        # get xml root
        root = get_xml_root(url)

        all_entries = root.findall('feed:entry', namespace)
        for entry in all_entries:
            
            published = entry.find('feed:published', namespace).text
            
            # convert published_time to datetime object
            date_obj = datetime.datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')
            if date_obj < ago: 
                continue

            # get article id by spliting the url by "/" and get the last item
            article_id = entry.find('feed:id', namespace).text.split("/")[-1]
            title = entry.find('feed:title', namespace).text
            published = published.replace("T", " at ").replace("Z"," UTC")

            # append each entry as a dictionary k-v pair 
            entry_list.append({'article_id': article_id, 'title': title, 'published': published})

        ## stop looping if entry_list has at least one article
        ## or stop looping if there are no entries for that author
        ## otherwise do increase days_delta to another 30 days period
        if len(entry_list) > 0:
            keep_looping = False
        elif len(all_entries) == 0:
            keep_looping = False
        else:
            now = ago
            ago = now - datetime.timedelta(days=delta)

    return entry_list
  

## function for getting a list of author
## return author_list (list of tuples)
def get_authors_list():

    max_limit = 10
    max_results = "&max_results=" + str(max_limit)

    author_list = []

    # get today's date and 30 days ago
    now = datetime.datetime.now()
    ago = now - datetime.timedelta(days=delta)
    
    url = api_url + search_category + sort_order + max_results
    # get xml root
    root = get_xml_root(url)
    
    # create dict / hashmap to store author and number of contribution
    author_dict = {}

    enough_authors = False

    for entry in root.findall('feed:entry', namespace):
    
        published = entry.find('feed:published', namespace).text
        
        # convert published_time to datetime object
        date_obj = datetime.datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')

        if enough_authors:
            break

        '''
        name = entry.find('feed:author', namespace).find('feed:name', namespace).text
        if not author_dict.get(name):
            print(name)
            num = len(get_author_details(name))
            author_dict[name] = num
        #'''

        #'''
        for author in entry.findall('feed:author', namespace):

            author_name = author.find('feed:name', namespace).text
            if not author_dict.get(author_name):
                num = len(get_author_details(author_name))
                author_dict[author_name] = num

            if len(author_dict) >= max_limit:
                enough_authors = True
                break
        #'''
    
    # sort dict based on number of contributions
    author_list = sorted(author_dict.items(), key=lambda kv: kv[1], reverse=True)    
    return author_list