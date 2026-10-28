import sys, pickle; sys.path.insert(0,'..')
from pdfmerge import new_overlay, merge
from render_preview import draw_scene
import scene2
S,D,a,b,h=scene2.build_all()
pickle.dump((S,),open('../scene2_cache.pkl','wb'))
fig,ax=new_overlay(); draw_scene(ax,S,'A0')
merge('/home/user/RancangKota/Claude outputs/Siteplan_Rev_24Okt/SitePlan_Kroya_Smart_Unified_Market_Rev_24Okt_SitePlan_A0.pdf',fig,'../out_test3.pdf')
