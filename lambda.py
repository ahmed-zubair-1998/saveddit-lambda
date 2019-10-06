import praw
import string
import json


def lambda_handler(event, context):

  reddit = praw.Reddit(client_id=client_id,	#Reddit Client ID
                       client_secret=client_secret,	#Reddit Clieent Secret
                       user_agent=agent,	#User Agent
                       password=password,	#Reddit Account Password
                       username=user)		#Reddit username
						#Read Reddit API Documentation to Learn About These Values
  
  saved = reddit.redditor(user).saved(limit=None)
  
  title_dict = {}
  subreddits = {}
  posts = []
  start_url = 'https://www.reddit.com'
  count = 0
  count_err = 0
  
  table = str.maketrans('', '', string.punctuation)
  for x in saved:
    try:
      title = x.title.lower().translate(table).split()
      text = x.selftext.lower().translate(table).split()
      for word in title:
        if word in title_dict:
          title_dict[word].append([start_url + x.permalink, x.title])
        else:
          title_dict[word] = [[start_url + x.permalink, x.title],]
      for word in text:
        if word in title_dict:
          title_dict[word].append([start_url + x.permalink, x.title])
        else:
          title_dict[word] = [[start_url + x.permalink, x.title],]
      s = x.subreddit._path[:-1]
      if s in subreddits:
        subreddits[s] += 1
      else:
        subreddits[s] = 1
      posts.append([(start_url + x.permalink), x.title])
      count += 1
    except Exception as e:
      print(e)
      count_err += 1


  if event["type"] == "posts":
    return {
        'statusCode': 200,
        'body': json.dumps(posts)
    }
  
  if event["type"] == "subreddits":
    return {
        'statusCode': 200,
        'body': json.dumps(subreddits)
    }
  
  return {
        'statusCode': 200,
        'body': json.dumps(title_dict[event["type"]])
    }
