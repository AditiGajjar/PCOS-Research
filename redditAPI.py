# # OPTION 1:
#
# import requests
# import pandas as pd
import praw
import pandas as pd

#
# auth = requests.auth.HTTPBasicAuth('VIx_RDaZR5jRr6PzudlNgg', 'FbYqg9VQnP2JMW58y1iSJm7pz4dqqQ')
#
# data = {'grant_type': 'password',
#         'username': 'ConsciousCandy7',
#         'password': 'Adg@0030'}
#
# headers = {'User-Agent': 'MyPCOSBot/0.0.1'}
#
# # send our request for an OAuth token
# res = requests.post('https://www.reddit.com/api/v1/access_token',
#                     auth=auth, data=data, headers=headers)
#
# # convert response to JSON and pull access_token value
# TOKEN = res.json()['access_token']
#
# # add authorization to our headers dictionary
# headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
#
# # while the token is valid (~2 hours) we just add headers=headers to our requests
# requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
#
# res = requests.get('https://oauth.reddit.com/r/PCOS/?f=flair_name%3A"Weight"',
#                    headers=headers)
#
# df = pd.DataFrame()  # initialize dataframe
#
# # loop through each post retrieved from GET request
# for post in res.json()['data']['children']:
#     # append relevant data to dataframe
#     df = df.append({
#         'subreddit': post['data']['subreddit'],
#         'title': post['data']['title'],
#         'selftext': post['data']['selftext'],
#         'upvote_ratio': post['data']['upvote_ratio'],
#         'ups': post['data']['ups'],
#         'downs': post['data']['downs'],
#         'score': post['data']['score']
#     }, ignore_index=True)
#
# print(df.head())

# OPTION 2:

features = [
    'ID',
    'num_comments',
    'Title',
    'Subreddit',
    'Body',
    'URL',
    'Upvotes',
    'created_on',
    'Comments'
]

reddit = praw.Reddit(client_id='VIx_RDaZR5jRr6PzudlNgg', client_secret='FbYqg9VQnP2JMW58y1iSJm7pz4dqqQ',
                     user_agent='MyPCOSBot/0.0.1 by /u/ConsciousCandy7', username='ConsciousCandy7',
                     password='Adg@0030', )


posts = []
subreddit_total = reddit.subreddit('PCOS')

print("Collecting for flair: weight")
relevant_subs = subreddit_total.search(f"flair_name:{'Weight'}", limit=500)
for sub in relevant_subs:
    post = [
        str(sub.id),
        sub.num_comments,
        str(sub.title),
        str(sub.subreddit),
        str(sub.selftext),
        str(sub.url),
        sub.score,
        sub.created_utc,
    ]

    # Collect comments
    sub.comments.replace_more(limit=None)
    comment = ''
    for top_comment in sub.comments:
        comment = str(top_comment.body) + ' '

    post.append(str(comment))  # Add to the end of the list
    posts.append(post)  # Add to the main list

    # Update after every 100 posts
    if len(posts) % 100 == 0:
        print("Number of posts collected: {}".format(len(posts)))

# Convert to a data frame
posts_df = pd.DataFrame(posts,  columns=features)

print("The size of the collected dataframe is: {}".format(posts_df.shape))

# Using the to_datetime function of pandas to convert time from UNIX to regular
posts_df['creation_date'] = pd.to_datetime(posts_df['created_on'], dayfirst=True, unit='s')
# Drop created_on column now
posts_df.drop(['created_on'], axis=1, inplace=True)

print(posts_df)

posts_df.to_csv('/Users/aditigajjar/Desktop/reddit_raw.csv')

