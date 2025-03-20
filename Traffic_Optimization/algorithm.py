class Trffclght:
    units = []
    def __init__(self,  n_phases : int, all_crtclflw : float, of : list, sf : list, edges : list, all_red = 0, lst_phs_time = 2):
        self.units.append(self)                             #register the instance of trafficlight
        self.n_phases = n_phases                            #number of phases
        self.lost_time = (n_phases * lst_phs_time) + all_red#lost time
        #self.ltst_allcrtflw = all_crtclflw                  #summation of all critical flow
        self.ltst_of = of                                   #latest observed flows
        self.ltst_sas = sf                                  #total saturation flow on the routes
        self.ltst_crtflws_rt = []
        for i in range(len(of)): self.ltst_crtflws_rt.append(of[i]/sf[i])
        self.ltst_allcrtflws_rt = all_crtclflw
        self.ltst_optmcycle = 0                             #latest cycle caulculated
        self.ltst_greens = []                               #latest greens calculated
        self.edges = edges

    def update(self, all_crtclflw, of, sf):
        #self.latst_crtflw = all_crtclflw #summation of all critical flow
        self.ltst_ov = of #latest observed flows
        self.ltst_sas = sf    #total saturation flow on the routes
        for i in range(len(of)): self.ltst_crtflws_rt.append(of[i]/sf[i])
        self.ltst_allcrtflws_rt = all_crtclflw
        self.ltst_optmcycle = get_optmcycle(self.ltst_allcrtflws_rt, self.lost_time)
        #self.ltst_greens = get_greens(self.ltst_crtflws_rt, self.ltst_allcrtflws_rt, self.ltst_optmcycle, self.lost_time)

def get_optmcycle(allcrtflws_rt, lost_time : int):
    optmcycle = (1.5 * float(lost_time) + 5) / (1 - allcrtflws_rt)
    return optmcycle

def get_greens(crtflws_rt, allcrtflws_rt, ltst_optmcycle, lost_time):

    greens = []
    for i in len(crtflws_rt):
        greens.append((crtflws_rt[i]/allcrtflws_rt)*(ltst_optmcycle - lost_time))
    
    return greens

n_phases = 2
all_crtclflw = 0.57
of = [400, 250]
sf = [1250, 1000]
edges = ['a', 'b']

sinal = Trffclght(n_phases, all_crtclflw, of, sf, edges)
#sinal2 = Trffclght(2,2,2,2)
sinal.update(all_crtclflw, of, sf)
print(sinal.ltst_optmcycle)
