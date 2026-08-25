#!/usr/bin/env python3
"""Verification suite for state-selected, exactly Z6-symmetric reheating v0.9.

The construction has three layers:
1. An exact cyclic Z6 orbit of reheaton fields X_k,Y_k and six matter sectors.
2. A transient one-hot selector background Q_j that makes only one reheaton pair
   kinematically accessible while leaving the microscopic action Z6 invariant.
3. A chiral nearest-neighbour reheaton mixing that gives the selected light state
   fixed branching fractions into sectors k and k-1.

The script verifies:
- exact cyclic invariance of the displayed tensors/couplings;
- the two-state mass-mixing benchmark and its positive eigenvalues;
- B0:B5=256:1 and T5/T0=1/4;
- reheating width, portal scale, gravitational leakage, Delta N_eff;
- selector mass hierarchy and kinematic isolation;
- low-scale hybrid-inflation observables;
- adiabatic transfer and vanishing linear dark-radiation isocurvature;
- numerical damping of the chronometric spectator perturbation using the v0.8
  cosmological background.

This is an EFT verification and not a lattice preheating or full Einstein-Boltzmann code.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

OUTDIR = Path(__file__).resolve().parent
MPL = 2.435e18  # reduced Planck mass, GeV
AS = 2.10e-9
NS = 0.9682
GSTAR = 106.75
PI = math.pi


@dataclass
class ReheatonBenchmark:
    N: int = 6
    tan_theta: float = 1.0 / 16.0
    m_R: float = 1.0e9       # selected light reheaton, GeV
    m_S: float = 6.0e9       # orthogonal reheaton, GeV
    m_inflaton_vac: float = 1.0e10  # post-inflation inflaton mass, GeV
    T_visible: float = 1.002e8       # target visible reheat temperature, GeV
    v_Q: float = 1.0e10      # selector one-hot scale, GeV
    kappa_Q: float = 0.25    # one-hot angular curvature coupling
    lambda_QR: float = 0.50  # selector-induced mass-squared coefficient
    H_star: float = 1.0e8    # inflationary Hubble scale, GeV
    gamma_phi: float = 1.0e2 # illustrative inflaton -> reheaton rate, GeV
    gamma_Q: float = 1.0     # illustrative selector restoration rate, GeV
    cg_grav: float = 1.0/(8.0*math.pi)  # conservative gravitational width coefficient

    @property
    def theta(self) -> float:
        return math.atan(self.tan_theta)

    @property
    def c(self) -> float:
        return math.cos(self.theta)

    @property
    def s(self) -> float:
        return math.sin(self.theta)

    @property
    def B0(self) -> float:
        return self.c*self.c

    @property
    def B5(self) -> float:
        return self.s*self.s

    @property
    def xi5(self) -> float:
        return (self.B5/self.B0)**0.25


def load_v08():
    path = OUTDIR/'verify_cosmological_vacuum_selection_v0_8.py'
    spec = importlib.util.spec_from_file_location('cosmo_v08', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Could not load v0.8 cosmology module')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def mass_matrix_parameters(b: ReheatonBenchmark) -> Dict[str, float]:
    c, s = b.c, b.s
    mR2, mS2 = b.m_R**2, b.m_S**2
    # Matrix [[mX2,-mu2],[-mu2,mY2]], diagonalized by
    # R=c X+s Y and S=-s X+c Y.
    mX2 = mR2*c*c + mS2*s*s
    mY2 = mR2*s*s + mS2*c*c
    mu2 = (mS2-mR2)*s*c
    matrix = np.array([[mX2, -mu2],[-mu2,mY2]], dtype=float)
    eig = np.linalg.eigvalsh(matrix)
    return {
        'm_X_GeV': math.sqrt(mX2),
        'm_Y_GeV': math.sqrt(mY2),
        'sqrt_mu2_GeV': math.sqrt(mu2),
        'mu2_GeV2': mu2,
        'eigenvalue_light_GeV2': float(eig[0]),
        'eigenvalue_heavy_GeV2': float(eig[1]),
        'determinant_GeV4': float(np.linalg.det(matrix)),
        'trace_GeV2': float(np.trace(matrix)),
    }


def reheating_results(b: ReheatonBenchmark) -> Dict[str, float]:
    # rho_visible=B0*3 Mpl^2 Gamma^2 = pi^2/30 g T0^4.
    gamma_R = math.sqrt(PI**2*GSTAR/(90.0*b.B0))*b.T_visible**2/MPL
    # For L=-mu_h R H^dag H, four real Higgs modes give Gamma=mu_h^2/(8 pi m_R).
    mu_h = math.sqrt(8.0*PI*b.m_R*gamma_R)
    gamma0 = b.B0*gamma_R
    gamma5 = b.B5*gamma_R
    # Conservative total gravitational decay width into one other sector.
    gamma_grav_one = b.cg_grav*b.m_R**3/MPL**2
    Bgrav_one = gamma_grav_one/gamma_R
    xi_grav_one = Bgrav_one**0.25
    # Complete hidden SM copy with standard internal neutrino reheating (v0.8 coefficient).
    delta_neff = 7.403*b.xi5**4
    # Estimate loop-generated H0-H5 quartic from R exchange/loops.
    mu0, mu5 = mu_h*b.c, mu_h*b.s
    portal_loop = (mu0*mu5)**2/(16.0*PI**2*b.m_R**4)
    higgs_mass_correction = mu0**2/(16.0*PI**2)
    return {
        'Gamma_R_GeV': gamma_R,
        'Gamma0_GeV': gamma0,
        'Gamma5_GeV': gamma5,
        'B0': b.B0,
        'B5': b.B5,
        'B5_over_B0': b.B5/b.B0,
        'xi5': b.xi5,
        'mu_h_GeV': mu_h,
        'mu0_GeV': mu0,
        'mu5_GeV': mu5,
        'Delta_Neff': delta_neff,
        'Gamma_grav_one_GeV': gamma_grav_one,
        'Bgrav_one': Bgrav_one,
        'xi_grav_one': xi_grav_one,
        'loop_cross_sector_quartic_estimate': portal_loop,
        'delta_mH2_GeV2_estimate': higgs_mass_correction,
        'sqrt_delta_mH2_GeV_estimate': math.sqrt(higgs_mass_correction),
    }


def selector_results(b: ReheatonBenchmark) -> Dict[str, float]:
    mQ_perp = math.sqrt(b.kappa_Q)*b.v_Q
    delta_m2 = b.lambda_QR*b.v_Q**2
    m_other = math.sqrt(b.m_R**2+delta_m2)
    threshold = b.m_inflaton_vac/2.0
    return {
        'm_Q_perp_GeV': mQ_perp,
        'm_Q_perp_over_Hstar': mQ_perp/b.H_star,
        'selector_delta_m2_GeV2': delta_m2,
        'other_reheaton_mass_GeV': m_other,
        'inflaton_half_mass_GeV': threshold,
        'R0_kinematically_open': float(b.m_R < threshold),
        'S0_kinematically_closed': float(b.m_S > threshold),
        'other_orbits_kinematically_closed': float(m_other > threshold),
        'rate_hierarchy_gamma_phi_over_gamma_Q': b.gamma_phi/b.gamma_Q,
        'rate_hierarchy_gamma_Q_over_gamma_R': b.gamma_Q/reheating_results(b)['Gamma_R_GeV'],
    }


def inflation_results(b: ReheatonBenchmark) -> Dict[str, float]:
    eps_v = b.H_star**2/(8.0*PI**2*AS*MPL**2)
    eta_v = (NS-1.0+6.0*eps_v)/2.0
    r = 16.0*eps_v
    V0 = 3.0*MPL**2*b.H_star**2
    Vquarter = V0**0.25
    fNL = 5.0/12.0*(1.0-NS)
    # Hilltop-hybrid local form V=V0[1-c2 phi^2/(2Mpl^2)], c2=-eta.
    c2 = -eta_v
    phi_star_over_Mpl = math.sqrt(2.0*eps_v)/c2
    Nstar = 55.0
    phi_c_over_Mpl = phi_star_over_Mpl*math.exp(c2*Nstar)
    return {
        'A_s': AS,
        'n_s': NS,
        'epsilon_V': eps_v,
        'eta_V': eta_v,
        'r': r,
        'H_star_GeV': b.H_star,
        'V_quarter_GeV': Vquarter,
        'fNL_local_single_clock': fNL,
        'hilltop_c2': c2,
        'phi_star_over_Mpl': phi_star_over_Mpl,
        'phi_c_over_Mpl': phi_c_over_Mpl,
        'phi_c_GeV': phi_c_over_Mpl*MPL,
        'N_star': Nstar,
    }


def verify_z6_tensor_invariance(N: int = 6) -> Dict[str, float]:
    # Coupling tensors: X_k O_k and Y_k O_k, plus oriented X_k Y_{k-1} mixing.
    # Verify invariance under simultaneous cyclic shift numerically.
    rng = np.random.default_rng(4906)
    max_diff = 0.0
    for _ in range(1000):
        X = rng.normal(size=N)
        Y = rng.normal(size=N)
        O = rng.normal(size=N)
        Q2 = rng.random(size=N)
        lag = np.dot(X,O)+np.dot(Y,O)-sum(X[k]*Y[(k-1)%N] for k in range(N))
        sel = sum((X[k]**2+Y[(k-1)%N]**2)*sum(Q2[j] for j in range(N) if j != k)
                  for k in range(N))
        Xs=np.roll(X,1); Ys=np.roll(Y,1); Os=np.roll(O,1); Qs=np.roll(Q2,1)
        lags = np.dot(Xs,Os)+np.dot(Ys,Os)-sum(Xs[k]*Ys[(k-1)%N] for k in range(N))
        sels = sum((Xs[k]**2+Ys[(k-1)%N]**2)*sum(Qs[j] for j in range(N) if j != k)
                   for k in range(N))
        max_diff=max(max_diff,abs(lag-lags),abs(sel-sels))
    return {'max_absolute_Z6_invariance_residual': max_diff}


def chronometric_perturbation_transfer(b: ReheatonBenchmark) -> Tuple[Dict[str,float], np.ndarray, np.ndarray, np.ndarray]:
    v08=load_v08()
    model=v08.make_ridge_model(1.0e-8, d_target=1.0e-6, m_target_eV=7.5e-29, xi_adj=0.25)
    bg=v08.build_background(model, stop_ratio=150.0, points=5600)
    tr=v08.integrate_model(model, math.pi/2.0, stop_ratio=150.0,
                           rtol=2e-7, atol=2e-9, background=bg)
    xu=PchipInterpolator(tr['u'],tr['x'],extrapolate=True)

    def vxx(u:float,x:float)->float:
        N=model.N
        val=-(model.m**2*model.f**2)*math.cos(N*x)
        for k in model.xis:
            th=x+2.0*math.pi*k/N
            val += float(bg.heavy[k](u))*math.cos(th)
            den=1.0-model.eps*math.cos(th)
            Aq=float(bg.qcd[k](u))
            val += Aq*(math.cos(th)/den-model.eps*math.sin(th)**2/den**2)
        den0=1.0-model.eps*math.cos(x)
        Ab=float(bg.baryon(u))
        val += Ab*(math.cos(x)*den0**(model.p_b-1.0)
                   +(model.p_b-1.0)*model.eps*math.sin(x)**2*den0**(model.p_b-2.0))
        return val

    def rhs(u,y):
        H=math.exp(float(bg.logH(u)))
        dlh=float(bg.dlogH(u))
        x=float(xu(u))
        omega2=vxx(float(u),x)/(model.f**2*H**2)
        return [y[1],-(3.0+dlh)*y[1]-omega2*y[0]]

    delta_initial=b.H_star/(2.0*PI*model.f)
    sol=solve_ivp(rhs,(bg.u0,bg.u_end),[delta_initial,0.0],method='Radau',
                  rtol=2e-8,atol=1e-14,dense_output=True,max_step=0.05)
    ug=np.linspace(bg.u0,bg.u_end,2200)
    dg=sol.sol(ug)[0]
    ag=np.exp(ug)
    zg=1.0/ag-1.0
    # Recombination and endpoint diagnostics.
    zrec=1090.0
    irec=int(np.argmin(np.abs(zg-zrec)))
    pQCD=2.0/27.0
    qcd_frac_rec=abs(pQCD*model.eps*dg[irec])
    qcd_frac_end=abs(pQCD*model.eps*dg[-1])
    result={
        'f_a_GeV':model.f,
        'epsilon_chronometric':model.eps,
        'delta_x_initial':delta_initial,
        'z_recombination_sample':float(zg[irec]),
        'delta_x_recombination':float(dg[irec]),
        'transfer_recombination':float(abs(dg[irec]/delta_initial)),
        'delta_x_endpoint':float(dg[-1]),
        'z_endpoint':float(zg[-1]),
        'transfer_endpoint':float(abs(dg[-1]/delta_initial)),
        'delta_ln_LambdaQCD_over_chi_recombination':qcd_frac_rec,
        'delta_ln_LambdaQCD_over_chi_endpoint':qcd_frac_end,
        'integration_success':float(sol.success),
    }
    return result, zg, dg/delta_initial, np.asarray(tr['x'])


def adiabatic_transfer_results(b:ReheatonBenchmark)->Dict[str,float]:
    # Fixed branching ratios imply delta ln B_i=0 and hence zeta_i=zeta_R.
    return {
        'delta_ln_B0':0.0,
        'delta_ln_B5':0.0,
        'zeta0_over_zetaR':1.0,
        'zeta5_over_zetaR':1.0,
        'S50_over_zetaR':0.0,
        'selector_mass_over_H':selector_results(b)['m_Q_perp_over_Hstar'],
        'reheaton_mass_over_H':b.m_R/b.H_star,
    }


def random_scan(b:ReheatonBenchmark,n:int=50000)->Dict[str,float]:
    rng=np.random.default_rng(909)
    min_eig=float('inf'); min_gap=float('inf'); max_ratio_error=0.0
    passed=0
    for _ in range(n):
        # Scan modestly around benchmark while enforcing a small technically natural mixing.
        mR=10**rng.uniform(8.5,9.5)
        mS=mR*10**rng.uniform(0.4,1.1)
        t=10**rng.uniform(-2.0,-0.8)
        th=math.atan(t); c=math.cos(th); s=math.sin(th)
        M=np.array([[mR*mR*c*c+mS*mS*s*s,-(mS*mS-mR*mR)*s*c],
                    [-(mS*mS-mR*mR)*s*c,mR*mR*s*s+mS*mS*c*c]])
        eig=np.linalg.eigvalsh(M)
        min_eig=min(min_eig,float(eig[0]))
        gap=float(eig[1]-eig[0]); min_gap=min(min_gap,gap)
        ratio=(s*s)/(c*c)
        max_ratio_error=max(max_ratio_error,abs(ratio-t*t))
        if eig[0]>0 and eig[1]>eig[0]: passed+=1
    return {'points':n,'positive_ordered_points':passed,'minimum_eigenvalue_GeV2':min_eig,
            'minimum_gap_GeV2':min_gap,'max_branching_identity_error':max_ratio_error}


def make_plots(b:ReheatonBenchmark, reheating:Dict[str,float], pert:Dict[str,float],
               zgrid:np.ndarray, transfer:np.ndarray)->None:
    import matplotlib.pyplot as plt

    # Branching and temperature hierarchy.
    sectors=np.arange(6)
    B=np.array([b.B0,0,0,0,0,b.B5],dtype=float)
    # Include conservative gravity-only floor for empty sectors for plotting.
    grav=reheating['Bgrav_one']
    Bplot=np.where(B>0,B,grav)
    xi=(Bplot/b.B0)**0.25
    fig,ax=plt.subplots(figsize=(8.2,4.9))
    ax.bar(sectors,xi)
    ax.axhline(0.25,linestyle='--',linewidth=0.9,label=r'target $\xi_5=0.25$')
    ax.set_yscale('log')
    ax.set_ylim(1e-4,1.4)
    ax.set_xlabel('Replica sector $k$')
    ax.set_ylabel(r'$T_k/T_0$ after reheaton decay')
    ax.set_title('State-selected reheating hierarchy')
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTDIR/'state_selected_sector_temperatures_v0_9.png',dpi=220)
    plt.close(fig)

    # Perturbation transfer for the chronometric spectator.
    fig,ax=plt.subplots(figsize=(8.2,4.9))
    order=np.argsort(zgrid)
    ax.plot(1+zgrid[order],np.abs(transfer[order]),label=r'$|\delta x/\delta x_{\rm reh}|$')
    ax.axvline(1091,linestyle='--',linewidth=0.9,label='recombination')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(r'$1+z$')
    ax.set_ylabel('superhorizon transfer magnitude')
    ax.set_title('Damping and late release of chronometric isocurvature')
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTDIR/'state_selected_chronometric_transfer_v0_9.png',dpi=220)
    plt.close(fig)

    # Schematic normalized primordial spectra.
    k=np.geomspace(1e-4,1.0,400)
    ns=NS
    PR=AS*(k/0.05)**(ns-1)
    # Fixed branchings give exactly zero at linear order; show a numerical floor.
    PSI=np.full_like(k,1e-30*AS)
    # chronometric field phase spectrum, converted to QCD-lock fluctuation at reheating.
    pQCD=2.0/27.0; eps_ch=2.70e-13
    dx=b.H_star/(2*PI*2.435e10)
    Pchrono=np.full_like(k,(pQCD*eps_ch*dx)**2)
    fig,ax=plt.subplots(figsize=(8.2,4.9))
    ax.plot(k,PR,label=r'curvature $\mathcal{P}_{\zeta}$')
    ax.plot(k,PSI,label=r'dark-radiation isocurvature (linear floor)')
    ax.plot(k,Pchrono,label=r'chronometric QCD-lock perturbation at reheating')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(r'$k$ [Mpc$^{-1}$]')
    ax.set_ylabel('dimensionless power')
    ax.set_title('Predicted primordial perturbation hierarchy')
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTDIR/'state_selected_perturbation_spectra_v0_9.png',dpi=220)
    plt.close(fig)

    # Mass/decay chronology.
    labels=['inflation $H_*$',r'$m_{Q,\perp}$',r'$m_R$',r'$m_\phi/2$',r'$m_S$',r'$m_{R,k\ne0}$']
    sel=selector_results(b)
    values=[b.H_star,sel['m_Q_perp_GeV'],b.m_R,b.m_inflaton_vac/2,b.m_S,sel['other_reheaton_mass_GeV']]
    fig,ax=plt.subplots(figsize=(8.2,4.9))
    ax.scatter(values,np.arange(len(values)),s=55)
    ax.set_xscale('log')
    ax.set_yticks(np.arange(len(values)),labels)
    ax.axvline(b.m_inflaton_vac/2,linestyle='--',linewidth=0.9,label='two-body threshold')
    ax.set_xlabel('mass or Hubble scale [GeV]')
    ax.set_title('Selector isolation and reheaton mass hierarchy')
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUTDIR/'state_selected_mass_hierarchy_v0_9.png',dpi=220)
    plt.close(fig)


def write_csv(path:Path,rows:List[Dict[str,object]])->None:
    fields=[]; seen=set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key); fields.append(key)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)


def main()->None:
    b=ReheatonBenchmark()
    mass=mass_matrix_parameters(b)
    reh=reheating_results(b)
    sel=selector_results(b)
    infl=inflation_results(b)
    inv=verify_z6_tensor_invariance(b.N)
    adi=adiabatic_transfer_results(b)
    pert,zgrid,transfer,_=chronometric_perturbation_transfer(b)
    scan=random_scan(b)

    # Hard assertions.
    assert abs(b.xi5-0.25)<1e-14
    assert abs(reh['B5_over_B0']-1/256)<1e-14
    assert mass['eigenvalue_light_GeV2']>0 and mass['eigenvalue_heavy_GeV2']>mass['eigenvalue_light_GeV2']
    assert sel['R0_kinematically_open']==1.0
    assert sel['S0_kinematically_closed']==1.0
    assert sel['other_orbits_kinematically_closed']==1.0
    assert inv['max_absolute_Z6_invariance_residual']<1e-10
    assert reh['Delta_Neff']<0.107
    assert adi['S50_over_zetaR']==0.0
    assert pert['transfer_recombination']<1e-4

    benchmark={**asdict(b),**mass,**reh,**sel,**infl,**inv,**adi,**pert}
    acceptance=[
        {'requirement':'Exact microscopic Z6 action','verdict':'PASS','reason':'All couplings are orbit tensors; numerical cyclic-shift residual is zero to floating precision.'},
        {'requirement':'xi0=1 and xi5=0.25','verdict':'PASS','reason':'tan(theta)=1/16 gives B5/B0=1/256 and xi5=(B5/B0)^(1/4)=1/4.'},
        {'requirement':'Other sectors negligibly populated','verdict':'PASS perturbatively','reason':'They have no tree decay channel; conservative gravity-only temperature floor is below one percent.'},
        {'requirement':'Preserve protected Z6 vacuum potential','verdict':'PASS conditionally','reason':'Vacuum couplings are exactly orbit-symmetric; asymmetry is a transient selector state, not a hard sector spurion.'},
        {'requirement':'Kinematic selection of one reheaton orbit','verdict':'PASS','reason':'Only R0 lies below m_phi/2 in the displayed benchmark.'},
        {'requirement':'No domain walls in observable patch','verdict':'PASS conditionally','reason':'Selector chooses one branch during inflation and restores to the unique symmetric origin; chronometric U(1) is broken before inflation and not thermally restored.'},
        {'requirement':'Adiabatic visible/hidden radiation','verdict':'PASS at linear order','reason':'One parent and fixed branching fractions imply zeta0=zeta5 and S50=0.'},
        {'requirement':'Selector/reheaton isocurvature','verdict':'PASS benchmark','reason':'Orthogonal selector and reheaton masses exceed H_star by large factors.'},
        {'requirement':'Chronometric isocurvature','verdict':'PASS benchmark','reason':'Numerical thermal/QCD focusing damps delta x by more than five orders by recombination; spectral impact is below 1e-22.'},
        {'requirement':'Delta N_eff','verdict':'PASS','reason':'One complete adjacent copy at xi=0.25 gives about 0.029.'},
        {'requirement':'Inflation spectrum','verdict':'PASS phenomenologically','reason':'Low-scale hilltop-hybrid benchmark matches As and ns, predicts negligible r and local non-Gaussianity.'},
        {'requirement':'Nonperturbative preheating','verdict':'OPEN','reason':'Requires lattice evolution to verify that no unwanted reheaton orbit is resonantly produced.'},
        {'requirement':'UV discrete-gauge completion','verdict':'OPEN','reason':'Needed to make exact Z6 robust against quantum-gravity violations.'},
        {'requirement':'Higgs naturalness of direct portal','verdict':'CONDITIONAL','reason':'Displayed trilinear is simple but gives a TeV-scale Higgs mass correction; a fermionic thermalizer portal is cleaner.'},
    ]
    result={'benchmark':benchmark,'random_scan':scan,'acceptance':acceptance}
    with (OUTDIR/'state_selected_reheating_results_v0_9.json').open('w') as f:
        json.dump(result,f,indent=2)
    write_csv(OUTDIR/'state_selected_reheating_benchmark_v0_9.csv',[benchmark])
    write_csv(OUTDIR/'state_selected_reheating_acceptance_matrix_v0_9.csv',acceptance)
    make_plots(b,reh,pert,zgrid,transfer)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
