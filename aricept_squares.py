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
    myDlg.addField('Mode(demo/capacity):')
    myDlg.addField('t_stim(.1/.2):')
    myDlg.show()  #show dialog and wait for OK or Cancel
    if gui.OK:  #then the user pressed OK
        [name,day_num,mode,t_stim] = myDlg.data
    else: 
        print 'user cancelled'
        sys.exit()
    
    if mode.lower() not in ['demo','capacity']:
        print "Unacceptable mode type. Type demo, or capacity"
        sys.exit()
    else:
        mode=mode.lower()
    if day_num not in ['1','2','3']:
        print "Unacceptable day number. Type 1, 2, or 3"
        sys.exit()
    if t_stim not in ['.1','.2']:
        print "Unacceptable t_stim. Type .1 or .2"
        sys.exit()
    else:
        day_num = int(day_num)
        t_stim=float(t_stim)
     
     
    date = str(dt.date.today())
    day_path = 'data/'+name+'/day'+str(day_num)
    try:
        os.makedirs(day_path)
    except OSError:
        print 'directory '+day_path+' already exists'
    
    fname = day_path+'/'+mode+'_tstim_'+str(t_stim*1000)+'.txt'
    fn = 'data/'+name+'/maxK'+str(t_stim*1000)+'.txt'
    f_out = open(fname,'w')
    f_out.write('# subject: '+name+' \n# day: '+str(day_num)+' \n# mode: '+mode+' \n# t_stim: '+str(t_stim)+' \n')
    f_out.write('# date: '+date+' \n#\n# i_TRIAL, SSIZE, SOA_gap, CHANGE, ANSWER, ANSWER_TYPE, ANSWER_INT \n')
    
    if day_num == 1 and mode in ['capacity']:
        print 'making new capacity file'
        f_cap = open(fn,'w')
        f_cap.write('# subject: '+name+' \n# day: '+str(day_num)+' \n# mode: '+mode+' \n# t_stim: '+str(t_stim)+' \n')
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
        n_trials_per_block=40 #needs to be divisible by 4
        break_time = 80   #breaks after every 80 trials ~3min
    if mode == 'demo':
        n_trials_per_block=12   #needs to be divisible by 4
        break_time = 10000  #avoid all breaks in demo mode
    
    n = n_trials_per_block
    
    SOA_gap = [.025,.200]
    print 'using SOA gaps: '+str(SOA_gap)
    all_trials = []
    for ssize in SSizes:
        list_items = ['ssize','SOA_gap','change','answer','answer_type','answer_int']
        init_values = [ssize,.025,False,False,'', 0]
        trials0 = []
        for i in range(n):
                trials0.append(dict(zip(list_items,init_values)))
        half =  np.arange(0,n/2)
        fourth_1 = np.arange(0,n/4)
        fourth_2 = np.arange(n/4,2*n/4)
        fourth_3 = np.arange(2*n/4,3*n/4)
        fourth_4 = np.arange(3*n/4,4*n/4)

        
        for i in half:
            trials0[i]['SOA_gap'] = .2
        for i in fourth_1:
            trials0[i]['change']=True
        for i in fourth_2:
            trials0[i]['change']=False
        for i in fourth_3:
            trials0[i]['change']=True
        for i in fourth_4:
            trials0[i]['change']=False

        trials1=[]
        trials2=[]
        for i in range(n/2):
            trials1.append(trials0[i])
            trials2.append(trials0[i+n/2])
        #randomize trials within each SSize block:
        rand.shuffle(trials1)
        rand.shuffle(trials2)
        #add trials from this SSize block to the list of all trials
        all_trials=all_trials+trials1
        all_trials=all_trials+trials2
    
    n_tot = len(all_trials)
    
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
    message = '\n\nPress any key to continue'
    hit_sound = sound.Sound(value='G', secs=0.5, octave=4, sampleRate=44100, bits=16)
    miss_sound = sound.Sound(value='G', secs=0.5, octave=3, sampleRate=44100, bits=16)
    
    TextBlocks= ["Hello and thanks for participating! \n\n This is a visual working memory task in which you will be shown \
a set of colored squares. The number of squares will range from 1 square to 6 squares. Your task is \
to remember the color of a set of squares that will be shown to you very briefly. Following these squares, \
a set of multicolored squares will be shown to you. This 'mask' is presented as an experimental control, \
you do not need to remember any information about the 'mask' squares.",
                            "Following the 'mask' you will have a blank screen and then you will be shown another set of squares. \
This set will consist of the same number of squares you saw in the beginning and in the same locations. \
Your task is to decide if the colors are the same as the original set you saw. It is possible that one of the squares \
has changed color. It is also just as equally possible that none of the squares have changed color and \
it is the exact same set as the beginning.",
                            "If you decide that there has been no change, press the '1' key on the keyboard.\n\
If you decide that there has been a change, press the '2' key on the keyboard. ",
                            "After your response, you will hear a tone. \n A HIGH pitched tone means your answer was CORRECT.\n \
A LOW pitched tone means your answer was INCORRECT.",
                            "Typically people can remember 3 (+/- 1) squares. For many of the trials more squares will be on the screen \
than you can remember. In cases like this feel free to remember as much as you can (a subset of the squares) \
instead of attempting to remember all of them.",
                            "It is very important that you keep your eyes fixated in the center of the screen during the entire trial. \
Because the stimuli can appear in any location, and because they are presented for a very brief duration, \
keeping your gaze at the center of the screen may improve your performance.",
                            "You can rest your eyes in between trials before pressing the 1 or 2 key and of course during breaks. \
You are free to take breaks whenever you need by pausing before answering the trials as just mentioned \
and also at the predetermined break times. Feel free to come outside of the room, get fresh air, have some water, etc. \
If you do not want to take a break and would like to continue, just press the space bar. ",
                            ""]
                            
    for text_i in TextBlocks:
        #draw message and wait for key press, then flip the screen so it's empty
        text_to_draw = visual.TextStim(myWin,text = text_i+message)
        text_to_draw.draw()
        myWin.flip()
        event.waitKeys(maxWait=None)
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
            fix.draw()
            myWin.flip()
            core.wait(2)
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
        plot_em_up(all_trials,fname,-2)
    else:
        maxK = get_maxK(fn)
        if maxK==-1 or maxK==None:
           maxK = 2
        plot_em_up(all_trials, fname, maxK)


    




