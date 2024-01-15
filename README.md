# preconditioners_ipm

Interior point methods (IPM) are a standard approach to solve linear optimization problems and are especially useful when considering large-scale optimization problems. IPMs start with a feasible point from which a search direction is obtained by solving a linear equation system arising from the KKT optimality conditions.

Description:

Work description

Interior point methods (IPM) are a standard approach to solve linear optimization problems and are especially useful when considering large-scale optimization problems. IPMs start with a feasible point from which a search direction is obtained by solving a linear equation system arising from the KKT optimality conditions. In practice, solving this linear equation system is the computational bottleneck of the algorithm. While iterative methods are commonly used to solve large-scale equation systems, they often require a good preconditioner to achieve fast convergence. It has proven difficult to design good preconditioners for a general class of linear equation systems arising in linear programming.

Recent advances in data-driven optimization aim to replace hand-engineered preconditioners with parameterized functions that can be trained against data. The aim of this project is to extend this setting of learned preconditioners to interior-point methods. Here, several key challenges can be considered depending on the students' interest and background:

Choosing a suitable loss function. While for generic problems a standard distance metric (Frobenius norm) can be used, but this is numerically challenging for interior point methods. In IPMs, a series of slowly changing linear equation systems has to be. By changing how the preconditioner is computed, it might be possible to use this to improve overall performance

References

Jorge Nocedal and Stephen Wright, Numerical Optimization, 1999. 
Florian Potra and Stephen Wright, Interior point methods, 2000. 
Paul Häusner, Ozan Öktem and Jens Sjölund. Neural incomplete factorization: learning preconditioners for the conjugate gradient method (https://arxiv.org/abs/2305.16368Links to an external site.), 2023.
