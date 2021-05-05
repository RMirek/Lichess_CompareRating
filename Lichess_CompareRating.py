import time
import json
import urllib
import matplotlib.pyplot as plt
import ast
import numpy as np
import datetime
import matplotlib.dates as mdates

def get_user_points(user):
    print('Processing user: ', user)
    user_history = urllib.request.urlopen(
        "http://en.lichess.org/api/user/" + user + '/rating-history').read()
    return ast.literal_eval(json.loads(user_history)[1:-1])

users_list = ['rwmmir', 'Thibault'] # list of users, you can put as many as you want

GAME_TYPE = 'Blitz' #Bullet, Blitz, Rapid, Classical...

fig, ax = plt.subplots(1,1, figsize=(8, 6), facecolor='w', edgecolor='k')

for i, user in enumerate(users_list):
    user_points = get_user_points(user)
    
    for game in user_points: 
        if game['name'] == GAME_TYPE:
            points = np.array(game['points'])
            dates = [datetime.datetime(x[0], x[1]+1, x[2]) for x in points[:,:3]]
            plt.plot(dates, points[:,3], label=user, linewidth=2)
            time.sleep(1)
    
ax.set_ylabel(GAME_TYPE + ' rating',fontsize=20)
ax.set_xlabel('Date',fontsize=20)   
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.legend(fontsize=20)
ax.tick_params(axis='both', direction = "in", which='major', labelsize = 20,
    right = True, top = True, left = True)    