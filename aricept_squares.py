from psychopy import visual, event, core, sound,gui
from math import sin, cos
import numpy as np
import  numpy.random as rand
import sys,os, datetime as dt
import random
import pylab as pl
from aricept_squares_util import *


if __name__=="__main__":
    
    #for subject testing on a dual-display system
#    myWin = visual.Window([1024,768], monitor='testMonitor', units='deg',color = 'gray',screen=1)   

    #for testing on a single-display system
    myWin = visual.Window([1024,768], monitor='testMonitor', units='deg',color = 'gray')   
    
    log = open('logfile.txt','w')
    #________________________________________________________________
    #      get subject info
    #________________________________________________________________
    
    myDlg = gui.Dlg(title="Aricept Squares")
    myDlg.addText('Please enter subject information')
    myDlg.addField('Subject ID:')
    myDlg.addField('Day(1/2/3):')
    myDlg.addField('Mode(demo/encoding/capacity):')
    myDlg.show()  #show dialog and wait for OK or Cancel
    if gui.OK:  #then the user pressed OK
        [name,day_num,mode] = myDlg.data
    else: 
        print 'user cancelled'
        sys.exit()
    
    if mode.lower() not in ['demo','capacity','encoding']:
        print "Unacceptable mode type. Type demo, encoding, or capacity"
        sys.exit()
    else:
        mode=mode.lower()
    if day_num not in ['1','2','3']:
        print "Unacceptable day number. Type 1, 2, or 3"
        sys.exit()
    else:
        day_num = int(day_num)
     
     
    date = str(dt.date.today())
    day_path = 'data/'+name+'/day'+str(day_num)
    try:
        os.makedirs(day_path)
    except OSError:
        print 'directory '+day_path+' already exists'
    
    fname = day_path+'/'+mode+'.txt'
    fn = 'data/'+name+'/maxK.txt'
    f_out = open(fname,'w')
    f_out.write('# subject: '+name+' \n# day: '+str(day_num)+' \n# mode: '+mode+' \n')
    f_out.write('# date: '+date+' \n#\n# i_TRIAL, SSIZE, SOA_gap, CHANGE, ANSWER, ANSWER_TYPE, ANSWER_INT \n')
    
    if day_num == 1 and mode in ['capacity']:
        print 'making new capacity file'
        f_cap = open(fn,'w')
        f_cap.write('# subject: '+name+' \n# day: '+str(day_num)+' \n# mode: '+mode+' \n')
        f_cap.write('# date: '+date+' \n#\n# Max Capacity \n')
        f_cap.close()
        run1ss = [1,2,3,4,5,6]
        run2ss = [1,2,3,4,5,6]
    elif mode in ['demo']:
        run1ss = [1,2,3]
        run2ss = [1,2,3]
    else:
        k = get_maxK(fn)
        print 'maxK',k
        if k == -1 or k==None:
            k=2
        run1ss = [k-1,k,k+1,k+2]
        run2ss = [k-1,k,k+1,k+2]
    
    #________________________________________________________________
    #      randomize set sizes
    #________________________________________________________________
    
    rand.shuffle(run1ss)
    rand.shuffle(run2ss)
    SSizes = run1ss+run2ss
    print >> log, 'run2ss',run2ss, 'run1ss',run1ss, 'SSizes', SSizes
    
    
    #________________________________________________________________
    #      make blocks
    #________________________________________________________________
    
    
    if mode == 'capacity':
        t_stim = .2
        n_trials_per_block=40 #needs to be divisible by 10
        break_time = 160   #breaks after every 133 trials ~ 5 min
    if mode == 'encoding':
        n_trials_per_block=160 #needs to be divisible by 10
        t_stim = .1
        break_time = 160   #breaks after every 133 trials ~ 5 min
    if mode == 'demo':
        n_trials_per_block=10   #needs to be divisible by 10
        t_stim = .2
        break_time = 10000  #avoid all breaks in demo mode
    
    n = n_trials_per_block
    
    SOA_gap = [.015, .025,.05,.075,.100]
    print 'using SOA gaps: '+str(SOA_gap)
    all_trials = []
    for ssize in SSizes:
        list_items = ['ssize','SOA_gap','change','answer','answer_type','answer_int']
        init_values = [ssize,.015,False,False,'', 0]
        trials0 = []
        for i in range(n):
                trials0.append(dict(zip(list_items,init_values)))
        half =  np.arange(0,n/2)
        tenth_1 = np.arange(0,n/10)
        tenth_2 = np.arange(n/10,2*n/10)
        tenth_3 = np.arange(2*n/10,3*n/10)
        tenth_4 = np.arange(3*n/8,4*n/10)
        tenth_5 = np.arange(4*n/10,5*n/10)
        tenth_6 = np.arange(5*n/10,6*n/10)
        tenth_7 = np.arange(6*n/10,7*n/10)
        tenth_8 = np.arange(7*n/10,8*n/10)
        tenth_9 = np.arange(8*n/10,9*n/10)
        tenth_10 = np.arange(9*n/10,10*n/10)
        
        for i in half:
            trials0[i]['change'] = True
        for i in tenth_1:
            trials0[i]['SOA_gap']=.015
        for i in tenth_2:
            trials0[i]['SOA_gap']=.025
        for i in tenth_3:
            trials0[i]['SOA_gap']=.05
        for i in tenth_4:
            trials0[i]['SOA_gap']=.075
        for i in tenth_5:
            trials0[i]['SOA_gap']=.1
        for i in tenth_6:
            trials0[i]['SOA_gap']=.015
        for i in tenth_7:
            trials0[i]['SOA_gap']=.025
        for i in tenth_8:
            trials0[i]['SOA_gap']=.05
        for i in tenth_9:
            trials0[i]['SOA_gap']=.075
        for i in tenth_10:
            trials0[i]['SOA_gap']=.1
            
        #randomize trials within each SSize block:
        rand.shuffle(trials0)
        #add trials from this SSize block to the list of all trials
        all_trials=all_trials+trials0
    
    n_tot = len(all_trials)
    
    if mode == 'capacity':
        for trial in all_trials:
            trial['SOA_gap'] = .2
    
    for i in range(n_tot):
        print >> log, all_trials[i]
    print >> log, 'n_tot:', n_tot
    
    #________________________________________________________________
    #     make stimulus
    #________________________________________________________________
    
    
    #define possible locations
    eccen = 6 #this can change, distance to fixation point
    polar = np.linspace(2,9,8)*np.pi/4
    polar += np.pi/8
    
    stims = []
    #place them in circle
    for i,pos in enumerate(polar):
        current_x = eccen * np.cos(pos)
        current_y = eccen * np.sin(pos)
        stims.append(visual.Rect(myWin, width = 1.0,fillColor = 'gray', lineColor = 'gray', height = 1.0, pos = (current_x,current_y)))
    colors = ['blue','red','green','yellow','black','white','coral','purple']
    
    #define other stimuli, fixation cross, message and feedback sounds
    fix = visual.TextStim(myWin,text = '+',height = 1.0,color = -1)
    message = visual.TextStim(myWin,text = 'Press the space bar to begin')
    hit_sound = sound.Sound(value='G', secs=0.5, octave=4, sampleRate=44100, bits=16)
    miss_sound = sound.Sound(value='G', secs=0.5, octave=3, sampleRate=44100, bits=16)
    
    #draw message and wait for key press, then flip the screen so it's empty
    message.draw()
    myWin.flip()
    event.waitKeys(maxWait=None, keyList='space')
    fix.draw()
    myWin.flip()
    
    #give subjects a second to settle in
    core.wait(1.0)
    
    
    #________________________________________________________________
    #    start trials
    #________________________________________________________________
    
    
    #for trials in randomizer:
    for trials in range(n_tot):
        if ((trials+1) % break_time) == 0:
            message = visual.TextStim(myWin,text = 'Take a break!\n Then, press the space bar to continue')
            message.draw()
            myWin.flip()
            event.waitKeys(maxWait=None, keyList='space')
            core.wait(2)
            fix.draw()
            myWin.flip()
        #Memory Sample, color gray squares depending upon set size, and display for 100 ms
        rand.shuffle(colors)
        rand.shuffle(stims)

        for squares in range(all_trials[trials]['ssize']):
            stims[squares].setFillColor(colors[squares])
    
        for thisStim in stims:
            thisStim.draw()
        fix.draw()
        myWin.flip()
        core.wait(t_stim)
    
        #Memory Delay, flip screen to hide stimuli and decide if there is a change (random number is greater than 0.5, there is a change)
        fix.draw()
        myWin.flip()
        if all_trials[trials]['change'] == True:
            stims[0].setFillColor(colors[7])
       
       #ENCODING TIME
        core.wait(all_trials[trials]['SOA_gap'])
            
        #Mask here, currently using the mask made in Vogel 2006 paper
        for thisStim in stims[0:all_trials[trials]['ssize']]:
            [stim_x,stim_y]=thisStim.pos
            mask_colors = random.sample(range(8),4)
            mask1= visual.Rect(myWin, width = .5,fillColor = colors[mask_colors[0]], lineColor = 'gray', height = .5, pos = (stim_x-.25,stim_y-.25))
            mask1.draw()
            mask2= visual.Rect(myWin, width = .5,fillColor = colors[mask_colors[1]], lineColor = 'gray', height = .5, pos = (stim_x+.25,stim_y-.25))
            mask2.draw()
            mask3= visual.Rect(myWin, width = .5,fillColor = colors[mask_colors[2]], lineColor = 'gray', height = .5, pos = (stim_x-.25,stim_y+.25))
            mask3.draw()
            mask4= visual.Rect(myWin, width = .5,fillColor = colors[mask_colors[3]], lineColor = 'gray', height = .5, pos = (stim_x+.25,stim_y+.25))
            mask4.draw()
            
        fix.draw()
        myWin.flip()
        #Show mask for 500ms
        core.wait(.5)
        #Now hide the mask and wait the remainder of the 1000ms before showing the stimulus again
        fix.draw()
        myWin.flip()
        core.wait(.5 - t_stim - all_trials[trials]['SOA_gap'])
    
        #Memory Probe, present for 1 seconds or until key press. If no key press, flip screen and wait for key press
        for thisStim in stims:
            thisStim.draw()
        fix.draw()
        myWin.flip()
        key = event.waitKeys(maxWait=1.0, keyList=['1','2','q','num_1','num_2'])
        if key != None:
            if key[0] =='2' or key[0] == 'num_2':
                all_trials[trials]['answer'] = True
            elif key[0]=='q':
                break
            elif key[0] =='1' or key[0] == 'num_1':
                all_trials[trials]['answer'] = False
    
        fix.draw()
        myWin.flip()
        if key == None:
            key = event.waitKeys(maxWait=None, keyList=['1','2','q','num_1','num_2'])
            if key[0] =='2' or key[0] == 'num_2':
                all_trials[trials]['answer'] = True
            elif key[0]=='q':
                break
            elif key[0] =='1' or key[0] == 'num_1':
                all_trials[trials]['answer'] = False
    
        #set color back to gray, play feedback, and wait 0.5 seconds
        for thisStim in stims:
            thisStim.setFillColor('gray')
        key = []
        if all_trials[trials]['answer'] == all_trials[trials]['change']:
            hit_sound.play()
        else:
            miss_sound.play()
        core.wait(1)
        
        #categorize their answer
        if all_trials[trials]['change']== True:
            if all_trials[trials]['answer']== True:
                all_trials[trials]['answer_type']='hit'
                all_trials[trials]['answer_int']=1
            if all_trials[trials]['answer']== False:
                all_trials[trials]['answer_type']='miss'
                all_trials[trials]['answer_int']=2
        if all_trials[trials]['change']== False:
            if all_trials[trials]['answer']== True:
                all_trials[trials]['answer_type']='false_alarm'
                all_trials[trials]['answer_int']=3
            if all_trials[trials]['answer']== False:
                all_trials[trials]['answer_type']='correct_reject'
                all_trials[trials]['answer_int']=4
        
        #write trial to file
        f_out.write(str(trials)+'\t'+str(all_trials[trials]['ssize'])+ '\t' 
            +str(all_trials[trials]['SOA_gap'])+ '\t' + str(all_trials[trials]['change']) 
            + '\t' +str(all_trials[trials]['answer'])+'\t'+str(all_trials[trials]['answer_type'])
            +'\t'+str(all_trials[trials]['answer_int'])+'\t\n')
            
    log.close()
    f_out.close()
    myWin.close()
    if day_num == 1 and mode in ['capacity']:
        maxK = calc_maxK(all_trials,fn)
        print "subject has a maxK of :",maxK
        
    else:
        maxK = get_maxK(fn)
        if maxK==-1 or maxK==None:
           maxK = 2
        plot_em_up(all_trials, fname, maxK)


    




