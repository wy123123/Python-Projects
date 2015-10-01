import urllib2
import json
import sqlite3

def main():
    #retrive any facebook page posts  
    #fill in the name of the company in the list_companies if the url of a fb user is https://www.facebook.com/user1
    list_companies = ["lovebonito"]
    app_id = "1447448915558555"
    secret = "75bb10a5327c9ae811775471b4fb4d39"
    graph_url = "https://graph.facebook.com/"
    #connection to database
    con = sqlite3.Connection("c:/users/lovebonito/desktop/sqlite/lbFB.db")
    c = con.cursor()
    try:
        query = '''create table testing2 (
        id INTEGER primary key,
        page_name char,
        post_id char unique,
        post_date char,
        post_story char,
        post_name char,
        No_post_likes,
        No_comments
        )'''
        c.execute(query)
        print "Table testing2 created"
    except:
        print "Table already exist"
    
    for company in list_companies:      
        get_post_ids_and_time(graph_url,company,app_id,secret)

#create  FB weburls using graph API
def create_post_url(graph_url,company, APP_ID, APP_SECRET,limit=150, since=None,until=None,field=None):
    #method to return 
    post_args = "&access_token=" + APP_ID + "|" + APP_SECRET
    if since != None and until != None:
        post_url = graph_url +company+"/"+ "posts?" + "limit=" + str(limit) + "&until=" + until+ "&since="+ since + post_args
        return post_url
    elif until != None and since == None:
        post_url = graph_url +company+"/"+ "posts?" + "limit=" + str(limit) + "&until=" + until + post_args
        return post_url
    elif since != None and until== None:
        post_url = graph_url +company+"/"+ "posts?" + "limit=" + str(limit) + "&since="+ since + post_args
        return post_url
    elif since == None and until == None:
        post_url = graph_url +company+"/"+ "posts?" + "limit=" + str(limit) + post_args
        return post_url

#construct the url for each post
def find_post_or_comment_url(graph_url,post_id,APP_ID,APP_SECRET):
    post_args = "&access_token=" + APP_ID + "|" + APP_SECRET
    post_likes = graph_url + post_id +"/likes?summary=1"+post_args
    post_comments = graph_url + post_id +"/comments?summary=1"+post_args
    return (post_likes,post_comments)

#read urls and download the data to json format
def read_webpage_to_json(url,data='data'):
    web_response = urllib2.urlopen(url)
    readable_page = web_response.read()
    json_postdata = json.loads(readable_page)
    json_fbposts = json_postdata[data]
    return json_fbposts

#get the page_name, post_id, post_date, post_story, post_name, store it to a sqlite database
def get_post_ids_and_time(graph,company,app_id,secret):
    print create_post_url(graph,company,app_id,secret)
    posts = read_webpage_to_json(create_post_url(graph,company,app_id,secret))
    data_list = ["id","created_time","story","message"]
    count = 0
    for post in posts:
        line_data = []
        try:
            line_data.append((post["from"]["name"]))
        except:
            line_data.append(("NA"))
        for dummy_index in range(len(data_list)):
            try:
                line_data.append((post[data_list[dummy_index]]))
            except:
                line_data.append(("NA"))
                
        #get the number of post likes/commment
        post_id_page = find_post_or_comment_url(graph,line_data[1],app_id,secret)
        post_likes_data = read_webpage_to_json(post_id_page[0],"summary")
        post_comments_data = read_webpage_to_json(post_id_page[1],"summary")
        line_data.append(post_likes_data["total_count"])
        line_data.append(post_comments_data['total_count'])
        c.executemany("insert or ignore into testing2(page_name,Post_id,Post_date,Post_story,Post_name,No_post_likes,No_comments) values(?,?,?,?,?,?,?)",(line_data,))
        count += 1
    latest_date = str(line_data[2])[:str(line_data[2]).find("T")]
    con.commit()
    print "Downloaded ",count,"posts from",company
    while count <1000:
        print create_post_url(graph,company,app_id,secret,until=latest_date)
        posts = read_webpage_to_json(create_post_url(graph,company,app_id,secret,until=latest_date))
        for post in posts:
            line_data = []
            try:
                line_data.append((post["from"]["name"]))
            except:
                line_data.append(("NA"))
            for dummy_index in range(len(data_list)):
                try:
                    line_data.append((post[data_list[dummy_index]]))
                except:
                    line_data.append(("NA"))
                
        #get the number of post likes/commment
            post_id_page = find_post_or_comment_url(graph,line_data[1],app_id,secret)
            post_likes_data = read_webpage_to_json(post_id_page[0],"summary")
            post_comments_data = read_webpage_to_json(post_id_page[1],"summary")
            line_data.append(post_likes_data["total_count"])
            line_data.append(post_comments_data['total_count'])
            c.executemany("insert or ignore into testing2(page_name,Post_id,Post_date,Post_story,Post_name,No_post_likes,No_comments) values(?,?,?,?,?,?,?)",(line_data,))
            count += 1
        latest_date = str(line_data[2])[:str(line_data[2]).find("T")]
        con.commit()
        print "Downloaded ",count,"posts from",company

if __name__ == "__main__":
    main()
