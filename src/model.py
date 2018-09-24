# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
import functions
import numpy

BASE_PATH = "C:/Users/aelek/source/antoniaelek/fantasy-premier-league/"
SEASON = "2018-19"
PLAYER = 'Eden_Hazard'
ID = 122

player = functions.get_player_data(base_path=BASE_PATH, player=PLAYER + '_' + str(ID), season=SEASON)
player.to_csv('C:/users/aelek/Desktop/out.csv', sep='\t')

# X = ALLDF['full_name_code','avail_status','team_name','ict_index',]
# Y = ALLDF['points'];
# GKDF = ALLDF[ALLDF['position'] == 'Goalkeeper']
# X.shape()
#
# GKFeatures = SelectKBest(chi2, k=5).fit_transform(X, Y)
#
# print(GKFeatures.shape())
# print(GKDF)

