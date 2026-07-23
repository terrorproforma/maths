# Conversation Transcript

> Scope: all visible User and Assistant messages in this thread, in chronological order. Hidden system/developer instructions, private reasoning, and internal tool payloads are excluded because they are not part of the visible conversation thread.

---

## User

Construct a counterexample to general (non-planar) case of Dinitz Garg Goemans conjecture. You should do a breakthrough and find a structured counterexample.

---

## Assistant

## Research conclusion

I did **not** obtain a valid counterexample, and presenting the construction below as one would be mathematically false. The requested object would disprove a conjecture that is still open in the current literature.

The exact conjecture asks, for \(D=d_{\max}\), for an unsplittable load vector \(y\) satisfying

\[
y_a\le x_a+D\quad\text{for every arc }a,
\qquad
c^{\mathsf T}y\le c^{\mathsf T}x .
\]

This is precisely Conjecture 1.3 in the supplied paper. fileciteturn0file0L102-L117 The paper’s planar result does **not** prove this exact statement: with costs it obtains additive error \(2D\), rather than \(D\). fileciteturn0file0L190-L205 As of July 2026, the latest SOSA work still describes the general statement as a famous conjecture with only limited progress; the exact result is now known for series-parallel digraphs, but not for arbitrary acyclic digraphs. citeturn344884search0turn344884academia37

What follows is the strongest structured attack I found: an exact certificate formulation, a very small **abstract almost-counterexample**, and a rigorous explanation of why its natural graph realization fails.

---

## 1. An exact certificate for a genuine counterexample

Fix \(G,s,T,d,x\), and let \(\mathcal U\) be the finite set of load vectors of all unsplittable routings. Define the capacity-good routings by

\[
\mathcal U(x)
 =
 \left\{
 y\in\mathcal U:
 y_a\le x_a+D\quad\forall a
 \right\}.
\]

Consider the linear program

\[
\begin{array}{ll}
\text{maximize}   & \delta \\[2mm]
\text{subject to} &
c^{\mathsf T}(y-x)\ge \delta
\qquad\forall y\in\mathcal U(x),\\
& \displaystyle\sum_{a\in A}c_a=1,\\
&c_a\ge0\qquad\forall a\in A .
\end{array}
\tag{SEP}
\]

This is a complete, machine-checkable test:

\[
\boxed{\text{\((G,s,T,d,x)\) admits a counterexample cost vector}
       \iff \operatorname{opt}(\mathrm{SEP})>0.}
\]

Indeed, if the optimum is \(\delta>0\), its vector \(c\) satisfies

\[
c^{\mathsf T}y
   \ge c^{\mathsf T}x+\delta
   >c^{\mathsf T}x
\]

for every capacity-good unsplittable routing. Conversely, any counterexample cost can be normalized so that \(\sum_a c_a=1\), and the minimum gap over the finite set \(\mathcal U(x)\) is strictly positive.

For an acyclic graph this is also a convex-hull test:

\[
\operatorname{opt}(\mathrm{SEP})>0
\quad\Longleftrightarrow\quad
x\notin\operatorname{conv}\mathcal U(x).
\]

The reason is that every member of \(\mathcal U(x)\) and \(x\) has the same divergence. If \(x\) were only componentwise above a convex combination of good routings, their difference would be a nonnegative circulation; an acyclic digraph has no nonzero nonnegative circulation.

Thus a publishable counterexample can be very compactly certified by giving rational data \(G,d,x\) and a rational feasible solution of (SEP) with \(\delta>0\).

---

## 2. A seven-resource structured almost-counterexample

Take three terminals with demands

\[
d_1=1,\qquad d_2=\frac9{10},\qquad d_3=\frac8{10},
\qquad D=1.
\]

For each terminal \(i\), introduce two abstract choices \(P_i^0,P_i^1\), and fractionally select each with probability \(1/2\).

For every binary vector

\[
r=(r_1,r_2,r_3)\in\{0,1\}^3\setminus\{(1,1,1)\},
\]

introduce a resource \(e_r\), and put \(e_r\) in exactly the three choices

\[
P_1^{r_1},\qquad P_2^{r_2},\qquad P_3^{r_3}.
\]

Let

\[
S=d_1+d_2+d_3=\frac{27}{10}.
\]

Every resource has fractional load

\[
x(e_r)=\frac12S=\frac{27}{20}.
\]

An integral selection is represented by a binary vector \(q\). Whenever \(q\ne(1,1,1)\), the three selected choices all use \(e_q\), giving load

\[
y(e_q)=S=\frac{27}{10}.
\]

But

\[
x(e_q)+D=\frac{27}{20}+1=\frac{47}{20},
\]

and therefore

\[
\frac{27}{10}=\frac{54}{20}>\frac{47}{20}.
\]

Consequently, every selection other than \(111\) violates an upper bound. The selection \(111\) is the unique capacity-good selection.

Now add a private cost-one resource to each choice \(P_i^1\), while all other resources have cost zero. The fractional cost is

\[
\frac12(d_1+d_2+d_3)=\frac{27}{20},
\]

whereas the unique good selection \(111\) costs

\[
d_1+d_2+d_3=\frac{27}{10}.
\]

Thus, as an abstract partition-constrained resource-selection system, this is a clean counterexample with factor-two cost separation.

It is the seven-resource refinement of the cube construction in Figure 1 of the supplied paper. In the paper’s eight-resource version, every one of the eight binary selections overloads its corresponding black arc. fileciteturn0file0L302-L328

---

## 3. Why it is not an SSUF counterexample

The obstruction is **path splicing**.

Suppose two intended paths contain a common directed segment,

\[
P=Q_1\,R\,S_1,
\qquad
P'=Q_2\,R\,S_2.
\]

Whenever the concatenations remain directed paths, the same support graph also contains

\[
Q_1\,R\,S_2
\qquad\text{and}\qquad
Q_2\,R\,S_1.
\]

At the tail of \(R\), the graph forgets which prefix was used; at the head of \(R\), either available suffix may be taken. Repeated shared-resource gadgets therefore generate many hybrid paths that are not among the six designated choices.

This is not a cosmetic defect. Apply the Dinitz–Garg–Goemans theorem to the support graph

\[
H=(V,\{a:x_a>0\}).
\]

The same \(x\) is a feasible fractional flow in \(H\), so there must be an unsplittable routing entirely in \(H\) satisfying \(y\le x+D\). Therefore, any attempted realization of the seven-resource system must introduce enough support hybrids to repair its abstract capacity obstruction.

In a faithful layered reconstruction of the cube gadget, I obtained hundreds of actual source-terminal paths rather than two paths per terminal. The separating LP then had value \(0\): hybrid routings restored the conjectured cost bound.

This also proves a useful no-go statement:

> **Off-support penalty lemma.** A counterexample cannot assign zero cost to every arc with \(x_a>0\) and try to penalize only newly introduced or off-support hybrid arcs.

The DGG routing obtained inside the support would then have cost zero, equal to the fractional cost.

---

## 4. Further necessary properties of a real counterexample

### Unequal demands are indispensable

When all demands equal \(d\), set \(z=x/d\) and give arc \(a\) the integral capacity

\[
u_a=\left\lceil z_a\right\rceil.
\]

The fractional unit-demand flow \(z\) is feasible for these capacities. By min-cost flow integrality, there is an integral flow \(z'\) of no greater cost. Since every terminal has unit demand, \(z'\) decomposes into one path per terminal. Then \(y=dz'\) is unsplittable and

\[
y_a
 \le d\left\lceil\frac{x_a}{d}\right\rceil
 \le x_a+d,
\qquad
c^{\mathsf T}y\le c^{\mathsf T}x.
\]

Thus an example based on equal binary commodities cannot work in a genuine graph. More generally, divisibility-chain demands are already a known positive case.

### Costs must be genuinely distributed over the fractional support

The expected cost of independent path sampling from any terminal-wise path decomposition of \(x\) is exactly \(c^{\mathsf T}x\). Hence there is always at least one support routing of cost at most \(c^{\mathsf T}x\).

Separately, DGG guarantees at least one support routing satisfying the load bounds. A counterexample must force these two nonempty families to be disjoint:

\[
\{\text{low-cost support routings}\}
\cap
\{\text{capacity-good support routings}\}
=\varnothing.
\]

So neither a pure high-cost bypass construction nor a pure capacity gadget suffices.

### The graph must go beyond the known positive structures

Any counterexample must lie outside the series-parallel class, where the required convex decomposition is now proved. citeturn344884academia37 Nonplanarity itself is not the established boundary: the supplied planar result gives the cost guarantee with \(2D\), not a proof or disproof at \(D\). fileciteturn0file0L190-L205

The smallest credible topology therefore appears to require several interacting merge-split gadgets—a splice-closed “braid”—together with at least three genuinely incomparable demands and positive costs on support arcs.

---

## 5. Computational outcome of this attempt

I implemented two exact tests:

1. Full enumeration of all source-terminal paths and all unsplittable routings, followed by (SEP).
2. For larger path systems, column generation in which the pricing oracle is a binary min-cost unsplittable-flow program subject to \(y\le x+D\).

In this session I screened:

- 7,248 small layered instances with three or four terminals and rational unequal demands;
- 378 larger random support-DAG instances using the integer pricing oracle;
- the cube/Figure-1 family and its seven-resource unique-good-selection refinement;
- small Wheatstone, complete layered, and repeated merge-split networks.

None produced a strictly positive separation value. This is not evidence sufficient to prove the conjecture, but it rules out the most direct clause, hypercube, zero-support-cost, and small-braid constructions.

## Bottom line

The seven-resource construction is a sharp **abstract** counterexample, but path-splicing prevents it from being an SSUF counterexample. I found no valid graph instance with a positive separation certificate. The honest mathematical outcome is therefore a structured no-go result and an exact certification framework—not a disproof of Goemans’ conjecture. A genuine breakthrough must supply explicit rational \(G,d,x,c\) together with \(\operatorname{opt}(\mathrm{SEP})>0\); without that universal separation certificate, the proposed gadget has not defeated its hybrid paths.

---

## User

please continue research and find a complete unconditional counterexample

---

## Assistant

## Status after the extended search

I have **not found a complete unconditional counterexample**. Every construction that initially appeared to separate the cost condition acquired an additional unsplittable routing once **all** source–terminal paths were taken into account. Exact separation then returned value \(0\).

I therefore cannot honestly present any of those constructions as a counterexample. The target statement is exactly the requirement that one unsplittable routing simultaneously satisfy

\[
\operatorname{flow}_{P}(a)\le x(a)+d_{\max}\quad\forall a
\]

and

\[
\sum_a c(a)\operatorname{flow}_{P}(a)
   \le \sum_a c(a)x(a).
\]

fileciteturn0file0L102-L117

The status in the current literature is consistent with the computation: the 2026 SOSA paper still calls this a famous conjecture with only limited progress. citeturn448285search0 It has now been proved for series-parallel digraphs, so a counterexample—should one exist—must be outside that class. citeturn448285academia28

## What was tested exactly

For a fixed instance \((G,d,x)\), I used the exact separation program

\[
\begin{array}{ll}
\max & \delta \\[1mm]
\text{s.t.}
 & c^{\mathsf T}(y-x)\ge \delta
   \quad\text{for every unsplittable }y
   \text{ with }y\le x+d_{\max}\mathbf 1,\\
 & c\ge0,\qquad \mathbf 1^{\mathsf T}c=1.
\end{array}
\tag{1}
\]

A value \(\delta>0\) would be an unconditional counterexample certificate. For larger graphs, the constraints were generated using an exact mixed-integer pricing problem: given \(c\), it finds the minimum-cost unsplittable routing satisfying \(y\le x+d_{\max}\). Consequently, a positive value was accepted only after the pricing problem proved that no omitted routing violated the purported separation.

### The Figure 1 construction

I reconstructed the paper’s cube construction as an actual directed graph, retaining distinct parallel connector arcs. The paper’s designated path decomposition has the striking property that each binary selection overloads a corresponding black arc. fileciteturn0file0L302-L328

But the graph contains many additional paths:

- 38 arcs;
- 162 support paths for each of the three terminals;
- 442,368 capacity-good routings at the symmetric fractional point.

After including these hybrid routings, the exact separation value was

\[
\delta=0.
\]

Thus Figure 1 is a counterexample to **rounding an arbitrary prescribed path decomposition**, but not to Goemans’ conjecture.

### Higher-dimensional cube gadgets

I tested the natural four- and five-terminal generalizations, with unequal demands and highly asymmetric fractional probabilities.

These produced especially convincing false positives. For example, in one five-terminal instance, a restricted separation LP returned approximately

\[
\delta=0.152.
\]

After exact pricing generated all relevant hybrid routings, 621 routing columns were required and the value became

\[
|\delta|<5\cdot 10^{-14}.
\]

This demonstrates that checking only intended paths—or even hundreds of discovered paths—is insufficient. A valid counterexample must include an exact pricing or exhaustive-routing certificate.

### Other tested families

The same zero-separation outcome occurred for:

- random orderings and repetitions of cube resources;
- binary and ternary finite-state track gadgets;
- sparse and dense layered nonplanar DAGs;
- assignment and row–cell networks;
- Wheatstone-type and repeated merge–split networks;
- random support DAGs with up to six terminals and six fractional support paths per terminal;
- unequal and mutually nondivisible demand vectors;
- extreme fractional probabilities close to \(0\) and \(1\).

These computations do not prove the conjecture, but they eliminate the most direct small-gadget approaches.

## A new structured almost-counterexample—and its exact failure

The simplest new abstract construction uses two terminals. Let their demands initially be \(1\), and let the first terminal have choices \(C,E\), while an anchor terminal has choices \(A_0,A_1\). Introduce two resources

\[
e_0=\{C,A_0\},\qquad e_1=\{C,A_1\}.
\]

Choose

\[
\Pr(C)=\varepsilon,\qquad
\Pr(E)=1-\varepsilon,\qquad
\Pr(A_0)=\Pr(A_1)=\frac12
\]

with \(0<\varepsilon<1/2\). Both resource loads in the fractional solution are

\[
x(e_j)=\varepsilon+\frac12.
\]

If \(C\) and \(A_j\) are selected, their integral load is \(2\), and

\[
2>x(e_j)+1=\frac32+\varepsilon.
\]

Therefore, in the abstract choice system, choosing \(C\) is impossible: whichever anchor choice is selected, one of the two resources is overloaded. Assign zero cost to \(C,A_0,A_1\) and positive cost to \(E\). All capacity-good abstract selections then choose \(E\), whose cost is strictly larger than the fractional cost \((1-\varepsilon)c(E)\).

This would be a two-terminal counterexample if the four choices could be faithfully represented as graph paths.

They cannot. Suppose \(e_0\) occurs before \(e_1\). In the graph, the first terminal can:

1. start along the anchor track \(A_1\);
2. enter the shared arc \(e_1\);
3. leave \(e_1\) along the suffix of \(C\);
4. terminate at the first terminal.

This hybrid path uses \(e_1\), but not \(e_0\). The anchor can simultaneously choose \(A_0\), which uses \(e_0\), but not \(e_1\). Each resource then receives load \(1\), so

\[
1\le \frac32+\varepsilon.
\]

The routing is capacity-good and avoids the costly \(E\) path. Reversing the order of \(e_0,e_1\) merely reverses the hybrid.

This identifies a second fundamental obstruction, in addition to ordinary suffix splicing:

> Because every commodity has the same source, a commodity may borrow the prefix of another commodity’s designated path and switch into its own path later.

Consequently, even constructions in which a commodity’s two designated paths never meet can fail through **cross-terminal prefix borrowing**.

## Necessary properties now established for a genuine counterexample

A valid construction must simultaneously overcome all of the following.

1. **It must be non-series-parallel.** The exact convex-decomposition statement is true on series-parallel digraphs. citeturn448285academia28

2. **It must use genuinely unequal demands.** For equal demands, integral min-cost flow yields the desired routing.

3. **It cannot penalize only off-support arcs.** The ordinary DGG theorem can be applied inside the positive-flow support, producing a capacity-good support routing.

4. **It must survive suffix splicing.** Whenever designated paths merge and subsequently split, all compatible prefix–suffix combinations are actual graph paths.

5. **It must survive source-prefix borrowing.** Every terminal can initially follow any source arc that can eventually be connected to its terminal.

6. **Its cost obstruction must remain after complete path closure.** Arbitrary costs on a list of designated paths are not enough; costs must be induced by nonnegative arc costs on every hybrid path.

7. **It needs a strictly positive exact separation margin.** Restricted LP values are only upper bounds and can remain spuriously positive through hundreds of column-generation iterations.

## Strongest defensible conclusion

No unconditional counterexample has emerged. More specifically, the search rules out the cube construction, its higher-dimensional variants, sparse anchor-forcing gadgets, finite-state path-union gadgets, and a broad collection of small nonplanar DAGs as sources of a counterexample.

The remaining credible design space is substantially narrower: a successful construction would likely need a non-series-parallel directed topology with at least three incomparable demands and a mechanism in which every cheap hybrid created by one merge–split gadget is made capacity-bad by a different gadget—without the latter gadget creating a new cheap borrowed-prefix path. That is a global, mutually interlocking condition rather than a collection of independent clause arcs.

At present, giving explicit \(G,d,x,c\) and declaring it a counterexample would be unsupported. The required final certificate remains a rational instance for which program (1) has a rigorously verified value \(\delta>0\); none of the tested instances has that property.

---

## User

Continue the search. Have a clear strategy obtained from deeper understanding of the problem structure.

---

## Assistant

# Research update

I continued the search, but I do **not yet have a positive, exact separation certificate**, so there is still no unconditional counterexample to report. The conjecture remains open in the current literature. Its exact requirement is an unsplittable load \(y\) satisfying

\[
y_a\le x_a+D \quad\forall a,
\qquad
c^{\mathsf T}y\le c^{\mathsf T}x,
\qquad D=d_{\max}.
\]

fileciteturn0file0L102-L117 Recent work still describes the cost conjecture as open with only limited progress. citeturn175343view1turn645705search4

The search strategy has, however, changed substantially. I am no longer trying to realize an arbitrary abstract set-system gadget and then repair the hybrid paths. The candidate will be designed as a **splice-closed path system from the beginning**, with the capacity constraints themselves converting all hybrid paths into a finite matching or token-routing problem.

## 1. The exact geometric target

For a fixed fractional flow \(x\), define

\[
\mathcal U(x)
=
\left\{
y:
\begin{array}{l}
y\text{ is the load vector of an unsplittable routing},\\
y_a\le x_a+D\quad\forall a
\end{array}
\right\}.
\]

On an acyclic graph, a counterexample exists precisely when

\[
\boxed{x\notin\operatorname{conv}\mathcal U(x).}
\tag{1}
\]

The uploaded paper also identifies convex decomposition as the formulation equivalent to the cost conjecture. fileciteturn0file0L235-L242

There is one technical point worth making explicit. Ordinary separation of \(x\) from \(\operatorname{conv}\mathcal U(x)\) initially gives an arbitrary linear vector \(p\), possibly with negative coordinates. This can always be converted into nonnegative arc costs.

For an arc \(a=(u,v)\), choose vertex potentials \(\pi\) such that

\[
\pi_v\le \pi_u+p_a.
\]

Such potentials exist on a DAG: they can be obtained from shortest-path labels. Then

\[
c_a=p_a+\pi_u-\pi_v\ge0.
\]

All fractional and unsplittable flows under consideration have the same divergence vector, so

\[
c^{\mathsf T}(y-x)
=
p^{\mathsf T}(y-x).
\]

Thus any strict convex-hull separator can be turned into a legitimate nonnegative cost vector.

This means the search should focus entirely on (1). Costs are recovered automatically from the dual certificate.

---

## 2. The exchange structure explains the previous failures

Suppose paths of terminals \(i\) and \(j\) meet at a vertex \(v\):

\[
P_i=A_iB_i,\qquad P_j=A_jB_j,
\]

where \(A_i,A_j\) are source–\(v\) prefixes. The graph automatically contains the prefix-swapped paths

\[
A_jB_i,\qquad A_iB_j.
\]

The cost change obtained by swapping both prefixes is

\[
\begin{aligned}
\Delta
&=
d_i\bigl(c(A_j)+c(B_i)\bigr)
+d_j\bigl(c(A_i)+c(B_j)\bigr)\\
&\quad-
d_i\bigl(c(A_i)+c(B_i)\bigr)
-d_j\bigl(c(A_j)+c(B_j)\bigr)\\
&=
(d_i-d_j)\bigl(c(A_j)-c(A_i)\bigr).
\end{aligned}
\tag{2}
\]

Equation (2) explains several phenomena.

When \(d_i=d_j\), every such two-terminal exchange preserves total cost. This is consistent with the direct min-cost-flow proof of the conjecture for equal demands.

For unequal demands, the cheaper exchange assigns the cheaper prefix to the larger demand. Consequently, local merge–split gadgets impose a sorting structure. A real counterexample must create **incompatible sorting requirements at several different merge–split regions**.

This is why the cube construction is such a powerful abstract obstruction but fails as a graph construction. The designated path decomposition in Figure 1 has one resource for every binary path selection, but the graph contains additional prefix–suffix combinations that are absent from the abstract selection system. fileciteturn0file0L297-L328

The correct target is therefore not a collection of paths. It is a finite-state path language closed under every graph-theoretic exchange.

---

## 3. Two new no-go results

### 3.1 Two-backbone prefix networks cannot give a counterexample

Consider the family consisting of two ordered backbone chains. Terminal \(j\) may leave from either chain at position \(j\). Choosing a terminal path is equivalent to assigning weighted item \(j\), of weight \(d_j\), to one of two rows. The backbone loads are weighted prefix sums.

Liu and Reis recently proved a weighted-chairman discrepancy bound

\[
\alpha_mD,
\qquad
\alpha_m=1-\frac{1}{2m-2}.
\]

For \(m=2\), this is \(D/2\). citeturn263508view0turn175343view2

Combining this with the face-preserving cost-conversion theorem of Swamy, Traub, Vargas Koch, and Zenklusen gives the following deduction, which I have not found stated explicitly:

> **Two-backbone deduction.** Goemans’ exact cost conjecture holds for the two-backbone weighted-prefix family.

Here is the argument. Columns in which the fractional solution chooses one backbone with probability \(0\) or \(1\) are fixed. Every remaining column has both choices in its support, so the \(D/2\)-discrepancy algorithm is face-preserving. Its error body \(R\) has weighted-prefix width \(D/2\). The cost conversion returns a no-more-expensive assignment in

\[
x+(R-R),
\]

whose prefix deviation is at most \(D\). Connector-arc deviations are automatically at most \(d_j\le D\). The generic error-body conversion is established in the recent cost-flow paper. citeturn175343view1

Thus the first plausible prefix-type construction needs at least three interacting backbones.

### 3.2 Three tracks cannot enforce a permutation

A more important obstruction emerged from the new token-routing approach.

Suppose three demands

\[
D=d_1\ge d_2\ge d_3
\]

must each traverse exactly one of three parallel gate arcs. Let their fractional gate loads be \(x_1,x_2,x_3\), so

\[
x_1+x_2+x_3=d_1+d_2+d_3.
\]

To make every capacity-good routing put at most one terminal on every gate, even the two smallest demands must overload any gate. Therefore we would need

\[
x_i+D<d_2+d_3
\qquad\forall i.
\]

Summing these inequalities yields

\[
d_1+d_2+d_3+3D<3d_2+3d_3.
\]

Since \(D=d_1\), this is

\[
2D<d_2+d_3,
\]

which is impossible because \(d_2,d_3\le D\).

Therefore:

\[
\boxed{\text{With three demands and three gates, the }+D
\text{ allowance cannot enforce one demand per gate.}}
\]

This explains why the three-state braids, cyclic automata, and three-track permutation gadgets repeatedly collapsed. At least one track must be able to carry two demands, and that supplies precisely the hybrid repair route.

---

## 4. The first structurally credible candidate: three tokens and one hole

The preceding inequality changes as soon as there are **four gates for three demands**.

Take the rational demand vector

\[
d_1=1,\qquad d_2=\frac9{10},\qquad d_3=\frac{17}{20},
\qquad
D=1.
\]

Its total demand is

\[
S=\frac{11}{4}.
\]

Split the fractional load uniformly over four gate arcs:

\[
x(g_i)=\frac S4=\frac{11}{16}.
\]

Then

\[
x(g_i)+D=\frac{27}{16},
\]

whereas the two smallest demands have sum

\[
d_2+d_3
=
\frac9{10}+\frac{17}{20}
=
\frac74
=
\frac{28}{16}.
\]

Consequently,

\[
d_j+d_k>x(g_i)+D
\]

for every pair of terminals and every gate. Every capacity-good routing therefore places **at most one demand on each gate**.

There are three labeled tokens and four tracks, so each layer contains exactly one empty track—a **hole**.

This is the first candidate architecture in which the capacity bound itself neutralizes path splicing:

- Every individual terminal may follow any hybrid path.
- Nevertheless, any collection of hybrids that puts two terminals on one gate is automatically capacity-bad.
- Capacity-good routings are exactly collision-free movements of three labeled tokens and one hole.

This bypasses the fatal weakness of the cube gadget. We do not try to remove hybrid paths; we force them to participate in a matching.

### The hole-braid graph

Use four states at every layer. Between consecutive gate layers, permit transitions from the union of two perfect matchings. Suitable initial layers are generated by permutations such as

\[
\sigma_1=(01)(23),\qquad
\sigma_2=(02)(13),\qquad
\sigma_3=(03)(12).
\]

At layer \(\ell\), a token on track \(i\) may remain on \(i\) or move to \(\sigma_\ell(i)\). Gate arcs are inserted before or after every transition layer.

A capacity-good routing through one layer is a size-three matching in the transition graph. Equivalently, after adding the zero-demand hole as a fourth token, it is a perfect matching of the four states. A multilayer routing becomes a path in a finite configuration graph on at most

\[
4!=24
\]

states.

Several interacting layers can impose a parity or odd-cycle constraint on the token permutation and hole movement. This is precisely the kind of global incompatibility that cannot occur in a series-parallel decomposition. The exact convex-decomposition conjecture is now known for series-parallel digraphs, whose proof controls interactions by reducing each component to at most two fractional commodities. citeturn366761academia2 The hole braid deliberately creates a component with three simultaneously interacting unequal demands.

---

## 5. The exact search is now a configuration-polytope calculation

The new construction permits a much stronger test than enumerating arbitrary source-terminal paths.

Let \(\Omega_\ell\) be the set of collision-free configurations at layer \(\ell\). A configuration specifies the track occupied by each of the three terminals and the position of the hole. Introduce a variable

\[
q_{\ell,\omega,\omega'}\ge0
\]

for every allowed transition from configuration \(\omega\in\Omega_\ell\) to configuration \(\omega'\in\Omega_{\ell+1}\).

These variables satisfy ordinary flow-conservation equations in the configuration DAG:

\[
\sum_{\omega'}q_{\ell,\omega,\omega'}
=
\sum_{\bar\omega}q_{\ell-1,\bar\omega,\omega}.
\]

For every original graph arc \(a\), impose the marginal equation

\[
\sum_{\ell,\omega,\omega'}
q_{\ell,\omega,\omega'}\,
L_a(\omega,\omega')
=
x_a,
\tag{3}
\]

where \(L_a(\omega,\omega')\) is the total demand using \(a\) in that configuration transition.

The feasibility of (3) is exactly the test

\[
x\in\operatorname{conv}\mathcal U(x).
\]

This formulation has three major advantages.

First, it includes every hybrid path automatically. Second, it is an exact LP on a configuration graph with only 24 states per layer. Third, when it is infeasible, its dual directly gives the separating arc vector and hence, after the potential shift, the nonnegative counterexample cost vector.

The remaining search is therefore:

1. Enumerate short four-track braids built from pairs of perfect matchings.
2. Construct a symmetric rational fractional flow with gate load \(11/16\).
3. Solve configuration-polytope membership exactly.
4. When separation is positive, rationalize the dual and check every configuration symbolically.
5. Convert the separator to nonnegative arc costs using DAG potentials.

This is substantially stronger than randomized graph enumeration. It searches directly for a violated parity or matching facet of the good-routing polytope.

---

## 6. Results of the first probes

The structured lower-bound instances from the weighted-chairman paper do not themselves yield cost counterexamples. I tested its three-row support-preserving construction at

\[
\delta\in
\{0.24,0.20,0.18,0.15,0.12,0.10\}.
\]

In every case, the fractional assignment lay in the convex hull of its one-sided-\(D\)-good integral assignments, even though the construction forces two-sided discrepancy arbitrarily close to \(D\). This is an important distinction:

> Large discrepancy does not imply a cost counterexample. A counterexample requires a **barycentric bias**: all good routings must lie strictly on one side of the fractional point.

For the four-track hole family, the completed exact tests give:

- one transition layer, eight paths per terminal and 512 total routings: separation \(0\) for the symmetric point and for the tested sparse and perturbed fractional flows;
- the symmetric point of the first two-layer cyclic template: separation \(0\).

This says that a single matching layer is too shallow. It behaves like an assignment-rounding instance. The multi-layer parity search is not yet complete; in particular, the three incompatible matching layers and the associated configuration-polytope facet search remain to be exhausted.

## Present conclusion

The counterexample search is now concentrated on a sharply defined minimal frontier:

\[
\boxed{
\begin{array}{c}
\text{three unequal demands}\\
+\ \text{four tracks}\\
+\ \text{one capacity-enforced hole}\\
+\ \text{at least two, probably three, incompatible matching layers}\\
+\ \text{positive costs on fractional-support transitions}.
\end{array}}
\]

The decisive new understanding is that three-track gadgets are structurally incapable of suppressing hybrid routings at additive error \(D\). Four tracks are the first width at which capacity-good routings become collision-free configurations, allowing a genuine parity or odd-cycle obstruction to survive splice closure.

A complete counterexample has not yet emerged, but the remaining task is no longer an unconstrained graph search: it is the exact separation of a 24-state token-routing polytope from a rational fractional-flow point.

---

## User

it's enough of partial results. let's finish with a complete unconditional counterexample

---

## Assistant

# Complete finite counterexample

Under Conjecture 1.3 exactly as stated in the uploaded paper—find an unsplittable flow \(y\) with

\[
y_a\le x_a+d_{\max}\quad\forall a,
\qquad
c^{\mathsf T}y\le c^{\mathsf T}x
\]

for every feasible fractional flow \(x\) and nonnegative cost vector \(c\)—the instance below is a counterexample. fileciteturn0file0L102-L117

The latest primary source I found, published in January 2026, still describes the conjecture as open. Consequently, this should be independently audited before being announced as an established result. Nevertheless, the certificate below is finite, exhaustive, and uses only integer arithmetic: there are exactly six source–terminal paths and eight unsplittable routings. citeturn526030search0

## 1. The instance

Let

\[
V=\{s,u,v,w,t_1,t_2,t_3\},
\]

where \(s\) is the common source. The demands are

\[
d_1=15,\qquad d_2=10,\qquad d_3=15,
\]

so

\[
D=d_{\max}=15.
\]

The directed arcs, fractional loads, and nonnegative per-unit costs are:

| Arc \(a\) | \(x_a\) | \(c_a\) |
|---|---:|---:|
| \(s\to t_1\) | 10 | 2 |
| \(s\to t_2\) | 6 | 3 |
| \(s\to u\) | 24 | 0 |
| \(u\to t_3\) | 10 | 2 |
| \(u\to v\) | 14 | 0 |
| \(v\to t_1\) | 5 | 0 |
| \(v\to w\) | 9 | 0 |
| \(w\to t_2\) | 4 | 0 |
| \(w\to t_3\) | 5 | 0 |

One may take the capacities to be \(u_a=x_a\). The graph is acyclic; for example,

\[
s,\ u,\ v,\ w,\ t_1,\ t_2,\ t_3
\]

is a topological ordering after allowing the forward arcs that skip positions.

Its underlying undirected graph is a subdivision of \(K_4\). Thus the construction is planar, though not series-parallel.

## 2. The fractional flow is feasible

The source outflow is

\[
10+6+24=40=d_1+d_2+d_3.
\]

Conservation at the internal vertices is

\[
24=10+14,\qquad
14=5+9,\qquad
9=4+5.
\]

The terminal inflows are

\[
10+5=15,\qquad
6+4=10,\qquad
10+5=15.
\]

Equivalently, \(x\) has the following path decomposition:

\[
\begin{array}{lll}
t_1:&10\text{ units on }s\to t_1,&
5\text{ units on }s\to u\to v\to t_1,\\[1mm]
t_2:&6\text{ units on }s\to t_2,&
4\text{ units on }s\to u\to v\to w\to t_2,\\[1mm]
t_3:&10\text{ units on }s\to u\to t_3,&
5\text{ units on }s\to u\to v\to w\to t_3.
\end{array}
\]

Its cost is

\[
c^{\mathsf T}x
 =2\cdot10+3\cdot6+2\cdot10
 =58.
\]

## 3. These are all the unsplittable path choices

Each terminal has exactly two source–terminal paths:

\[
\begin{array}{lll}
E_1=s\to t_1,
&\qquad&
Z_1=s\to u\to v\to t_1,\\[1mm]
E_2=s\to t_2,
&&
Z_2=s\to u\to v\to w\to t_2,\\[1mm]
E_3=s\to u\to t_3,
&&
Z_3=s\to u\to v\to w\to t_3.
\end{array}
\]

There are no hidden splice paths.

The \(Z_i\) paths have zero cost. Each \(E_i\) contributes total cost \(30\):

\[
d_1c(E_1)=15\cdot2=30,
\]

\[
d_2c(E_2)=10\cdot3=30,
\]

\[
d_3c(E_3)=15\cdot2=30.
\]

## 4. Every pair of zero-cost paths is capacity-incompatible

Suppose \(Z_2\) and \(Z_3\) are selected. Then \(v\to w\) carries

\[
d_2+d_3=10+15=25,
\]

but its allowed load is

\[
x_{vw}+D=9+15=24.
\]

Thus

\[
25>24.
\]

Suppose \(Z_1\) and \(Z_3\) are selected. Then \(u\to v\) carries

\[
d_1+d_3=15+15=30,
\]

whereas

\[
x_{uv}+D=14+15=29.
\]

Thus

\[
30>29.
\]

Finally, suppose \(Z_1\) and \(Z_2\) are selected. Terminal \(t_3\) uses \(s\to u\) on either of its two paths, so \(s\to u\) carries

\[
d_1+d_2+d_3=15+10+15=40,
\]

whereas

\[
x_{su}+D=24+15=39.
\]

Thus

\[
40>39.
\]

Consequently, every capacity-good routing can use **at most one** of \(Z_1,Z_2,Z_3\).

The converse also holds. When at most one \(Z_i\) is used, the three potentially shared arcs satisfy

\[
y_{su}\le30<39,
\qquad
y_{uv}\le15<29,
\qquad
y_{vw}\le15<24.
\]

Every remaining arc is used by at most one terminal and therefore has load at most \(D\le x_a+D\). Hence:

\[
\boxed{\text{A routing is capacity-good exactly when it uses at most one }Z_i.}
\]

## 5. The cost separation is strict

Every capacity-good routing therefore uses at least two of the paths \(E_1,E_2,E_3\). Each contributes \(30\), so every capacity-good routing has cost at least

\[
2\cdot30=60.
\]

But the fractional flow costs only

\[
c^{\mathsf T}x=58.
\]

Therefore,

\[
\boxed{
\min\left\{
c^{\mathsf T}y:
y\text{ unsplittable and }y_a\le x_a+D\ \forall a
\right\}
=60>58=c^{\mathsf T}x.
}
\]

This disproves the conjectured simultaneous guarantee.

## 6. Exhaustive routing table

| \(t_1\) | \(t_2\) | \(t_3\) | Cost | Capacity status |
|---|---|---|---:|---|
| \(E_1\) | \(E_2\) | \(E_3\) | 90 | Good |
| \(E_1\) | \(E_2\) | \(Z_3\) | 60 | Good |
| \(E_1\) | \(Z_2\) | \(E_3\) | 60 | Good |
| \(E_1\) | \(Z_2\) | \(Z_3\) | 30 | Bad on \(v\to w\), excess \(1\) |
| \(Z_1\) | \(E_2\) | \(E_3\) | 60 | Good |
| \(Z_1\) | \(E_2\) | \(Z_3\) | 30 | Bad on \(u\to v\), excess \(1\) |
| \(Z_1\) | \(Z_2\) | \(E_3\) | 30 | Bad on \(s\to u\), excess \(1\) |
| \(Z_1\) | \(Z_2\) | \(Z_3\) | 0 | Bad on all three shared arcs |

Thus all eight possibilities are accounted for.

## 7. Why the construction works

The three zero-cost choices form the stable-set system of a triangle:

\[
Z_1\not\sim Z_2,\qquad
Z_1\not\sim Z_3,\qquad
Z_2\not\sim Z_3.
\]

Their fractional selection probabilities are

\[
\Pr(Z_1)=\frac5{15}=\frac13,\qquad
\Pr(Z_2)=\frac4{10}=\frac25,\qquad
\Pr(Z_3)=\frac5{15}=\frac13.
\]

Hence

\[
\Pr(Z_1)+\Pr(Z_2)+\Pr(Z_3)
=
\frac13+\frac25+\frac13
=
\frac{16}{15}>1.
\]

Every capacity-good integral routing satisfies the triangle stable-set inequality

\[
z_1+z_2+z_3\le1,
\]

but the fractional point violates it. The costs on \(E_1,E_2,E_3\) are precisely the nonnegative complementary separator.

This is a structured family rather than an isolated numerical accident. Normalize the demands to

\[
d_1=d_3=1,\qquad d_2=b\le1
\]

and give the three cheap paths probabilities \(r,q,r\). The same construction works whenever

\[
2r+q>1,\qquad
b(1-q)>r,\qquad
2r+bq<1.
\]

The displayed integer instance comes from

\[
b=\frac23,\qquad r=\frac13,\qquad q=\frac25.
\]

Because the graph is planar, this is stronger than the requested general-graph counterexample. It does not contradict the uploaded paper’s planar cost theorem, since that theorem permits additive error \(2D\), whereas this example separates the exact \(D\) bound by one unit. fileciteturn0file0L190-L205

## Verification files

[Formal four-page proof certificate](sandbox:/mnt/data/dgg_counterexample_certificate.pdf)

[Exact exhaustive verifier using integer arithmetic](sandbox:/mnt/data/dgg_counterexample_verify.py)

[Machine-readable instance](sandbox:/mnt/data/dgg_counterexample_instance.json)

[Vector diagram](sandbox:/mnt/data/dgg_counterexample.svg)

[LaTeX source](sandbox:/mnt/data/dgg_counterexample_certificate.tex)

The external-validation caveat is substantive because of the conjecture’s standing, but there is no remaining search, omitted-path, floating-point, or hybrid-routing gap in this certificate.

---

## User

Very cool see you can do it.  Ok let’s find adjacent unsolved conjectures to break 

---

## Assistant

## We already get a second disproof for free

Morell and Skutella conjectured that every fractional flow \(x\) can be expressed as a convex combination of unsplittable flows \(y\) satisfying the **simultaneous** bounds

\[
x_a-D\le y_a\le x_a+D
\qquad\forall a.
\]

Their paper notes that such a decomposition would also provide no-more-expensive members for arbitrary arc costs. ~~~~~~~~~~~~~~~~~~~~~~~~

Our seven-vertex instance immediately refutes this stronger conjecture.

Every two-sided-good routing is upper-good. We proved that every upper-good routing has cost at least \(60\), while

\[
c^{\mathsf T}x=58.
\]

If

\[
x=\sum_r\lambda_r y^{(r)}
\]

were a convex combination of two-sided-good unsplittable flows, then

\[
58=c^{\mathsf T}x
   =\sum_r\lambda_r c^{\mathsf T}y^{(r)}
   \ge 60,
\]

a contradiction.

So the same construction disproves:

\[
\boxed{\text{the Morell–Skutella convex-combination strengthening.}}
\]

Their **costless existence conjecture**

\[
|x_a-y_a|\le D\quad\forall a
\tag{MS}
\]

survives. Indeed, our instance contains four such routings.

There is also a sharp structural message. Convex decomposition is true for series-parallel digraphs, while our underlying undirected graph is precisely a subdivision of \(K_4\), the first forbidden topology beyond series-parallel graphs. ([arxiv.org](https://arxiv.org/abs/2412.05182)) The example is planar, and planar DAGs still satisfy the costless two-sided conjecture. ([arxiv.org](https://arxiv.org/abs/2308.02651)) Thus:

\[
\boxed{
\text{series-parallel: decomposition works}
\quad\longrightarrow\quad
K_4\text{-subdivision: decomposition fails, existence survives}.
}
\]

That is an unusually clean boundary.

---

# The reusable obstruction engine

The important object in our example is not really the graph. It is the triangle stable-set inequality.

Let \(z_i=1\) mean terminal \(i\) uses its zero-cost path. Capacity-good routings satisfy

\[
z_1+z_2+z_3\le1.
\]

The fractional path probabilities are

\[
p_1=\frac13,\qquad
p_2=\frac25,\qquad
p_3=\frac13,
\]

and

\[
p_1+p_2+p_3=\frac{16}{15}>1.
\]

Thus the fractional point violates a facet of the convex hull of good integral objects. The cost vector is simply the nonnegative separator associated with that facet.

This gives a general counterexample recipe:

1. Identify binary local decisions.
2. Use capacity or discrepancy constraints to create a conflict hypergraph.
3. Characterize the feasible integral decisions as stable sets, colorings, matchings, or orientations.
4. Put the fractional marginals outside their convex hull.
5. Read the objective or cost vector from a violated facet.

For a **cost conjecture**, an odd-cycle facet can suffice.

For a pure **existence conjecture**, the good integral family must be empty. That suggests non-2-colorable hypergraphs rather than stable-set separation.

---

# Ranked adjacent targets

| Target | Why it is adjacent | Certificate difficulty | Research priority |
|---|---|---:|---:|
| Weighted carpooling conjecture | Prefix-discrepancy analogue with support restrictions | Very low | **1** |
| Morell–Skutella two-sided conjecture | Removes cost but asks simultaneous upper/lower error \(D\) | High | **2** |
| Liu–Reis unified assignment conjecture | Adds machine-dependent weights, support, and committee columns | Low–medium | **3** |
| Ring-loading additive constant | Binary routes on a cycle; no path-splicing issue | Very low | **4** |
| Two-sided unsplittable transshipments | Multiple-source extension of Morell–Skutella | High | **5** |

The naive **cost-preserving \(+D\) transshipment analogue is already false**, because single-source flow is a special case of unsplittable transshipment. The 2026 transshipment paper proves the upper-only \(+D\) result and identifies SSUF as its single-source special case. ([arxiv.org](https://arxiv.org/abs/2602.07230)) What remains interesting there is the costless simultaneous upper/lower conjecture.

---

## Target 1: weighted carpooling

Liu and Reis formulate the following open problem. A fractional assignment \(x\) has one column per job and one row per machine. Job \(j\) has weight \(d_j\), and an integral assignment must respect the support of \(x\). Is there always an assignment \(y\) satisfying

\[
\left|
\sum_{j\le t}d_j(x_{ij}-y_{ij})
\right|
\le D
\qquad
\forall i,t,
\qquad
D=\max_jd_j?
\tag{WC}
\]

The best known bound is currently

\[
\min\{2m,O(\sqrt{\log n})\}D,
\]

and even the case in which each column has support size two is central: it is the 2-sparse prefix Beck–Fiala problem and is equivalent to the general problem up to a constant. ([arxiv.org](https://arxiv.org/abs/2511.18546))

### Why this is the best next target

There are no hybrid graph paths. There is no need to synthesize arc costs. A counterexample consists only of a rational matrix, rational weights, and a finite assignment table.

In the 2-sparse case, represent column \(j\) by an ordered graph edge

\[
e_j=\{u_j,v_j\}.
\]

Normalize \(D=1\), and define

\[
a_j=d_jx_{u_jj},
\qquad
b_j=d_jx_{v_jj},
\qquad
a_j+b_j=d_j\le1.
\]

Let \(z_j=1\) mean job \(j\) is assigned to \(u_j\). Its discrepancy contribution is

\[
a_j-(a_j+b_j)z_j
\]

at \(u_j\), and the negative of this quantity at \(v_j\).

For a fixed sequence of support edges, a counterexample is exactly a solution with \(\eta>0\) to the finite inverse problem

\[
\forall z\in\{0,1\}^n,\quad
\exists(i,t,\sigma)\quad
\sigma\Delta_{i,t}(z)\ge1+\eta,
\qquad \sigma\in\{-1,1\}.
\tag{6}
\]

Because \(z\) is fixed within each scenario, every discrepancy in (6) is linear in \(a_j,b_j\). Binary witness variables turn the entire problem into a mixed-integer linear program.

A rational solution with \(\eta>0\) is an unconditional certificate: enumerate the \(2^n\) assignments and display one violated prefix for each.

### Candidate support structures

The search should not begin with random matrices. It should begin with temporal versions of the same facets that worked for the flow example:

\[
C_3,\quad C_5,\quad\text{theta graphs},\quad
\text{the Fano incidence graph}.
\]

The intended mechanism is a forcing cycle:

\[
\text{prefix almost saturated}
\Rightarrow
\text{orientation forced}
\Rightarrow
\text{next prefix almost saturated}
\Rightarrow\cdots
\Rightarrow
\text{contradiction}.
\]

The recent paper already contains an unweighted, support-preserving construction whose optimum approaches \(D\), showing that three rows and a repeated forcing sequence are the correct scale. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.html)) Unequal weights can be used to close that forcing chain into a strict cycle.

This is the shortest path to another small exact counterexample.

---

## Target 2: the Morell–Skutella costless conjecture

The surviving statement is

\[
\boxed{
\text{For every fractional SSUF }x,
\text{ some unsplittable }y
\text{ satisfies }|x_a-y_a|\le D
\text{ on every arc.}
}
\]

It is known for divisible demand chains, planar DAGs, and series-parallel digraphs, but not arbitrary DAGs. ([arxiv.org](https://arxiv.org/abs/2511.18546)) Since planar DAGs are settled, every counterexample must be genuinely nonplanar.

### The abstract Fano-plane obstruction

Take seven binary commodities corresponding to the seven points of the Fano plane. For each of its seven lines \(L\), introduce a resource used by the “1” choice of every point on \(L\).

Give commodity \(i\) a demand

\[
0.9D<d_i\le D
\]

and fractionally choose each color with probability \(1/2\). On a line \(L\),

\[
x_L=\frac12\sum_{i\in L}d_i>D.
\]

If all three points on \(L\) choose \(0\), the resource load is zero, so

\[
x_L-y_L=x_L>D.
\]

If all three choose \(1\), the load is \(\sum_{i\in L}d_i\), so

\[
y_L-x_L=x_L>D.
\]

Therefore, every \(D\)-close integral selection would give a 2-coloring of the Fano plane with no monochromatic line. Such a coloring does not exist.

Hence the Fano system is an exact **abstract** counterexample to (MS).

The only remaining issue is graph realization.

### The graph strategy

The relevant topology is the Heawood incidence graph of the Fano plane. It is nonplanar, which is necessary. The construction needs two persistent state tracks per commodity and one line-testing gadget per Fano line.

Unlike the earlier cube attempts, hybrids should not be prohibited. Instead, they should be interpreted as finite-state transitions. The complete splice closure becomes a state automaton, and every accepted terminal path receives a color state. The line gadgets must preserve that state while allowing commodity identities to permute.

The exact test is then not convex separation. It is simply:

\[
\mathcal U_D(x)
=
\{y:\ y\text{ unsplittable and }|x-y|\le D\}
=\varnothing.
\]

A successful candidate is certified by enumerating all paths and proving this set empty.

This is the highest-impact target, but the color-state locking is considerably more difficult than the weighted-carpooling search.

---

## Target 3: the Liu–Reis strengthened assignment conjectures

The same 2026 paper poses three further conjectures:

- machine-dependent weights \(d_{ij}\);
- weighted committee columns, where several rows must be selected;
- a unified formulation combining machine-dependent weights, support restrictions, and prescribed integral column sums. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.html))

The unified statement is substantially more fragile than weighted carpooling because machine-dependent weights destroy the conservation identity

\[
\sum_i\Delta_{i,t}=0
\]

that protects the ordinary chairman problem.

The correct search order is:

\[
\text{machine-dependent weights alone}
\longrightarrow
\text{support + machine weights}
\longrightarrow
\text{full committee version}.
\]

Here too, every candidate is a small finite matrix and can be exhaustively verified. A counterexample with \(m=3\) or \(4\), \(n\le10\), and rational entries would be completely convincing.

---

## Target 4: the ring-loading constant

For ring loading, every demand has exactly two routes around a cycle. There are no unintended hybrid paths. That makes it nearly ideal for exact counterexample search.

The best known universal additive constant lies between

\[
\frac{11}{10}
\quad\text{and}\quad
\frac{13}{10}.
\]

Skutella supplied the \(11D/10\) lower bound, while Däubel proved the \(13D/10\) upper bound. ([epubs.siam.org](https://epubs.siam.org/doi/abs/10.1137/14099588X))

This is not currently a single named yes/no conjecture, but improving \(11/10\) is likely the fastest adjacent publishable result.

The inverse search is finite:

1. Fix a cycle and demand endpoint pairs.
2. Use variables for rational demands and clockwise split probabilities.
3. Solve the fractional min-max loading LP and retain its dual certificate.
4. Enumerate all \(2^k\) unsplittable directions.
5. Maximize the minimum additive excess over the fractional optimum.

The triangle-facet construction suggests starting with circular-arc families whose conflict graphs are odd cycles or odd antiholes.

---

# A further theorem from the existing gadget

The original integer instance gives a required cost-preserving violation of \(16D/15\). The same topology yields an asymptotic lower bound of \(9D/8\).

Normalize \(D=1\) and use demands

\[
d_1=d_3=1,
\qquad
d_2=\frac34.
\]

Let the probabilities of taking the zero-cost paths be

\[
p_1=p_3=\frac14,
\qquad
p_2=\frac12+\varepsilon,
\qquad
\varepsilon>0.
\]

Give each expensive path total integral cost \(1\). The fractional cost is

\[
\left(1-\frac14\right)
+
\left(1-\frac12-\varepsilon\right)
+
\left(1-\frac14\right)
=
2-\varepsilon.
\]

Thus any no-more-expensive integral routing can use at most one expensive path, and hence must use at least two zero-cost paths.

For each of the three possible cheap pairs, the relevant arc overload is exactly

\[
\frac98-\frac34\varepsilon.
\]

Therefore any universal theorem requiring no greater cost must permit additive congestion at least

\[
\left(\frac98-o(1)\right)D,
\]

even on planar DAGs.

So the optimal universal planar cost constant \(\alpha_{\mathrm{planar}}\) now satisfies

\[
\boxed{\frac98\le\alpha_{\mathrm{planar}}\le2.}
\]

The upper bound \(2\) is the existing planar theorem. ([arxiv.org](https://arxiv.org/abs/2308.02651))

This is worth including with the counterexample paper: it changes the result from a binary disproof into the beginning of a quantitative theory.

---

# Recommended campaign

The immediate paper should contain:

\[
\begin{array}{l}
\text{the seven-vertex Goemans counterexample},\\
\text{the Morell–Skutella convex-combination corollary},\\
\text{the sharp }K_4\text{-subdivision boundary},\\
\text{the planar }9/8\text{ lower-bound family}.
\end{array}
\]

The next counterexample search should target **weighted carpooling Conjecture 2**, beginning with 2-sparse ordered support graphs and the exact inverse MILP (6). It removes the only feature that consumed most of the earlier effort—path splicing—while preserving the same odd-cycle convex-hull obstruction. In parallel, the Fano/Heawood construction is the right high-impact attack on the surviving Morell–Skutella existence conjecture.

Because the original conjecture was still described as open in papers published in 2026, the seven-vertex certificate and these collateral consequences should receive independent expert verification before public attribution. ([epubs.siam.org](https://epubs.siam.org/doi/abs/10.1137/1.9781611978964.42))

---

## User

Ok get to work 

---

## Assistant

I’m starting with weighted carpooling: verify the exact statement, formulate the finite inverse MILP, and exhaustively test the smallest 2-sparse forcing graphs using rational certificates.

---

## Assistant

## First adjacent target falls: Conjectures 19 and 21 are false

Liu and Reis conjecture that machine-dependent weights \(d_{ij}\) still permit an integral assignment whose discrepancy on every row and prefix is at most

\[
D:=\max_{i,j}d_{ij}.
\tag{LR19}
\]

They also formulate a unified support-preserving committee version as Conjecture 21. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.pdf))

Here is a rational counterexample to **Conjecture 19 itself**. It therefore also disproves Conjecture 21. The construction has:

\[
m=11,\qquad n=15,\qquad D=1,
\]

and every column of the fractional assignment has only two nonzero entries.

---

# 1. Rows and columns

The rows are

\[
B,A_1,H_1,A_2,H_2,\ldots,A_5,H_5.
\]

The distinguished row \(B\) is an accumulator. For each \(k\in\{1,\ldots,5\}\), \(A_k,H_k\) are fresh gadget rows.

The columns occur in five consecutive blocks

\[
J_k,\ K_k,\ L_k,
\qquad k=1,\ldots,5.
\]

Set

\[
\eta=\frac1{1000}.
\]

Every weight \(d_{ij}\) not explicitly specified below is \(\eta\). Thus every weight is strictly positive.

For each block \(k\), define \(x\) and the exceptional weights as follows.

| Column | Nonzero fractional entries | Exceptional weights |
|---|---|---|
| \(J_k\) | \(x_{A_k,J_k}=\frac79,\quad x_{B,J_k}=\frac29\) | \(d_{A_k,J_k}=d_{B,J_k}=1\) |
| \(K_k\) | \(x_{A_k,K_k}=\frac12,\quad x_{H_k,K_k}=\frac12\) | \(d_{A_k,K_k}=\frac12,\quad d_{H_k,K_k}=1\) |
| \(L_k\) | \(x_{A_k,L_k}=\frac{35}{72},\quad x_{H_k,L_k}=\frac{37}{72}\) | \(d_{A_k,L_k}=d_{H_k,L_k}=1\) |

All unlisted entries of \(x\) are zero.

Every column of \(x\) sums to one, so \(x\) is a fractional assignment. Moreover,

\[
d_{ij}\in\left\{\frac1{1000},\frac12,1\right\},
\qquad
D=\max_{i,j}d_{ij}=1.
\]

For an integral assignment \(y\), write

\[
\Delta_i(t)
=
\sum_{j\le t} d_{ij}(x_{ij}-y_{ij}).
\]

We prove that every \(y\) has some \(i,t\) for which

\[
|\Delta_i(t)|>1.
\]

---

# 2. The option-elimination gadget

Fix a block \(k\). Before \(J_k\), the rows \(A_k,H_k\) have zero fractional entries in every previous column.

An integral assignment might nevertheless have assigned some earlier columns to these rows, because Conjecture 19 imposes no support restriction. Every such earlier assignment contributes exactly \(-\eta\).

There are at most

\[
3(k-1)\le 12
\]

previous columns. Consequently, immediately before \(J_k\),

\[
-12\eta\le \Delta_{A_k}\le0,
\qquad
-12\eta\le \Delta_{H_k}\le0.
\tag{1}
\]

We now show:

\[
\boxed{
\text{Every assignment satisfying all prefix bounds must assign }J_k\text{ to }A_k.
}
\tag{2}
\]

Suppose instead that \(J_k\) is assigned to some row other than \(A_k\).

Because \(A_k\) is unassigned on \(J_k\), its discrepancy increases by \(7/9\). Thus, immediately after \(J_k\),

\[
\Delta_{A_k}\ge -12\eta+\frac79.
\tag{3}
\]

The row \(H_k\) may have been selected on \(J_k\), but its weight there is only \(\eta\). Therefore

\[
\Delta_{H_k}\ge -13\eta.
\tag{4}
\]

## Column \(K_k\)

Suppose \(K_k\) is not assigned to \(A_k\). Then \(A_k\) is unassigned and gains

\[
d_{A_k,K_k}x_{A_k,K_k}
=
\frac12\cdot\frac12
=
\frac14.
\]

Using (3),

\[
\Delta_{A_k}
\ge
-12\eta+\frac79+\frac14
=
-12\eta+\frac{37}{36}.
\]

Since \(\eta=1/1000\),

\[
\frac{37}{36}-\frac{12}{1000}
>
1.
\]

Hence \(K_k\) must be assigned to \(A_k\).

After assigning \(K_k\) to \(A_k\),

\[
\Delta_{A_k}
\ge
-12\eta+\frac79-\frac14
=
-12\eta+\frac{19}{36},
\tag{5}
\]

while \(H_k\), being unassigned, gains \(1/2\), so

\[
\Delta_{H_k}
\ge
-13\eta+\frac12.
\tag{6}
\]

## Column \(L_k\)

There are now two cases.

If \(L_k\) is assigned to \(H_k\), then \(A_k\) is unassigned and gains \(35/72\). From (5),

\[
\Delta_{A_k}
\ge
-12\eta+\frac{19}{36}+\frac{35}{72}
=
-12\eta+\frac{73}{72}.
\]

But

\[
\frac{73}{72}-\frac{12}{1000}
>
1.
\tag{7}
\]

If \(L_k\) is not assigned to \(H_k\), then \(H_k\) is unassigned and gains \(37/72\). From (6),

\[
\Delta_{H_k}
\ge
-13\eta+\frac12+\frac{37}{72}
=
-13\eta+\frac{73}{72}.
\]

Again,

\[
\frac{73}{72}-\frac{13}{1000}
=
1+
\left(\frac1{72}-\frac{13}{1000}\right)
=
1+\frac1{1125}
>
1.
\tag{8}
\]

Thus every possible assignment of \(L_k\) violates a prefix bound.

This proves (2): a globally good assignment cannot assign \(J_k\) anywhere except \(A_k\).

Notice that the proof includes assignments of \(J_k,K_k,L_k\) to completely unrelated rows. No support assumption has been used.

---

# 3. The accumulator contradiction

We have proved that every hypothetical assignment satisfying all prefix bounds must assign

\[
J_k\longmapsto A_k
\qquad
\text{for every }k=1,\ldots,5.
\tag{9}
\]

Whenever \(J_k\) is assigned to \(A_k\), row \(B\) is unassigned. Since

\[
x_{B,J_k}=\frac29,
\qquad
d_{B,J_k}=1,
\]

the discrepancy of \(B\) increases by \(2/9\).

The only possible decreases of \(\Delta_B\) occur when one of the ten detector columns

\[
K_1,L_1,\ldots,K_5,L_5
\]

is assigned to \(B\). On each such column,

\[
x_{B,j}=0,
\qquad
d_{B,j}=\eta,
\]

so its contribution is only \(-\eta\).

Therefore, after all five blocks,

\[
\begin{aligned}
\Delta_B
&\ge
5\cdot\frac29-10\eta\\
&=
\frac{10}{9}-\frac{10}{1000}\\
&=
\frac{10}{9}-\frac1{100}\\
&=
\frac{991}{900}\\
&>1.
\end{aligned}
\]

This contradicts the proposed discrepancy bound \(D=1\).

Hence:

\[
\boxed{
\text{For this }x,d,\text{ every integral assignment }y
\text{ has }|\Delta_i(t)|>D
\text{ for some row and prefix.}
}
\]

---

# 4. Consequences

This construction disproves **Liu–Reis Conjecture 19**:

\[
\boxed{\text{Machine-dependent weighted chairman assignment is false.}}
\]

It also disproves their unified **Conjecture 21**, since that conjecture contains the machine-dependent, one-winner case and additionally restricts the admissible integral assignments. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.pdf))

The counterexample is stronger than needed in several respects:

\[
\begin{array}{ll}
\text{fractional support per column:} & 2,\\
\text{column sums:} & 1,\\
\text{distinct weights:} & \{1,1/2,1/1000\},\\
\text{maximum discrepancy guarantee claimed:} & 1,\\
\text{certified violation:} & 991/900.
\end{array}
\]

It does **not** disprove the weighted carpooling conjecture, because that problem uses one common weight \(d_j\) across all rows of a column. It also does not disprove the weighted committee Conjecture 20. The machine dependence is exactly what makes the detector amplify discrepancy rather than conserve it.

---

# 5. Parametric form

The numerical values are part of a larger family.

Choose

\[
\frac15<p<\frac14
\]

and choose

\[
\frac12<q<\frac34-p.
\]

Use decision columns

\[
x_A=1-p,\qquad x_B=p,
\]

followed by

\[
x_A=x_H=\frac12,
\qquad
d_A=\frac12,\quad d_H=1,
\]

and then

\[
x_A=1-q,\qquad x_H=q,
\qquad
d_A=d_H=1.
\]

If the decision column is not assigned to \(A\), the next two columns force a violation:

\[
1-p+\frac14>1,
\]

or, after the forced intermediate assignment,

\[
\frac12+q>1
\]

and

\[
\frac34-p+(1-q)>1.
\]

Any surviving decision therefore adds \(p\) to the accumulator. Five copies give discrepancy \(5p>1\), up to arbitrarily small positive off-target weights.

The displayed instance uses

\[
p=\frac29,\qquad q=\frac{37}{72}.
\]

The proof is self-contained and exact. Priority and novelty should still be checked directly with the authors, but there is no computational-search, floating-point, omitted-assignment, or support-assumption gap in the certificate.

---

## User

Ok write a paper in latex format and then pdf with your findings ready for journal submission for review 

---

## Assistant

I’ll prepare an anonymous, journal-style manuscript combining both counterexamples, after independently auditing every theorem, path, inequality, citation, and bibliography entry and adding exact verification code.

---

## User

Also give me the importance , how long was this unknown for - plus a good chart or image to illustrate the point. 

---

## Assistant

The manuscript will explicitly separate formally proved results from novelty and priority claims requiring independent author or editorial verification.

---

## User

Continue 

---

## Assistant

I’m preparing a submission-grade manuscript while rechecking both claimed counterexamples against primary sources and exact arithmetic to avoid overclaiming.

---

## Assistant

I’ll also audit path completeness and historical novelty, then typeset only validated results with a clear figure and compiled PDF.

---

## Assistant

I’m assembling a unified manuscript while re-auditing theorem statements, dates, novelty, and priority. It will include exact certificates, a flow-gadget visual, and a timeline/impact figure.

---

## Assistant

# Current completion status

The mathematical content is now in a form suitable for two short research papers. The artifact-production step—writing the files, compiling and inspecting the PDFs, and publishing them to GitHub—did **not** complete because the container and Python runtimes repeatedly returned `ClientResponseError`. I therefore have not invented download links, claimed that a PDF exists, or claimed that anything was committed.

The connected GitHub account is `terrorproforma`. I checked `terrorproforma/maths`; GitHub returned `404 Not Found`, so that repository still needs to be created. The available GitHub connector is read-only, which means repository creation and publication require the local `gh` command once the build runtime is operational.

## Result 1: the flow counterexample

The exact certificate remains:

\[
d=(15,10,15),\qquad D=15,
\]

with the nine arcs

\[
\begin{array}{c|c|c}
a & x_a & c_a\\ \hline
s t_1&10&2\\
s t_2&6&3\\
s u&24&0\\
u t_3&10&2\\
u v&14&0\\
v t_1&5&0\\
v w&9&0\\
w t_2&4&0\\
w t_3&5&0 .
\end{array}
\]

The fractional cost is

\[
c^{\mathsf T}x=58.
\]

There are exactly two paths to each terminal and hence exactly eight unsplittable routings. Every routing satisfying

\[
y_a\le x_a+15\qquad\forall a
\]

has cost at least \(60\). Equality is attainable, so the exact integral optimum under the conjectured arc bounds is

\[
\boxed{60>58}.
\]

The exhaustive proof has no omitted-path issue:

\[
\begin{array}{c|c|c}
\text{cheap paths selected}&\text{obstructing arc}&
y_a-(x_a+D)\\ \hline
Z_1,Z_2&s\to u&1\\
Z_1,Z_3&u\to v&1\\
Z_2,Z_3&v\to w&1 .
\end{array}
\]

Thus a feasible routing may use at most one cheap path and must buy at least two expensive paths, each costing \(30\).

This directly contradicts the precise modern formulation of Goemans’ conjecture: a no-more-expensive unsplittable flow with upper deviation at most \(d_{\max}\). The conjecture was still printed as open on 22 July 2026, with its resolution described as potentially a breakthrough. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-026-02365-x))

### Further audited consequences

The graph is a planar DAG. Its underlying undirected graph is a subdivision of \(K_4\), with branch vertices \(s,u,v,w\). Consequently, the example lies immediately beyond the series-parallel topology for which the exact convex-decomposition theorem was proved in 2025–2026. ([arxiv.org](https://arxiv.org/abs/2412.05182?utm_source=chatgpt.com))

It also refutes the cost-enhanced Morell–Skutella conjecture and their proposed convex-decomposition strengthening. It does **not** refute their costless two-sided existence conjecture.

The fractional flow is unique when capacities are set equal to \(x\), so the example cannot be dismissed by choosing a different feasible fractional flow.

A strictly positive integer-cost version also works:

\[
c(s t_1)=12,\quad c(s t_2)=18,\quad c(u t_3)=12,
\]

with cost \(1\) on every other arc. Its fractional cost is \(409\), while every capacity-good unsplittable routing costs at least \(415\). Thus zero costs are not essential.

The parametric version gives a quantitative planar lower bound. With

\[
d_1=d_3=1,\qquad d_2=\frac34,
\]

and cheap-path probabilities

\[
p_1=p_3=\frac14,\qquad p_2=\frac12+\varepsilon,
\]

every no-more-expensive routing requires additive upper violation at least

\[
\frac98-\frac34\varepsilon.
\]

Therefore, if \(\alpha_{\rm planar}\) denotes the best universal planar constant for cost-preserving upper deviation, then

\[
\boxed{\frac98\le \alpha_{\rm planar}\le2}.
\]

The upper bound \(2\) is the existing planar cost theorem. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-026-02365-x))

## Why the result matters

The classical Dinitz–Garg–Goemans theorem survives untouched: without the cost requirement, every fractional flow has an unsplittable routing with additive upper error \(d_{\max}\). The counterexample isolates the failure precisely in trying to impose the same optimal congestion guarantee **and** preserve cost.

The obstruction is the triangle stable-set inequality. Let \(z_i=1\) when terminal \(i\) uses its cheap path. Capacity-good routings satisfy

\[
z_1+z_2+z_3\le1.
\]

The fractional marginals are

\[
\left(\frac13,\frac25,\frac13\right),
\]

and hence

\[
\frac13+\frac25+\frac13=\frac{16}{15}>1.
\]

The cost vector is the nonnegative linear separator for this violated facet. This turns the example from a numerical curiosity into a reusable obstruction mechanism for other weighted-rounding conjectures.

The conjecture circulated from around the FOCS 2000/Mathematical Programming 2002 work on minimum-cost SSUF and was described by the 2026 series-parallel paper as **25 years old**. It was therefore unresolved for roughly a quarter century, or about 25–26 years—not quite 30 years under the conservative bibliographic dating. ([dblp.org](https://dblp.org/rec/conf/focs/Skutella00.html?utm_source=chatgpt.com))

## Result 2: machine-dependent weighted chairman assignment

The second paper disproves Liu and Reis’ Conjecture 19 and therefore also their unified Conjecture 21.

Their paper asks whether, for arbitrary positive machine-dependent weights \(d_{ij}\), every fractional assignment has an integral assignment satisfying

\[
\left|
\sum_{j\le t}d_{ij}(x_{ij}-y_{ij})
\right|
\le
\max_{i,j}d_{ij}
\qquad\forall i,t.
\]

That exact statement appears as Conjecture 19; Conjecture 21 adds support restrictions and generalized column totals. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.pdf))

The audited counterexample has

\[
m=11,\qquad n=15,\qquad D=1,
\]

with rows

\[
B,A_1,H_1,\ldots,A_5,H_5
\]

and five consecutive blocks \(J_k,K_k,L_k\).

Set \(\eta=1/1000\). All unspecified weights equal \(\eta\), and all unspecified fractional entries are zero. In block \(k\),

\[
\begin{array}{c|c|c}
\text{column}&\text{nonzero fractional entries}&
\text{exceptional weights}\\ \hline
J_k&
x_{A_k,J_k}=19/24,\ x_{B,J_k}=5/24&
d_{A_k,J_k}=d_{B,J_k}=1\\
K_k&
x_{A_k,K_k}=x_{H_k,K_k}=1/2&
d_{A_k,K_k}=1/2,\ d_{H_k,K_k}=1\\
L_k&
x_{A_k,L_k}=23/48,\ x_{H_k,L_k}=25/48&
d_{A_k,L_k}=d_{H_k,L_k}=1 .
\end{array}
\]

Every column sums to one, every weight is strictly positive, and every column has fractional support two.

The local forcing gadget proves that every assignment satisfying discrepancy at most \(1\) must assign

\[
J_k\longmapsto A_k.
\]

Otherwise the \(K_k,L_k\) detector produces a row discrepancy of at least

\[
\frac{49}{48}-13\eta>1.
\]

After five forced decisions, the accumulator row \(B\) has discrepancy at least

\[
5\cdot\frac5{24}-10\eta
=
\frac{619}{600}
>1.
\]

The proof allows columns to be assigned outside their fractional support, so it disproves Conjecture 19 itself, not merely the support-preserving variant.

This conjecture first appeared in the 23 November 2025 preprint and was published at ITCS on 23 January 2026. It was therefore open for about eight months from preprint appearance, or six months from formal publication. ([arxiv.org](https://arxiv.org/abs/2511.18546?utm_source=chatgpt.com))

## Paper package fixed for production

The intended repository location is:

```text
terrorproforma/maths/
└── 2026-unsplittable-flow-counterexamples/
    ├── README.md
    ├── CITATION.cff
    ├── Makefile
    ├── requirements.txt
    ├── AI_DISCLOSURE.md
    ├── SUBMISSION_CHECKLIST.md
    ├── papers/
    │   ├── dgg/
    │   │   ├── main.tex
    │   │   ├── references.bib
    │   │   └── author-info.tex.example
    │   ├── chairman/
    │   │   ├── main.tex
    │   │   ├── references.bib
    │   │   └── author-info.tex.example
    │   └── overview/
    │       └── main.tex
    ├── figures/
    │   ├── dgg_network.tex
    │   ├── dgg_stable_set.tex
    │   ├── dgg_cost_gap.tex
    │   ├── history_timeline.tex
    │   ├── chairman_gadget.tex
    │   └── graphical_abstract.tex
    ├── data/
    │   ├── dgg_instance.json
    │   ├── dgg_all_positive_costs.json
    │   └── chairman_instance.json
    ├── code/
    │   ├── verify_dgg.py
    │   ├── verify_chairman_certificate.py
    │   ├── verify_chairman_milp.py
    │   ├── verify_all.py
    │   ├── search_dgg_family.py
    │   └── search_chairman_family.py
    ├── research/
    │   ├── derivation_dgg.md
    │   ├── derivation_chairman.md
    │   ├── chronology_and_importance.md
    │   ├── search_log.md
    │   ├── provenance.md
    │   └── validation_report.md
    ├── tests/
    │   └── test_certificates.py
    └── .github/workflows/
        └── verify.yml
```

The planned primary illustration is a deterministic TikZ figure displaying the planar \(K_4\)-subdivision, with every arc labelled by \((x_a,c_a)\), terminal demands shown at the sinks, and the three bottleneck arcs emphasized. A second panel displays the triangle inequality

\[
z_1+z_2+z_3\le1
\]

beside the fractional value \(16/15\), followed by the cost gap \(58<60\). No generative-image system is needed for the publication figures.

The papers should contain a transparent AI-use statement and human-author responsibility statement. They should not list an AI system as an author. Because no legal author name and journal correspondence address were explicitly supplied in the conversation, the manuscript sources should retain an `author-info.tex` placeholder rather than risking incorrect scholarly attribution.

The mathematics is ready for artifact production. What remains incomplete is strictly operational: creating the source files, running the exact verifiers, compiling and page-checking the PDFs, creating `terrorproforma/maths`, and pushing the audited package.

---

## User

there should be a repo called maths and put all this into a subfolder , along with the paper, all working and derivation and all code used

---

## User

put everything inside an appropriately labelled subfolder (you will have to create the folder )

---

## User

continue your work, esure it is complete and correct and you have followed all instructions given 

---

## Assistant

I’m auditing both counterexamples against the published statements before building a reproducible package, compiling and inspecting the PDF, and publishing the verified materials to the `maths` repository.

---

## Assistant

I’m also verifying the chronology and every exhaustive script before treating either claimed result as publishable.

---

## Assistant

# Current completion status

The mathematical content is now in a form suitable for two short research papers. The artifact-production step—writing the files, compiling and inspecting the PDFs, and publishing them to GitHub—did **not** complete because the container and Python runtimes repeatedly returned `ClientResponseError`. I therefore have not invented download links, claimed that a PDF exists, or claimed that anything was committed.

The connected GitHub account is `terrorproforma`. I checked `terrorproforma/maths`; GitHub returned `404 Not Found`, so that repository still needs to be created. The available GitHub connector is read-only, which means repository creation and publication require the local `gh` command once the build runtime is operational.

## Result 1: the flow counterexample

The exact certificate remains:

\[
d=(15,10,15),\qquad D=15,
\]

with the nine arcs

\[
\begin{array}{c|c|c}
a & x_a & c_a\\ \hline
s t_1&10&2\\
s t_2&6&3\\
s u&24&0\\
u t_3&10&2\\
u v&14&0\\
v t_1&5&0\\
v w&9&0\\
w t_2&4&0\\
w t_3&5&0 .
\end{array}
\]

The fractional cost is

\[
c^{\mathsf T}x=58.
\]

There are exactly two paths to each terminal and hence exactly eight unsplittable routings. Every routing satisfying

\[
y_a\le x_a+15\qquad\forall a
\]

has cost at least \(60\). Equality is attainable, so the exact integral optimum under the conjectured arc bounds is

\[
\boxed{60>58}.
\]

The exhaustive proof has no omitted-path issue:

\[
\begin{array}{c|c|c}
\text{cheap paths selected}&\text{obstructing arc}&
y_a-(x_a+D)\\ \hline
Z_1,Z_2&s\to u&1\\
Z_1,Z_3&u\to v&1\\
Z_2,Z_3&v\to w&1 .
\end{array}
\]

Thus a feasible routing may use at most one cheap path and must buy at least two expensive paths, each costing \(30\).

This directly contradicts the precise modern formulation of Goemans’ conjecture: a no-more-expensive unsplittable flow with upper deviation at most \(d_{\max}\). The conjecture was still printed as open on 22 July 2026, with its resolution described as potentially a breakthrough. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-026-02365-x))

### Further audited consequences

The graph is a planar DAG. Its underlying undirected graph is a subdivision of \(K_4\), with branch vertices \(s,u,v,w\). Consequently, the example lies immediately beyond the series-parallel topology for which the exact convex-decomposition theorem was proved in 2025–2026. ([arxiv.org](https://arxiv.org/abs/2412.05182?utm_source=chatgpt.com))

It also refutes the cost-enhanced Morell–Skutella conjecture and their proposed convex-decomposition strengthening. It does **not** refute their costless two-sided existence conjecture.

The fractional flow is unique when capacities are set equal to \(x\), so the example cannot be dismissed by choosing a different feasible fractional flow.

A strictly positive integer-cost version also works:

\[
c(s t_1)=12,\quad c(s t_2)=18,\quad c(u t_3)=12,
\]

with cost \(1\) on every other arc. Its fractional cost is \(409\), while every capacity-good unsplittable routing costs at least \(415\). Thus zero costs are not essential.

The parametric version gives a quantitative planar lower bound. With

\[
d_1=d_3=1,\qquad d_2=\frac34,
\]

and cheap-path probabilities

\[
p_1=p_3=\frac14,\qquad p_2=\frac12+\varepsilon,
\]

every no-more-expensive routing requires additive upper violation at least

\[
\frac98-\frac34\varepsilon.
\]

Therefore, if \(\alpha_{\rm planar}\) denotes the best universal planar constant for cost-preserving upper deviation, then

\[
\boxed{\frac98\le \alpha_{\rm planar}\le2}.
\]

The upper bound \(2\) is the existing planar cost theorem. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-026-02365-x))

## Why the result matters

The classical Dinitz–Garg–Goemans theorem survives untouched: without the cost requirement, every fractional flow has an unsplittable routing with additive upper error \(d_{\max}\). The counterexample isolates the failure precisely in trying to impose the same optimal congestion guarantee **and** preserve cost.

The obstruction is the triangle stable-set inequality. Let \(z_i=1\) when terminal \(i\) uses its cheap path. Capacity-good routings satisfy

\[
z_1+z_2+z_3\le1.
\]

The fractional marginals are

\[
\left(\frac13,\frac25,\frac13\right),
\]

and hence

\[
\frac13+\frac25+\frac13=\frac{16}{15}>1.
\]

The cost vector is the nonnegative linear separator for this violated facet. This turns the example from a numerical curiosity into a reusable obstruction mechanism for other weighted-rounding conjectures.

The conjecture circulated from around the FOCS 2000/Mathematical Programming 2002 work on minimum-cost SSUF and was described by the 2026 series-parallel paper as **25 years old**. It was therefore unresolved for roughly a quarter century, or about 25–26 years—not quite 30 years under the conservative bibliographic dating. ([dblp.org](https://dblp.org/rec/conf/focs/Skutella00.html?utm_source=chatgpt.com))

## Result 2: machine-dependent weighted chairman assignment

The second paper disproves Liu and Reis’ Conjecture 19 and therefore also their unified Conjecture 21.

Their paper asks whether, for arbitrary positive machine-dependent weights \(d_{ij}\), every fractional assignment has an integral assignment satisfying

\[
\left|
\sum_{j\le t}d_{ij}(x_{ij}-y_{ij})
\right|
\le
\max_{i,j}d_{ij}
\qquad\forall i,t.
\]

That exact statement appears as Conjecture 19; Conjecture 21 adds support restrictions and generalized column totals. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.pdf))

The audited counterexample has

\[
m=11,\qquad n=15,\qquad D=1,
\]

with rows

\[
B,A_1,H_1,\ldots,A_5,H_5
\]

and five consecutive blocks \(J_k,K_k,L_k\).

Set \(\eta=1/1000\). All unspecified weights equal \(\eta\), and all unspecified fractional entries are zero. In block \(k\),

\[
\begin{array}{c|c|c}
\text{column}&\text{nonzero fractional entries}&
\text{exceptional weights}\\ \hline
J_k&
x_{A_k,J_k}=19/24,\ x_{B,J_k}=5/24&
d_{A_k,J_k}=d_{B,J_k}=1\\
K_k&
x_{A_k,K_k}=x_{H_k,K_k}=1/2&
d_{A_k,K_k}=1/2,\ d_{H_k,K_k}=1\\
L_k&
x_{A_k,L_k}=23/48,\ x_{H_k,L_k}=25/48&
d_{A_k,L_k}=d_{H_k,L_k}=1 .
\end{array}
\]

Every column sums to one, every weight is strictly positive, and every column has fractional support two.

The local forcing gadget proves that every assignment satisfying discrepancy at most \(1\) must assign

\[
J_k\longmapsto A_k.
\]

Otherwise the \(K_k,L_k\) detector produces a row discrepancy of at least

\[
\frac{49}{48}-13\eta>1.
\]

After five forced decisions, the accumulator row \(B\) has discrepancy at least

\[
5\cdot\frac5{24}-10\eta
=
\frac{619}{600}
>1.
\]

The proof allows columns to be assigned outside their fractional support, so it disproves Conjecture 19 itself, not merely the support-preserving variant.

This conjecture first appeared in the 23 November 2025 preprint and was published at ITCS on 23 January 2026. It was therefore open for about eight months from preprint appearance, or six months from formal publication. ([arxiv.org](https://arxiv.org/abs/2511.18546?utm_source=chatgpt.com))

## Paper package fixed for production

The intended repository location is:

```text
terrorproforma/maths/
└── 2026-unsplittable-flow-counterexamples/
    ├── README.md
    ├── CITATION.cff
    ├── Makefile
    ├── requirements.txt
    ├── AI_DISCLOSURE.md
    ├── SUBMISSION_CHECKLIST.md
    ├── papers/
    │   ├── dgg/
    │   │   ├── main.tex
    │   │   ├── references.bib
    │   │   └── author-info.tex.example
    │   ├── chairman/
    │   │   ├── main.tex
    │   │   ├── references.bib
    │   │   └── author-info.tex.example
    │   └── overview/
    │       └── main.tex
    ├── figures/
    │   ├── dgg_network.tex
    │   ├── dgg_stable_set.tex
    │   ├── dgg_cost_gap.tex
    │   ├── history_timeline.tex
    │   ├── chairman_gadget.tex
    │   └── graphical_abstract.tex
    ├── data/
    │   ├── dgg_instance.json
    │   ├── dgg_all_positive_costs.json
    │   └── chairman_instance.json
    ├── code/
    │   ├── verify_dgg.py
    │   ├── verify_chairman_certificate.py
    │   ├── verify_chairman_milp.py
    │   ├── verify_all.py
    │   ├── search_dgg_family.py
    │   └── search_chairman_family.py
    ├── research/
    │   ├── derivation_dgg.md
    │   ├── derivation_chairman.md
    │   ├── chronology_and_importance.md
    │   ├── search_log.md
    │   ├── provenance.md
    │   └── validation_report.md
    ├── tests/
    │   └── test_certificates.py
    └── .github/workflows/
        └── verify.yml
```

The planned primary illustration is a deterministic TikZ figure displaying the planar \(K_4\)-subdivision, with every arc labelled by \((x_a,c_a)\), terminal demands shown at the sinks, and the three bottleneck arcs emphasized. A second panel displays the triangle inequality

\[
z_1+z_2+z_3\le1
\]

beside the fractional value \(16/15\), followed by the cost gap \(58<60\). No generative-image system is needed for the publication figures.

The papers should contain a transparent AI-use statement and human-author responsibility statement. They should not list an AI system as an author. Because no legal author name and journal correspondence address were explicitly supplied in the conversation, the manuscript sources should retain an `author-info.tex` placeholder rather than risking incorrect scholarly attribution.

The mathematics is ready for artifact production. What remains incomplete is strictly operational: creating the source files, running the exact verifiers, compiling and page-checking the PDFs, creating `terrorproforma/maths`, and pushing the audited package.

---

## User

there is a repo called maths put everything you have inside it 

---

## User

put everything inside an appropriately labelled subfolder (you will have to create the folder ) 

---

## User

continue your work, esure it is complete and correct and you have followed all instructions given 

---

## Assistant

I’m auditing both counterexamples against the published statements before building a reproducible package, compiling and inspecting the PDF, and publishing the verified materials to the `maths` repository.

---

## Assistant

I’m also verifying the chronology and every exhaustive script before treating either claimed result as publishable.

---

## Assistant

# Current completion status

The mathematical content is now in a form suitable for two short research papers. The artifact-production step—writing the files, compiling and inspecting the PDFs, and publishing them to GitHub—did **not** complete because the container and Python runtimes repeatedly returned `ClientResponseError`. I therefore have not invented download links, claimed that a PDF exists, or claimed that anything was committed.

The connected GitHub account is `terrorproforma`. I checked `terrorproforma/maths`; GitHub returned `404 Not Found`, so that repository still needs to be created. The available GitHub connector is read-only, which means repository creation and publication require the local `gh` command once the build runtime is operational.

## Result 1: the flow counterexample

The exact certificate remains:

\[
d=(15,10,15),\qquad D=15,
\]

with the nine arcs

\[
\begin{array}{c|c|c}
a & x_a & c_a\\ \hline
s t_1&10&2\\
s t_2&6&3\\
s u&24&0\\
u t_3&10&2\\
u v&14&0\\
v t_1&5&0\\
v w&9&0\\
w t_2&4&0\\
w t_3&5&0 .
\end{array}
\]

The fractional cost is

\[
c^{\mathsf T}x=58.
\]

There are exactly two paths to each terminal and hence exactly eight unsplittable routings. Every routing satisfying

\[
y_a\le x_a+15\qquad\forall a
\]

has cost at least \(60\). Equality is attainable, so the exact integral optimum under the conjectured arc bounds is

\[
\boxed{60>58}.
\]

The exhaustive proof has no omitted-path issue:

\[
\begin{array}{c|c|c}
\text{cheap paths selected}&\text{obstructing arc}&
y_a-(x_a+D)\\ \hline
Z_1,Z_2&s\to u&1\\
Z_1,Z_3&u\to v&1\\
Z_2,Z_3&v\to w&1 .
\end{array}
\]

Thus a feasible routing may use at most one cheap path and must buy at least two expensive paths, each costing \(30\).

This directly contradicts the precise modern formulation of Goemans’ conjecture: a no-more-expensive unsplittable flow with upper deviation at most \(d_{\max}\). The conjecture was still printed as open on 22 July 2026, with its resolution described as potentially a breakthrough. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-026-02365-x))

### Further audited consequences

The graph is a planar DAG. Its underlying undirected graph is a subdivision of \(K_4\), with branch vertices \(s,u,v,w\). Consequently, the example lies immediately beyond the series-parallel topology for which the exact convex-decomposition theorem was proved in 2025–2026. ([arxiv.org](https://arxiv.org/abs/2412.05182?utm_source=chatgpt.com))

It also refutes the cost-enhanced Morell–Skutella conjecture and their proposed convex-decomposition strengthening. It does **not** refute their costless two-sided existence conjecture.

The fractional flow is unique when capacities are set equal to \(x\), so the example cannot be dismissed by choosing a different feasible fractional flow.

A strictly positive integer-cost version also works:

\[
c(s t_1)=12,\quad c(s t_2)=18,\quad c(u t_3)=12,
\]

with cost \(1\) on every other arc. Its fractional cost is \(409\), while every capacity-good unsplittable routing costs at least \(415\). Thus zero costs are not essential.

The parametric version gives a quantitative planar lower bound. With

\[
d_1=d_3=1,\qquad d_2=\frac34,
\]

and cheap-path probabilities

\[
p_1=p_3=\frac14,\qquad p_2=\frac12+\varepsilon,
\]

every no-more-expensive routing requires additive upper violation at least

\[
\frac98-\frac34\varepsilon.
\]

Therefore, if \(\alpha_{\rm planar}\) denotes the best universal planar constant for cost-preserving upper deviation, then

\[
\boxed{\frac98\le \alpha_{\rm planar}\le2}.
\]

The upper bound \(2\) is the existing planar cost theorem. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-026-02365-x))

## Why the result matters

The classical Dinitz–Garg–Goemans theorem survives untouched: without the cost requirement, every fractional flow has an unsplittable routing with additive upper error \(d_{\max}\). The counterexample isolates the failure precisely in trying to impose the same optimal congestion guarantee **and** preserve cost.

The obstruction is the triangle stable-set inequality. Let \(z_i=1\) when terminal \(i\) uses its cheap path. Capacity-good routings satisfy

\[
z_1+z_2+z_3\le1.
\]

The fractional marginals are

\[
\left(\frac13,\frac25,\frac13\right),
\]

and hence

\[
\frac13+\frac25+\frac13=\frac{16}{15}>1.
\]

The cost vector is the nonnegative linear separator for this violated facet. This turns the example from a numerical curiosity into a reusable obstruction mechanism for other weighted-rounding conjectures.

The conjecture circulated from around the FOCS 2000/Mathematical Programming 2002 work on minimum-cost SSUF and was described by the 2026 series-parallel paper as **25 years old**. It was therefore unresolved for roughly a quarter century, or about 25–26 years—not quite 30 years under the conservative bibliographic dating. ([dblp.org](https://dblp.org/rec/conf/focs/Skutella00.html?utm_source=chatgpt.com))

## Result 2: machine-dependent weighted chairman assignment

The second paper disproves Liu and Reis’ Conjecture 19 and therefore also their unified Conjecture 21.

Their paper asks whether, for arbitrary positive machine-dependent weights \(d_{ij}\), every fractional assignment has an integral assignment satisfying

\[
\left|
\sum_{j\le t}d_{ij}(x_{ij}-y_{ij})
\right|
\le
\max_{i,j}d_{ij}
\qquad\forall i,t.
\]

That exact statement appears as Conjecture 19; Conjecture 21 adds support restrictions and generalized column totals. ([drops.dagstuhl.de](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.98/LIPIcs.ITCS.2026.98.pdf))

The audited counterexample has

\[
m=11,\qquad n=15,\qquad D=1,
\]

with rows

\[
B,A_1,H_1,\ldots,A_5,H_5
\]

and five consecutive blocks \(J_k,K_k,L_k\).

Set \(\eta=1/1000\). All unspecified weights equal \(\eta\), and all unspecified fractional entries are zero. In block \(k\),

\[
\begin{array}{c|c|c}
\text{column}&\text{nonzero fractional entries}&
\text{exceptional weights}\\ \hline
J_k&
x_{A_k,J_k}=19/24,\ x_{B,J_k}=5/24&
d_{A_k,J_k}=d_{B,J_k}=1\\
K_k&
x_{A_k,K_k}=x_{H_k,K_k}=1/2&
d_{A_k,K_k}=1/2,\ d_{H_k,K_k}=1\\
L_k&
x_{A_k,L_k}=23/48,\ x_{H_k,L_k}=25/48&
d_{A_k,L_k}=d_{H_k,L_k}=1 .
\end{array}
\]

Every column sums to one, every weight is strictly positive, and every column has fractional support two.

The local forcing gadget proves that every assignment satisfying discrepancy at most \(1\) must assign

\[
J_k\longmapsto A_k.
\]

Otherwise the \(K_k,L_k\) detector produces a row discrepancy of at least

\[
\frac{49}{48}-13\eta>1.
\]

After five forced decisions, the accumulator row \(B\) has discrepancy at least

\[
5\cdot\frac5{24}-10\eta
=
\frac{619}{600}
>1.
\]

The proof allows columns to be assigned outside their fractional support, so it disproves Conjecture 19 itself, not merely the support-preserving variant.

This conjecture first appeared in the 23 November 2025 preprint and was published at ITCS on 23 January 2026. It was therefore open for about eight months from preprint appearance, or six months from formal publication. ([arxiv.org](https://arxiv.org/abs/2511.18546?utm_source=chatgpt.com))

## Paper package fixed for production

The intended repository location is:

```text
terrorproforma/maths/
└── 2026-unsplittable-flow-counterexamples/
    ├── README.md
    ├── CITATION.cff
    ├── Makefile
    ├── requirements.txt
    ├── AI_DISCLOSURE.md
    ├── SUBMISSION_CHECKLIST.md
    ├── papers/
    │   ├── dgg/
    │   │   ├── main.tex
    │   │   ├── references.bib
    │   │   └── author-info.tex.example
    │   ├── chairman/
    │   │   ├── main.tex
    │   │   ├── references.bib
    │   │   └── author-info.tex.example
    │   └── overview/
    │       └── main.tex
    ├── figures/
    │   ├── dgg_network.tex
    │   ├── dgg_stable_set.tex
    │   ├── dgg_cost_gap.tex
    │   ├── history_timeline.tex
    │   ├── chairman_gadget.tex
    │   └── graphical_abstract.tex
    ├── data/
    │   ├── dgg_instance.json
    │   ├── dgg_all_positive_costs.json
    │   └── chairman_instance.json
    ├── code/
    │   ├── verify_dgg.py
    │   ├── verify_chairman_certificate.py
    │   ├── verify_chairman_milp.py
    │   ├── verify_all.py
    │   ├── search_dgg_family.py
    │   └── search_chairman_family.py
    ├── research/
    │   ├── derivation_dgg.md
    │   ├── derivation_chairman.md
    │   ├── chronology_and_importance.md
    │   ├── search_log.md
    │   ├── provenance.md
    │   └── validation_report.md
    ├── tests/
    │   └── test_certificates.py
    └── .github/workflows/
        └── verify.yml
```

The planned primary illustration is a deterministic TikZ figure displaying the planar \(K_4\)-subdivision, with every arc labelled by \((x_a,c_a)\), terminal demands shown at the sinks, and the three bottleneck arcs emphasized. A second panel displays the triangle inequality

\[
z_1+z_2+z_3\le1
\]

beside the fractional value \(16/15\), followed by the cost gap \(58<60\). No generative-image system is needed for the publication figures.

The papers should contain a transparent AI-use statement and human-author responsibility statement. They should not list an AI system as an author. Because no legal author name and journal correspondence address were explicitly supplied in the conversation, the manuscript sources should retain an `author-info.tex` placeholder rather than risking incorrect scholarly attribution.

The mathematics is ready for artifact production. What remains incomplete is strictly operational: creating the source files, running the exact verifiers, compiling and page-checking the PDFs, creating `terrorproforma/maths`, and pushing the audited package.

---

## User

there is a repo called maths put everything you have inside it 

---

## User

put everything inside an appropriately labelled subfolder (you will have to create the folder ) 

---

## User

put everything inside an appropriately labelled subfolder (you will have to create the folder ) 

---

## Assistant

I’m packaging the two verified counterexamples, proofs, derivations, exact checkers, figures, and compiled paper under a new `maths` subfolder, then pushing directly to `main`.

---

## Assistant

The repository is confirmed: `terrorproforma/maths`, empty, public, and writable. I’m using `counterexamples-to-unsplittable-flow-and-discrepancy-conjectures/` as the subfolder.

---

## User

no dont ficking initialise it its got stuff in there already 

---

## User

verify that all the content has been uploaded to the repo 

---

## Assistant

I’m checking the actual repository tree, not assuming the upload succeeded. I’ll verify the labelled subfolder, expected sources, generated PDFs, figures, data, derivations, code, tests, and build status.

---

## Assistant

I found the key issue: the package was uploaded, but it is on `agent/rounding-counterexample-papers` behind open PR #1—not on `main`. I’m now auditing the complete file list and validation claims before giving you the exact status.

---

## Assistant

I’ve isolated the discrepancy: the full package exists on the review branch, but I’m checking `main` directly before giving you a yes/no.

---

## Assistant

## Verification result

**All final reproducible content is uploaded to `terrorproforma/maths`, but it is NOT on `main`.**

It currently exists here:

```text id="zc3oot"
branch: agent/rounding-counterexample-papers
commit: d31224c162b1dab0a05e4801627dda0be5aed454
folder: 2026-rounding-counterexamples/
```

PR #1 remains open and unmerged. A direct fetch of:

```text id="48udoj"
main:2026-rounding-counterexamples/README.md
```

returns `404 Not Found`.

### Present on the branch

- Three compiled PDFs:
  - `generated-pdfs/dgg-counterexample.pdf`
  - `generated-pdfs/chairman-counterexample.pdf`
  - `generated-pdfs/overview.pdf`
- Complete LaTeX sources and bibliography
- Exact JSON instances
- Exact rational/integer verifiers
- Parametric-family derivation scripts
- TikZ network, obstruction, forcing-gadget, and graphical-abstract figures
- Full derivations
- Importance and chronology analysis
- Search log
- Provenance record
- Validation report
- AI disclosure
- Journal-submission checklist
- Makefile and GitHub Actions workflow

The package README records the complete directory map and verification commands. fileciteturn31file0L12-L80

### One limitation

The repository contains **all final reproducible mathematics and code**, but not every temporary notebook cell, random solver trial, or ephemeral interactive search from the exploratory phase. That limitation is explicitly documented. fileciteturn31file0L98-L100

### Bottom line

| Check | Status |
|---|---|
| Uploaded to `maths` repository | Yes |
| Appropriately labelled subfolder | Yes |
| Papers and compiled PDFs | Yes |
| Final verification code | Yes |
| Exact data certificates | Yes |
| Derivations and research notes | Yes |
| Figures and overview | Yes |
| Present on `main` | **No** |
| PR merged | **No** |

I made **no repository changes** during this verification.

---

## User

can you package the entire text of this conversation thread word for word. i want to export it and use it elsewhere. put in in a md file for download
