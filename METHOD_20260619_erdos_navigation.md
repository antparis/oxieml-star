# METHOD 2026-06-19 -- [METHOD, not a result] The Erdos-navigation protocol: a discovery strategy for the eml/eml* project, kept STRICTLY SEPARATE from the judge. Inspired by the OpenAI / Erdos unit-distance result (announced 2026-05-20, verified by Gowers and Sawin; the model disproved Erdos' 1946 unit-distance conjecture by abandoning square-grid constructions and reformulating via algebraic number theory -- infinite class field towers, Golod-Shafarevich -- giving n^(1+delta), delta>=0.014 per Sawin). This is a NAVIGATION rule (where/how to look), NOT a judge function and NOT a result. It carries no MSE and no verdict.
## The three roles (pipeline, no contamination)
 - NAVIGATOR = this method. Decides WHERE to look and how to reframe. Computes nothing; orients only.
 - DISCOVERER = the PySR translator. Takes data, proposes a candidate formula. Limited on irrational exponents.
 - CERTIFIER = the SymPy judge (verify_exact.py / judge_v2.py). Takes the formula, rules holo / anti /
   real-trapped / module-trapped, EXACTLY and NEUTRALLY. It can and must say NO.
 Flow: navigator reframes -> data on the new terrain -> discoverer proposes a formula -> certifier rules.
 The judge stays neutral and separate (Erdos point 4 below protects it explicitly).
## The four Erdos points, translated to eml/eml*
 1. DO NOT ITERATE ON KNOWN CONSTRUCTIONS (they bias toward reproducing the known). For us, the "square
    grid" is SPATIAL FIELDS (fluids, potentials, vortices). Every wall this project hit came from there:
    real fields are mirror-locked; potential-derived fields give only mirror or module-trap; Navier-Stokes
    gives module-trap (vortices) or periodicity artefacts (Taylor-Green, Kovasznay). Stop iterating there.
 2. REFRAME VIA A DEEPER, A PRIORI FOREIGN STRUCTURE. Erdos went geometry -> algebraic number theory.
    For us: stop seeing anti-holomorphy as a property of a FIELD IN SPACE; see it as forced by an
    ALGEBRAIC structure. Candidates where conjugation is FORCED (not an analysis choice): imaginary
    quadratic fields (complex conjugation = the Galois automorphism), Maass forms (real-analytic,
    NON-holomorphic, forced by the hyperbolic Laplacian), modular vs non-holomorphic automorphic forms.
 3. COUNTER-INTUITIVE PARAMETERIZATION: fix what intuition grows, grow what intuition fixes. Intuition
    says "look in rich, turbulent physical systems". Counter-move: fix the physics to the MINIMUM, grow
    the ALGEBRAIC structure (e.g. field degree growing, level/weight growing), keep the object simple.
 4. ARBITER = external rigorous verification, NEVER the model's self-validation. For us this is UNCHANGED:
    the SymPy judge + execution on Anthony's machine. This point explicitly PROTECTS the judge: the method
    never enters the judge; the judge never "searches" for chirality. A search-biased judge would be the
    SPARC self-deception. The judge stays bete et severe (dumb and strict).
## Why this is recorded now (today's lesson)
This session iterated on spatial fields all day and hit the wall every time (potential flow honest-holo;
Navier-Stokes module-trapped or periodicity-artefact; the Beltrami sieve even had a periodicity blind
spot). Erdos point 1 names that exact error. The method is the antidote: change terrain, do not polish
the grid. NOTE: a method that worked for Erdos guarantees NOTHING for us -- a resemblance is not an
identity (the project's own rule against seductive analogies). This protocol offers a DIRECTION, not a
promised result. Any lead it suggests is still INVALID until the judge certifies on Anthony's machine.
## Status
[METHOD] navigation protocol, separate from the judge. NOT a result, no MSE, no verdict. First terrains
to try under it: Maass forms (non-holomorphy forced by the hyperbolic Laplacian) and imaginary quadratic
fields (conjugation forced by Galois). Reconnects: navigation law (independent anti needs a natively
complex object, not a real field); CERTIFIER vs DISCOVERER distinction; SPARC guard (judge stays neutral).
Reference: OpenAI unit-distance result 2026-05-20 (Sawin "An explicit lower bound for the unit distance
problem", delta>=0.014); arbiter discipline unchanged. Arbiter for any eml* lead = SymPy judge + machine.
