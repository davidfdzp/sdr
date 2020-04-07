# File: ptfun.py
import numpy as np
# sps = Fs/Fb
# Assuming Fs = sps, Fb = 1
def pampt(sps, ptype, pparms=[]):
    ptype=ptype.lower()
    if ptype == 'rect':
        nn = np.arange(sps)
        pt = np.ones(len(nn))
    elif ptype == 'man':
        nn = np.arange(sps) - sps/2
        ttp = nn/float(sps)
        pt = -np.ones(len(nn))
        ixp = np.where(ttp >= 0)
        pt[ixp]=1
    elif ptype == 'msin':
        nn = np.arange(sps) - sps/2
        ttp = nn/float(sps)
        pt = np.sin(2*np.pi*ttp)
    elif ptype == 'tri':
        nn=np.arange(-sps,sps)
        pt=1+nn/float(sps)
        ix=np.where(nn>=0)[0]
        pt[ix]=1-nn[ix]/float(sps)
    elif ptype == 'sinc':
        k=5# default k
        if len(pparms)>0:
            k=pparms[0]
            nn=np.arange(-k*sps,k*sps)
            pt=np.sinc(nn/float(sps))
            if len(pparms)>1:
                pt=pt*np.kaiser(len(pt),pparms[1])
    elif ptype == 'rcf':
        nk = round(pparms[0]*sps)
        nn = np.arange(-nk, nk)
        pt = np.sinc(nn/float(sps))
        if len(pparms) > 1:
            p2t = 0.25*np.pi*np.ones(len(nn))
            atFB = pparms[1]/float(sps)*nn
            atFB2 = np.power(2*atFB,2.0)
            ix = np.where(atFB2 != 1)[0]
            p2t[ix] = np.cos(np.pi*atFB[ix])
            p2t[ix] = p2t[ix]/(1-atFB2[ix])
            pt = pt*p2t
    # http://ecee.colorado.edu/~mathys/ecen4242/classnotes/python/PAM_006.pdf
    elif(ptype=='rrcf'): # Root raised cosine in freq
        nk = round(pparms[0]*sps)
        nn = np.arange(-nk, nk)
        ttp = nn/float(sps)
        alfa=pparms[1] # Rolloff parameter
        falf=4*alfa
        pt=(1-alfa+4*alfa/np.pi)*np.ones(len(ttp))
        ix=np.where(np.logical_and(ttp!=0,np.power(falf*ttp,2.0)!=1.0))[0]
        pt[ix]=np.sin((1-alfa)*np.pi*ttp[ix])
        pt[ix]=pt[ix]+falf*ttp[ix]*np.cos((1+alfa)*np.pi*ttp[ix])
        pt[ix]=1.0/(np.pi)*pt[ix]/((1-np.power(falf*ttp[ix],2.0))*ttp[ix])
        ix=np.where(np.power(falf*ttp,2.0)==1.0)[0]
        pt[ix]=(1+2/np.pi)*np.sin(np.pi/(4*alfa))+(1-2/np.pi)*np.cos(np.pi/(4*alfa))
        pt[ix]=alfa/np.sqrt(2.0)*pt[ix]
    # elif ptype == 'man' # Manchester pulse
    # elif ptype == 'msin'# Manchester sin pulse
    else:
        pt = np.ones(1) # default value
    return pt
    
def pamhRt(sps, ptype, pparms=[]):
    pt = pampt(sps, ptype, pparms)
    hRt = pt[::-1] # h_R(t) = p(-t)
    hRt = 1.0/sum(np.power(pt,2.0))*hRt
    return hRt
    
def pam_pt(FB,Fs,ptype,pparms=[]):
    """    Generate PAM pulse p(t)
    >>>>> ttp, pt = pam_pt(FB, Fs, ptype, pparms) <<<<<
    where  ttp:   time axis for p(t)
    pt:    PAM pulse p(t)
    FB:    Baud rate  (Fs/FB=sps)
    Fs:    sampling rate of p(t)
    ptype: pulse type from list
    ('man', 'msin', rcf', 'rect', 'rrcf', 'sinc', 'tri')
    pparms not used for 'rect','tri'
    pparms = [k, alfa]  for 'rcf'
    pparms = [k, beta]  for 'sinc'
    k:     "tail" truncation parameter for 'sinc'
    (truncates p(t) to -k*TB <= t < k*TB)
    beta:  Kaiser window parameter for 'sinc'
    alfa: Rolloff parameter for 'rcf', 0<alfa<=1
    """
    ptyp=ptype.lower()
    if(ptyp=='rect' or ptyp=='man' or ptyp=='msin'):
        kR=0.5; kL=-kR
    elif ptyp=='tri':
        kR=1.0; kL=-kR
    elif (ptyp=='rcf' or ptyp=='rrcf' or ptyp=='sinc'):
        kR=pparms[0]; kL=-kR
    else:
        kR=0.5; kL=-kR
    tpL, tpR = kL/float(FB), kR/float(FB)
    ixpL, ixpR = int(np.ceil(tpL*Fs)), int(np.ceil(tpR*Fs))
    ttp = np.arange(ixpL,ixpR)/float(Fs) # time axis for p(t)
    pt=np.zeros(ttp.size)
    if ptyp =='man':
        pt=-np.ones(ttp.size)
        ixp=np.where(ttp>=0)
        pt[ixp]=1
    elif ptyp=='msin':
        pt=np.sin(2*np.pi*FB*ttp)
    elif ptyp=='rcf':
        pt=np.sinc(FB*ttp)
        if pparms[1]!=0:
            p2t=np.pi/4.0*np.ones(ttp.size)
            ix=np.where(np.power(2*pparms[1]*FB*ttp,2.0)!=1)[0]
            p2t[ix]=np.cos(np.pi*pparms[1]*FB*ttp[ix])
            p2t[ix]=p2t[ix]/(1-np.power(2*pparms[1]*FB*ttp[ix],2.0))
            pt=pt*p2t
    elif ptyp=='rect':
        ixp=np.where(np.logical_and(ttp>=tpL,ttp<tpR))[0]
        pt[ixp]=1 # rectangular pulse p(t)
    elif(ptype=='rrcf'): # Root raised cosine in freq
        alfa=pparms[1] # Rolloff parameter
        falf=4*alfa*FB
        pt=(1-alfa+4*alfa/np.pi)*np.ones(len(ttp))
        ix=np.where(np.logical_and(ttp!=0,np.power(falf*ttp,2.0)!=1.0))[0]
        pt[ix]=np.sin((1-alfa)*np.pi*FB*ttp[ix])
        pt[ix]=pt[ix]+falf*ttp[ix]*np.cos((1+alfa)*np.pi*FB*ttp[ix])
        pt[ix]=1.0/(FB*np.pi)*pt[ix]/((1-np.power(falf*ttp[ix],2.0))*ttp[ix])
        ix=np.where(np.power(falf*ttp,2.0)==1.0)[0]
        pt[ix]=(1+2/np.pi)*np.sin(np.pi/(4*alfa))+(1-2/np.pi)*np.cos(np.pi/(4*alfa))
        pt[ix]=alfa/np.sqrt(2.0)*pt[ix]
    elif ptyp=='sinc':
        pt=np.sinc(FB*ttp)
        if len(pparms)>1: # Apply Kaiser window 
            pt=pt*np.kaiser(len(pt),pparms[1])
    else:
        pt = np.ones(1) # default value
    return pt

# From: http://ecee.colorado.edu/~mathys/ecen4242/classnotes/python/PAM_007.pdf
def eyediagram(tt, rt, FB, dispparms=[]):
    """
    Generate waveform array for eye diagram of digital PAM signal r(t)
    >>>>> ttA, A = eyediagram(tt, rt, FB, dispparms) <<<<<    
    where  tt:  time axis for rt           
    rt:  received PAM signal r(t)=sum_n a_n*q(t-nTB)           
    FB:  Baud rate of DT sequence a_n, TB = 1/FB           
    dispparms = [NTd, delay, width, step]           
    NTd:    Number of traces to display           
    delay:  trigger delay (in TB units, e.g., 0.5)           
    width:  display width (in TB units, e.g., 3)           
    step:   step size from trace to trace (in TB units)           
    ttA: time axis (in TB) for eye diagram display           
    A:   array of eye diagram traces    """
    # Parameters
    if type(dispparms)==int:
        dispparms=[dispparms]
    if len(dispparms)==0:
        dispparms=[50] # default # of traces
    if len(dispparms)==1:
        dispparms=np.hstack((dispparms,0)) # default delay
    if len(dispparms)==2:
        dispparms=np.hstack((dispparms,3)) # default width
    if len(dispparms)==3:
        dispparms=np.hstack((dispparms,1)) # default step
    # Setup
    Fs=(len(tt)-1)/(tt[-1]-tt[0])
    NTd=int(dispparms[0]) # Number of traces
    t0=dispparms[1]/float(FB) # Delay in sec
    if t0 < tt[0]:
        t0 = tt[0]
    tw=dispparms[2]/float(FB) # Display width in sec
    tstep=dispparms[3]/float(FB) # Step size in sec
    tend=t0 + NTd*tstep + tw # End time
    if tend > tt[-1]:
        NTd=int(np.floor((tt[-1]-t0-tw)/tstep))
    ixw=int(round(tw*Fs)) # samples per width
    A=np.zeros((NTd,ixw)) # Array for traces
    ix0=np.argmin(np.abs(tt)) # index of t=0
    ixd0=ix0+int(round(t0*Fs))
    for i in range(NTd):
        ixi = ixd0+int(round(i*tstep*Fs))
        A[i,:]=rt[ixi:ixi+ixw]
    ttA=FB*np.arange(ixw)/float(Fs)
    return ttA,A