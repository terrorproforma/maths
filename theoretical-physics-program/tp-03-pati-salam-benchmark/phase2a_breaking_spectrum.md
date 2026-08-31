# TP-03 Phase 2A — Neutral breaking orbit and heavy-vector spectrum

**Author:** Angus Muffatti  
**Status:** **COMPLETE AND REPRODUCED INSIDE PHASE 2B**

For

\[
\Delta_R\sim(10,1,3),
\]

choose

\[
\langle\Delta_R\rangle
=
\frac{v_R}{\sqrt2}
|44\rangle_{\rm sym}
\otimes|T_R^3=+1\rangle.
\]

The \(SU(4)\) state has \(B-L=-2\), so

\[
Y=T_R^3+\frac{B-L}{2}=0.
\]

The stabiliser is

\[
SU(3)_C\times U(1)_Y,
\]

and with the untouched \(SU(2)_L\),

\[
SU(4)_C\times SU(2)_L\times SU(2)_R
\rightarrow
SU(3)_C\times SU(2)_L\times U(1)_Y.
\]

Nine generators are broken:

- six \(SU(4)/[SU(3)\times U(1)]\) vector-leptoquark directions;
- two charged \(SU(2)_R\) directions;
- one neutral direction orthogonal to hypercharge.

With canonical generator normalization,

\[
m_X^2=\frac12g_4^2v_R^2,
\]

\[
m_{W_R}^2=\frac12g_R^2v_R^2,
\]

\[
m_{Z_R}^2=
\left(
\frac32g_4^2+g_R^2
\right)v_R^2.
\]

The orthogonal neutral eigenvalue is exactly zero, and

\[
\frac1{g_Y^2}
=
\frac1{g_R^2}
+
\frac{2}{3g_4^2}.
\]

The explicit generator-level calculation now lives in
`code/verify_phase2b_vacuum.py`; the machine output is
`results/phase2b_vacuum_spectrum.json`.
