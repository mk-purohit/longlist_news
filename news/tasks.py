from celery import shared_task

from decouple import config    # Needed to read environment variable SERP_API_KEY
import json  # for serialising data in to file and vice versa

from urllib import parse as url_parse
from urllib import request as url_request

import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as dt_parse

from .models import Newsitem, Key, Company, Postingsite

# Create your views here.

def get_past_date(str_days_ago):
    # Convert the past date string 
    # like today, yesterday, 2 days ago, 3 months ago, 4 weeks ago, 7 hours ago, 3 mins ago or 2 secs ago
    # in to yyyy-mm-dd date type object.

    TODAY = datetime.date.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return str(TODAY.isoformat())
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return str(date.isoformat())
    elif splitted[1].lower() in ['second', 'seconds', 'sec', 'secs', 's']:
        date = datetime.datetime.now() - relativedelta(seconds=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['minute', 'minutes', 'min', 'mins', 'm']:
        date = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = TODAY - relativedelta(weeks=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = TODAY - relativedelta(months=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return str(date.isoformat())
    else:
        # str_days_ago is not in the desired format, instead is like Nov 15, 1957 etc.
        date = dt_parse(str_days_ago).date()    
        return str(date.isoformat())


def process_data(data):


    if data["news_results"]:

        existing_sources = list(Postingsite.objects.all().values('name', 'quality'))     # Returns a list of dictionaries with the keys name and quality from postingsites table
        list_postingsites = [d['name'] for d in existing_sources]                        # Returns the list of names of Postingsites, list comprehension

        for item in data["news_results"]:
            if item["source"] in list_postingsites and next(dic for dic in existing_sources if dic["name"] == item["source"])["quality"]:
                # Save the news item record in Newsitem table of database if the link doesnot exist
                obj,created = Newsitem.objects.get_or_create(link=item['link'],
                defaults = {
                    'title':item['title'],
                    'source':item['source'],
                    'snippet':item['snippet'],
                    'date_posted': get_past_date(item['date']),
                    }
                )

            elif item["source"] in list_postingsites and not next(dic for dic in existing_sources if dic["name"] == item["source"])["quality"]:
                pass                
                # discard this news item record, not to be saved in the database

            elif item["source"] not in list_postingsites:
                # Save the source name in Postingsite table of database with quality as True
                obj = Postingsite(name=item["source"])
                obj.save()

                # Save the news item record in Newsitem table of database if the link doesnot exist
                obj,created = Newsitem.objects.get_or_create(link=item['link'],
                defaults = {
                    'title':item['title'],
                    'source':item['source'],
                    'snippet':item['snippet'],
                    'date_posted': get_past_date(item['date']),
                    }
                )

    return

def get_news_data(query_url):
    # Use urllib.request ie. url_request to make the request, 
    # and use json to convert the data of the API response into a Python dictionary

    """Makes an API request to a URL and returns the data as a Python object.
    Args:
        query_url (str): URL formatted for SerpAPI endpoint
    Returns:
        dict: News items 
    """
    response = url_request.urlopen(query_url)
    data = response.read()

    return json.loads(data)


def build_serp_query(search_string):
    # build the query for serp api based upon the serach string and other parameters to download the news data.

    BASE_SERP_API_URL = "https://serpapi.com/search.json"
    search_type = "nws"
    search_location = "India"
    api_key = config('SERP_API_KEY')

    search_url = (
            f"{BASE_SERP_API_URL}?q={search_string}&tbm={search_type}&location={search_location}&api_key={api_key}"
        )

    return search_url


# Scheduled Task for creating the seach strings, constructing the url for serp endpoint, getting the response news item 
# and saving the desired news items in the database. 
@shared_task()
def get_process_news():

    # create search_queries..

    company_names = list(Company.objects.filter(status=True).values_list('name', flat=True))
    search_strings = list(Key.objects.filter(status=True).values_list('name', flat=True))

    search_queries = []

    for search_string in search_strings:
        for company_name in company_names:
            if "$company" in search_string:
                query_string = search_string.replace("$company", company_name)
            else:
                query_string = company_name + " " + search_string
            search_queries.append(query_string)

    for search_query in search_queries:
        url_encoded_search_query = url_parse.quote_plus(search_query)   # encode the query to make it url configured like replacing the whhite spaces in query with plus sign et.
        query_url = build_serp_query(url_encoded_search_query)
    
        news_data = get_news_data(query_url)
        json.dump( news_data, open( search_query + ".json", 'w' ) )    # Serialize data into file:
  
        process_data(news_data)

    return


# Tasks for testing purposes

@shared_task()
def my_first_task():
    from datetime import datetime     # needed for my_first_task

    now = datetime.now() # current date and time
    time = now.strftime("%H:%M:%S")
    open(time+'.txt', 'w').close()
    return


@shared_task
def hello_world():
    print('Hello world!')
    return

