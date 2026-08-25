from __future__ import annotations
import math
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import k0

PI=math.pi; EG=0.5772156649015329; CA=3.0

def Cb(b: float, ratio: float=math.sqrt(2.0)) -> float:
    z=max(float(b)*ratio,1e-300)
    if z<1e-4:
        L=EG+math.log(z/2.0)
        val=z*z/4.0*(1.0-L)+z**4/64.0*(1.5-L)
    else:
        val=float(k0(z))+EG+math.log(z/2.0)
    return val/(2.0*PI)

def ccoeff(C1,C2,C3):
    return ((C2+C3-C1)/CA,(C3+C1-C2)/CA,(C1+C2-C3)/CA)

@dataclass(frozen=True)
class Res:
    mu2: float
    C: complex
    B: complex
    Bexp: float

@lru_cache(maxsize=20000)
def _solve(eta,x,mhat,c1,c2,c3,ratio):
    eta=float(eta);x=float(x);mhat=float(mhat);c1=float(c1);c2=float(c2);c3=float(c3);ratio=float(ratio)
    bmin=2e-6
    bmax=min(180.0,max(6.5,16.0/eta**0.25))
    def V(b): return c1*Cb(b,ratio)+c2*Cb(x*b,ratio)+c3*Cb((1-x)*b,ratio)
    def rhs(b,y):
        f=y[0]+1j*y[1]; fp=y[2]+1j*y[3]
        fpp=-3*fp/b+(mhat-1j*eta*V(b))*f
        return (fp.real,fp.imag,fpp.real,fpp.imag)
    K=np.sqrt(mhat-1j*eta*V(bmax)+0j)
    if K.real<0:K=-K
    fp=(-K-1.5/bmax)
    grid=np.geomspace(bmax,bmin,360)
    sol=solve_ivp(rhs,(bmax,bmin),(1,0,fp.real,fp.imag),t_eval=grid,method='DOP853',rtol=1e-7,atol=2e-9)
    if not sol.success: raise RuntimeError(sol.message)
    b=sol.t[::-1]; f=(sol.y[0]+1j*sol.y[1])[::-1]
    mask=b<min(0.03,bmax/60)
    bb=b[mask]; ff=f[mask]
    X=np.column_stack((np.ones_like(bb),bb**2*np.log(bb),bb**2,bb**4*np.log(bb),bb**4))
    sc=np.linalg.norm(X,axis=0); Xs=X/sc
    coeff=(np.linalg.lstsq(Xs,(ff*bb**2).real,rcond=None)[0]+1j*np.linalg.lstsq(Xs,(ff*bb**2).imag,rcond=None)[0])/sc
    coeff*= (1/PI)/coeff[0]
    mu=math.sqrt(2)*4*PI*coeff[2].imag
    return Res(max(mu,0.0),coeff[2],coeff[1],mhat/(2*PI))

def solve(eta,x,mhat,cs,ratio=math.sqrt(2.0)):
    q=lambda z:float(f'{z:.10g}')
    return _solve(q(eta),q(x),q(mhat),q(cs[0]),q(cs[1]),q(cs[2]),q(ratio))
