from __future__ import annotations
import math
from dataclasses import dataclass
import numpy as np
from numpy.polynomial.legendre import leggauss
PI=math.pi; NC=3.;CA=3.;CF=4/3;DA=8.;DF=3.;NU_G=16.;NU_Q=6.

def bose(x): return 1.0/np.expm1(np.clip(x,1e-12,700))
def fermi(x): return 1.0/(np.exp(np.clip(x,-700,700))+1.0)

def thermal(alpha,nf=7):
 g2=4*PI*alpha; md2=g2*(NC/3+nf/6); return g2,md2,.5*md2,CF*g2/4

def m2(ch,s,t,u,alpha,mg2,mq2):
 g2=4*PI*alpha;g4=g2*g2;ag=math.exp(5/3)/4*mg2;aq=math.e**2/4*mq2
 if ch=='gg':
  v=g4*(16*DA*CA**2/NU_G**2)*(3-s*u/(t-ag)**2-s*t/(u-ag)**2-t*u/(s+ag)**2)
 elif ch=='gq':
  v=g4*((-8*DF*CF**2/(NU_G*NU_Q))*(s*s+u*u)/((s+aq)*(u-aq))+(8*DF*CF*CA/(NU_G*NU_Q))*(s*s+u*u)/(t-ag)**2)
 elif ch=='qq':
  v=g4*(8*DF**2*CF**2/DA/NU_Q**2)*(s*s+u*u)/(t-ag)**2
 elif ch=='ann':
  v=g4*((8*DF*CF**2/NU_Q**2)*(u*u+t*t)/((t-aq)*(u-aq))-(8*DF*CF*CA/NU_Q**2)*(t*t+u*u)/(s+ag)**2)
 elif ch=='pair':
  v=g4*((8*DF*CF**2/NU_G**2)*(u*u+t*t)/((t-aq)*(u-aq))-(8*DF*CF*CA/NU_G**2)*(t*t+u*u)/(s+ag)**2)
 else: raise KeyError
 return max(float(v),0.)

def boost(E,v,beta,inv=False):
 b2=float(beta@beta)
 if b2<1e-18:return E,v.copy()
 gam=1/math.sqrt(1-b2);bp=float(beta@v)
 if inv:
  return gam*(E-bp),v+(((gam-1)*bp/b2)-gam*E)*beta
 return gam*(E+bp),v+(((gam-1)*bp/b2)+gam*E)*beta

@dataclass(frozen=True)
class Ch:
 mname:str;targetF:bool;cF:bool;dF:bool;gt:float;mult:float=1.;sym:float=1.

def rate(ch:Ch,alpha,p=3,nf=7,nk=16,nrel=12,nth=20,nphi=6):
 _,_,mg2,mq2=thermal(alpha,nf)
 xk,wk=leggauss(nk);ks=.5*(xk+1)*22;wks=.5*22*wk
 mus,wm=leggauss(nrel);cts,wt=leggauss(nth);phis=2*PI*np.arange(nphi)/nphi
 pvec=np.array([0.,0.,p]); total=0.;classic=0.
 for k,wki in zip(ks,wks):
  fb=float(fermi(k) if ch.targetF else bose(k))
  for mu,wmi in zip(mus,wm):
   s=2*p*k*(1-mu)
   if s<1e-12:continue
   kv=np.array([k*math.sqrt(max(1-mu*mu,0)),0,k*mu]);beta=(pvec+kv)/(p+k)
   _,ps=boost(p,pvec,beta,True);e3=ps/np.linalg.norm(ps);e2=np.array([0.,1.,0.]);e1=np.cross(e2,e3);e1/=np.linalg.norm(e1)
   Est=math.sqrt(s)/2; ang=0.;ang0=0.
   for ct,wti in zip(cts,wt):
    t=-.5*s*(1-ct);u=-s-t;M=m2(ch.mname,s,t,u,alpha,mg2,mq2);ds=M/(32*PI*s*ch.sym)
    st=math.sqrt(max(1-ct*ct,0));qfac=0.
    for ph in phis:
     cv=Est*(st*math.cos(ph)*e1+st*math.sin(ph)*e2+ct*e3)
     Ec,_=boost(Est,cv,beta,False);Ed,_=boost(Est,-cv,beta,False)
     fc=float(fermi(Ec) if ch.cF else bose(Ec));fd=float(fermi(Ed) if ch.dF else bose(Ed))
     qfac+=(1-fc if ch.cF else 1+fc)*(1-fd if ch.dF else 1+fd)
    qfac/=nphi;tw=1-ct
    ang+=wti*ds*tw*qfac;ang0+=wti*ds*tw
   phw=wki*k*k/(2*PI**2)*.5*wmi*fb*(1-mu)
   total+=phw*ang;classic+=phw*ang0
 mult=ch.gt*ch.mult
 return mult*total,mult*classic

def bundle(alpha,nf=7):
 cs={
 'g_gg':Ch('gg',False,False,False,NU_G,1,2),
 'g_gq':Ch('gq',True,False,True,2*nf*NU_Q),
 'g_pair':Ch('pair',False,True,True,NU_G,nf),
 'q_qg':Ch('gq',False,True,False,NU_G),
 'q_qq':Ch('qq',True,True,True,(2*nf-1)*NU_Q),
 'q_ann':Ch('ann',True,False,False,NU_Q,1,2),
 }
 o={}
 for n,c in cs.items():o[n],o[n+'_classical']=rate(c,alpha,nf=nf)
 o['g_total']=o['g_gg']+o['g_gq']+o['g_pair'];o['q_total']=o['q_qg']+o['q_qq']+o['q_ann']
 return o
