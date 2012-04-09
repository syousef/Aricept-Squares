def parse_file(fname):
    f = open(fname, 'r')
    all_trials=[]
    for line in f:
        if line[0] == '#':
            continue
        s = line.split('\t')
        new_dict = {'ssize':int(s[1]),'SOA_gap':float(s[2]),'change':bool(s[3]),'answer':bool(s[4]),
                            'answer_type':s[5],'answer_int':int(s[6].strip('\n'))}
        all_trials.append(new_dict)
    #print all_trials
    return all_trials
        
def calc_maxK(all_trials,fn):
    import numpy as np
    sg = .2
    SetSizes = [1,2,3,4,6]
    
    n_tot = len(all_trials)
    answer_ints = np.array([all_trials[i]['answer_int'] for i in range(n_tot)])
    ind = (np.where(answer_ints > 0))[0]
    Ssizes = [all_trials[i]['ssize'] for i in range(n_tot)]
    Ssizes = np.array([Ssizes[x] for x in ind])
    SOA_gaps = [all_trials[i]['SOA_gap'] for i in range(n_tot)]
    SOA_gaps = np.array([SOA_gaps[i] for i in ind])
    answer_ints = np.array([answer_ints[i] for i in ind])
    print Ssizes, SOA_gaps,answer_ints
    n_trials = len(answer_ints)
    capacities = []
    sets = []
    sgs = []    
    
    for ss in SetSizes:
        try:
            index = (np.where([Ssizes[i] == ss and SOA_gaps[i] == sg for i in range(len(Ssizes))])[0])
            print index, ss,sg
        except ValueError:
            print "skipping ss="+str(ss)+" , sg="+str(sg)
            continue
        ans = np.array([answer_ints[x] for x in index])
        hits =  float(len(np.where([ans[i] == 1 for i in range(len(ans))])[0]))
        misses =  float(len(np.where([ans[i] == 2 for i in range(len(ans))])[0]))
        false_alarms =  float(len(np.where([ans[i] == 3 for i in range(len(ans))])[0]))
        correct_rejects =  float(len(np.where([ans[i] == 4 for i in range(len(ans))])[0]))
        n_change = len(np.where([ans[i] == 1 or ans[i] == 2 for i in range(len(ans))])[0])
        n_nochange = len(np.where([ans[i] == 3 or ans[i] == 4 for i in range(len(ans))])[0])
        print ans
        print hits, misses,false_alarms,correct_rejects
        print n_change, n_nochange
    
        if n_change != 0 and n_nochange != 0:
            C = correct_rejects/n_nochange
            H = hits/n_change
            F = false_alarms/n_nochange
            S = ss
            capacity_1 = C*S*(H - F)/(1-F)
            capacity_2 = S * (H + C -1)
            capacities.append(capacity_2)
            sets.append(S)
            sgs.append(sg)
    
    maxK = np.round(max(capacities))
    print 'calculating maxK....'
    print 'maxK = ' + str(maxK)
    f_cap = open(fn,'a')
    f_cap.write(str(maxK)+'\n')
    return maxK
    
def get_maxK(fname):
    try:
        f = open(fname,'r')
    except IOError:
        print 'no such file:',fname
        return -1
    for line in f:
        if line[0] == '#':
            continue
        k = line
        print k
        if k != '':
            return int(float(k))
        else:
            print 'an error has occurred in getting maxK'
            return -1
        
def plot_em_up(all_trials, fname, maxK=2):
    import numpy as np, pylab as pl
    k = maxK
    SetSizes = [k-1,k,k+1,k+2]
    if k == -1:
        print 'no max K found, assuming maxK=2'
        k = 2
    if k==-2:
        print 'running capacity day1'
        SetSizes = [1,2,3,4,5,6]

    
    SOA_gap = [.015,.025,.05,.075,.100]
    f = open(fname.strip('.txt')+'_K.txt','w')
    n_tot = len(all_trials)
    
    answer_ints = np.array([all_trials[i]['answer_int'] for i in range(n_tot)])
    ind = (np.where(answer_ints > 0))[0]
    Ssizes = [all_trials[i]['ssize'] for i in range(n_tot)]
    Ssizes = np.array([Ssizes[x] for x in ind])
    SOA_gaps = [all_trials[i]['SOA_gap'] for i in range(n_tot)]
    SOA_gaps = np.array([SOA_gaps[i] for i in ind])
    answer_ints = np.array([answer_ints[i] for i in ind])
    print Ssizes, SOA_gaps,answer_ints
    
    n_trials = len(answer_ints)
    
    capacities = []
    sets = []
    sgs = []
    for ss in SetSizes:
        for sg in SOA_gap:
            try:
                index = (np.where([Ssizes[i] == ss and SOA_gaps[i] == sg for i in range(len(Ssizes))])[0])
                print index, ss,sg
            except ValueError:
                print "skipping ss="+str(ss)+" , sg="+str(sg)
                continue
            if index.size ==0:
                print "skipping ss=",str(ss), ", sg=",str(sg), " ... not enough data to calculate K"
                continue
            ans = np.array([answer_ints[x] for x in index])
            hits =  float(len(np.where([ans[i] == 1 for i in range(len(ans))])[0]))
            misses =  float(len(np.where([ans[i] == 2 for i in range(len(ans))])[0]))
            false_alarms =  float(len(np.where([ans[i] == 3 for i in range(len(ans))])[0]))
            correct_rejects =  float(len(np.where([ans[i] == 4 for i in range(len(ans))])[0]))
            n_change = len(np.where([ans[i] == 1 or ans[i] == 2 for i in range(len(ans))])[0])
            n_nochange = len(np.where([ans[i] == 3 or ans[i] == 4 for i in range(len(ans))])[0])
            print ans
            print hits, misses,false_alarms,correct_rejects
            print n_change, n_nochange
            
            if n_change != 0 and n_nochange != 0:
                C = correct_rejects/n_nochange
                H = hits/n_change
                F = false_alarms/n_nochange
                S = ss
                capacity_1 = C*S*(H - F)/(1-F)
                capacity_2 = S * (H + C -1)
                text_to_write=str(ss)+'\t'+str(sg)+'\t'+str(C)+'\t'+str(H)+'\t'+str(F)+'\t'+str(capacity_1)+'\t'+str(capacity_2)+'\n'
                f.write(text_to_write)
                capacities.append(capacity_2)
                sets.append(S)
                sgs.append(sg)
            
    f.close()

    caps = np.array(capacities)
    sets=np.array(sets)
    sgs=np.array(sgs)
        
    if caps.size ==0 or sets.size==0 or sgs.size==0:
        print "no data to plot"
        return 0
    pl.clf()
    pl.title('Capacity')
    #pl.axis([0,7,-1,5])
    pl.xlabel('Set Size')
    pl.ylabel('Capacity (K)')
    for soa in unique(sgs):
        ww = np.where([x == soa for x in sgs])[0]
        K = caps[ww]
        S = sets[ww]
        pl.plot(S,K)
        pl.hold(True)
    print "Thank you for your cooperation. See you next time!"
    pl.plot(S,S)
    names = ['SOA_gap = '+str(x) for x in unique(sgs)]
    names.append('Linear model')
    pl.legend(names,loc=0)
    pl.savefig(fname.strip('.txt')+'_plot.png')
   
  
def unique(seq): 
    # order preserving, returns unique value in sequence
    checked = []
    for e in seq:
       if e not in checked:
           checked.append(e)
    return checked 

def get_rand_seq(min,max):
    import urllib
    url = "http://www.random.org/sequences/?min="+str(min)+"&max="+str(max)+"&col=1&format=html&rnd=new"
    urlobj = urllib.urlopen("http://www.random.org/sequences/?min=1&max=4&col=1&format=html&rnd=new")
    text=urlobj.read()
    
    
    
