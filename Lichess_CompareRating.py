import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
import requests

def getUserPoints(user):
    resp = requests.get(url = 'http://lichess.org/api/user/' + user + '/rating-history')
    return resp.json()

def createFigure(variants, ncols=2):
    nrows = int(np.ceil(len(variants)/ncols))    
    fig, ax = plt.subplots(nrows, ncols, figsize=(8*nrows, 5*ncols), facecolor='w', edgecolor='k')
    return fig, ax

def get_nrow_ncol(number):
    nrow = int(np.floor(number/2))
    ncol = int(np.ceil(number/2)-1)
    return nrow, ncol

def formatTicks(nrow, ncol):
    ax[nrow, ncol].format_xdata = mdates.DateFormatter('%Y')    
    fmt_month = mdates.MonthLocator()
    ax[nrow, ncol].xaxis.set_minor_locator(fmt_month)
    ax[nrow, ncol].set_ylabel(variant + ' rating',fontsize=20)
    ax[nrow, ncol].set_xlabel('Date',fontsize=20)   
    
    ax[nrow, ncol].legend(fontsize=20)
    ax[nrow, ncol].tick_params(axis='both', direction = "in", which='major', labelsize = 20,
        right = True, top = True, left = True)    
    plt.setp(ax[nrow, ncol].get_xticklabels(), rotation=30, horizontalalignment='right')
    
users_list = ['rwmmir', 'Marianczellini'] # list of users, you can put as many as you want
variants = ['Bullet', 'Blitz', 'Rapid', 'Classical'] # variants, you can put as many as you want

fig, ax = createFigure(variants)

for i, variant in enumerate(variants):
    nrow, ncol = get_nrow_ncol(i)
    for user in users_list:
        userPoints = getUserPoints(user)
        for game in userPoints: 
            if game['name'] == variant:
                points = np.array(game['points'])
                if len(points)>0:
                    dates = [datetime.datetime(x[0], x[1]+1, x[2]) for x in points[:,:3]]
                    ax[nrow, ncol].plot(dates, points[:,3], label=user, linewidth=2)
                   
    formatTicks(nrow, ncol)                
    
if len(variants)%2==1:
    ax[nrow][ncol+1].set_visible(False)     

fig.tight_layout()        
plt.show()

# save_name = '_'.join(users_list) + '_' + '_'.join(variants)
# fig.savefig(save_name, bbox_inches='tight', dpi=100)
# plt.cla()
# plt.clf()
# plt.close('all')
