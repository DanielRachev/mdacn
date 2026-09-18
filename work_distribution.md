# Assignment 1: Work Distribution

## 1\. Collaboration & Review Protocol

- **Branching Strategy:** Every team member works on an isolated Git branch (for example, `feature/DANIEL-part-a`). All code, and figures for that member’s assigned questions must be committed directly to their branch.  
- **Peer Review (One-Down Rule):** When a branch is ready, open a Pull Request / Merge Request. Both the implementation and the draft report text must be reviewed and approved by the assigned reviewer before merging into `main`:  
  - **DANIEL** is reviewed by **POLLY**  
  - **POLLY** is reviewed by **ANTREAS**  
  - **ANTREAS** is reviewed by **JACEK**  
  - **JACEK** is reviewed by **GEORGI**  
  - **GEORGI** is reviewed by **JAKUB**  
  - **JAKUB** is reviewed by **DANIEL**  
- **Global Review (27.09.2026):** All individual branches must be finalized and merged into `main` by end of day 26.09.2026. On 27.09.2026, the entire team will conduct a comprehensive review of the unified 4-page report and verify the complete codebase before final submission on 28.09.2026.

## 2\. Schedule & Milestones

| Milestone | Target Date | Description |
| :---- | :---- | :---- |
| **M1: Core Engines & Utilities** | 21.09.2026 | DANIEL finishes tie-breaking module and network aggregator; ANTREAS finishes temporal SI simulation engine and exports G\_data trajectories. |
| **M2: G\_2 Simulation Outputs** | 23.09.2026 | GEORGI executes simulation on G\_2 and exports trajectory data for JAKUB. |
| **M3: Individual Completion** | 26.09.2026 | All individual questions implemented, report sections drafted, and one-down peer reviews approved. |
| **M4: Full Team Review** | 27.09.2026 | Joint review of unified 4-page report layout, narrative consistency, and code execution. |
| **M5: Submission** | 28.09.2026 | Final report PDF submitted. |

## 3\. Work Allocation by Team Member

### DANIEL

**Assigned Scope:** Question 1, Question 2, Question 3, Question 4, Question 5 \+ Shared Tie-Breaking Module \+ Aggregation Utility  
**Reviewer:** POLLY  
**Internal Deadlines:**

- *Shared Tie-Breaking Module & Aggregation Utility:* **21.09.2026** (Dependency for downstream tasks)  
    
- *Questions 1 to 5 (Code & Report):* **26.09.2026**  
    
- **Code Deliverables:**  
    
  - Build a reusable network aggregation function that aggregates temporal links over any arbitrary time interval \[t\_start, t\_end\].  
  - Use the aggregation function to construct the unweighted, aggregated static graph G over all time steps \[1, T \= 3259\].  
  - Calculate the number of nodes N, link density p, and standard deviation of degree sqrt(Var\[D\]) (Q1).  
  - Generate the degree distribution plot (Q2).  
  - Calculate degree assortativity rho\_D (Q3).  
  - Calculate the average clustering coefficient C (Q4).  
  - Calculate the average shortest path hopcount E\[H\] and graph diameter H\_max (Q5).  
  - Implement the standalone 1000-iteration randomized tie-breaking module for computing top-f recognition rates r(f) as specified in the assignment. Include automated unit validation for tied rank handling.


- **Report Deliverables:**  
    
  - Construct and populate the topological summary table containing all computed metrics: N, p, sqrt(Var\[D\]), C, E\[H\], H\_max, and rho\_D (Q1, Q3, Q4, Q5).  
  - Integrate the degree distribution plot and write the comparative analysis explaining whether Erdős–Rényi random graphs or scale-free networks better model the network (Q2).  
  - Write the physical interpretation of the degree correlation rho\_D in the context of face-to-face conference contacts (Q3).

### POLLY

**Assigned Scope:** Question 6, Question 7  
**Reviewer:** ANTREAS  
**Internal Deadline:** **26.09.2026**

- **Code Deliverables:**  
  - Compute the quantitative small-world metrics based on the formulas and criteria presented in Lecture 2 (e.g., comparing empirical clustering and path lengths against equivalent random graph baselines) (Q6).  
  - Compute the link weights W (total number of contacts per connected pair over \[1, T\]) for all edges in G (Q7).  
  - Compute the probability density function f\_W(x) with appropriate bin widths and scales (such as logarithmic binning) suitable for interpreting link weights (Q7).  
  - Generate the link weight distribution plot (Q7).  
- **Report Deliverables:**  
  - Write the quantitative justification evaluating whether the network possesses the small-world property, referencing Lecture 2 formulation (Q6).  
  - Integrate the link weight distribution plot and write the explanation determining whether W follows a power-law distribution, providing supporting evidence (Q7).

### ANTREAS

**Assigned Scope:** Simulation Core Engine, Question 8  
**Reviewer:** JACEK  
**Internal Deadlines:**

- *Simulation Engine & G\_data Trajectory Export:* **21.09.2026** (Dependency for JACEK and GEORGI)  
    
- *Report Section & Figure Polish:* **26.09.2026**  
    
- **Code Deliverables:**  
    
  - Build the discrete temporal SI spreading simulation engine on temporal contact networks, strictly following the model rules:  
    - Initially at t \= 0, exactly one node s is infected.  
    - When an infected node i contacts a susceptible node j at time step t, node j becomes infected during step t.  
    - Newly infected node j can only infect other nodes starting at step t \+ 1\.  
    - Once infected, nodes remain infected permanently.  
  - Run the simulation on G\_data across N iterations, using each node i in \[1, N\] as the sole seed node at t \= 0, spanning time steps \[1, T \= 3259\].  
  - Record the total count of infected nodes I(t) at every time step for each seed.  
  - Export simulation outputs (specifically total infected counts at t \= 600 and t \= 1200 for every seed node) to structured data files for downstream use.  
  - Compute and plot the average spreading curve E\[I(t)\] with error bars representing the standard deviation sqrt(Var\[I(t)\]) as a function of time step t on G\_data (Q8).


- **Report Deliverables:**  
    
  - Integrate the spreading curve figure for G\_data (Q8).  
  - Write the narrative explaining the temporal spreading dynamics observed on G\_data across the measurement window (Q8).

### JACEK

**Assigned Scope:** Question 9 (a, b, c, d), Question 10  
**Reviewer:** GEORGI  
**Internal Deadline:** **26.09.2026**

- **Code Deliverables:**  
  - Extract the long-term influence of all nodes at t^(l) \= 1200 from ANTREAS's simulation outputs, generate the descending influence plot, and construct ranking vector R (Q9).  
  - Compute the degrees d\_i^(1200) on the aggregated network over \[1, 1200\] using DANIEL's aggregation utility, and construct ordered vector D (Q9a).  
  - Compute the degrees d\_i^(600) on the aggregated network over \[1, 600\] using DANIEL's aggregation utility, and construct ordered vector D' (Q9b).  
  - Determine the time Z\_i when each node i makes its first contact in G\_data, and construct ordered vector Z (Q9c).  
  - Extract short-term influence at t^(s) \= 600 from ANTREAS's simulation outputs, and construct ranking vector R' (Q10).  
  - Compute recognition rates r\_RD(f), r\_RD'(f), r\_RZ(f), and r\_RR'(f) across f \= 0.05, 0.10, ..., 0.50 using DANIEL's tie-breaking module (Q9a-c, Q10).  
  - Plot all four recognition rate curves on a single consolidated comparison figure (Q9a-c, Q10).  
- **Report Deliverables:**  
  - Integrate the descending influence plot and the unified four-curve recognition rate comparison plot.  
  - Write the analysis identifying which metric among d\_i^(600), d\_i^(1200), or Z\_i best predicts influence ranking, which performs worst, and explain the physical mechanisms behind this behavior (Q9d).  
  - Write the evaluation of whether short-term dynamic influence R' outperforms static centralities at predicting long-term influence, explaining the physical reasons why (Q10).

### GEORGI

**Assigned Scope:** Question 11a  
**Reviewer:** JAKUB  
**Internal Deadlines:**

- *G\_2 Simulation Run & Trajectory Export:* **23.09.2026** (Dependency for JAKUB)  
    
- *Comparative Spreading Analysis & Report Section:* **26.09.2026**  
    
- **Code Deliverables:**  
    
  - Load the randomized temporal network file G\_2.  
  - Execute the temporal SI spreading simulation on G\_2 for all N seed nodes over \[1, T \= 3259\] using ANTREAS's simulation engine.  
  - Export G\_2 simulation results (specifically infection counts at t \= 600 and t \= 1200 for every seed) for JAKUB.  
  - Calculate E\[I(t)\] and sqrt(Var\[I(t)\]) for G\_2.  
  - Generate a comparative spreading plot showing E\[I(t)\] with error bars for both G\_2 and G\_data on the same figure (Q11a).


- **Report Deliverables:**  
    
  - Integrate the comparative spreading dynamics figure (G\_data vs. G\_2) (Q11a).  
  - Write the detailed comparative analysis identifying the key differences in spreading behavior between G\_data and G\_2, explaining the temporal causes (such as burstiness, contact concurrency, and the destruction of temporal correlation) (Q11a).

### JAKUB

**Assigned Scope:** Question 11b  
**Reviewer:** DANIEL  
**Internal Deadline:** **26.09.2026**

- **Code Deliverables:**  
  - Extract the long-term influence ranking R and short-term influence ranking R' specifically derived from G\_2 using GEORGI's simulation outputs.  
  - Compute degrees d\_i^(1200) and d\_i^(600) on G\_2 using DANIEL's aggregation utility, constructing ranking vectors D and D' for G\_2.  
  - Compute first contact times Z\_i on G\_2, constructing ranking vector Z for G\_2.  
  - Compute the four recognition rates r\_RD(f), r\_RD'(f), r\_RZ(f), and r\_RR'(f) on G\_2 using DANIEL's tie-breaking module.  
  - Generate a comparison plot showing the recognition curves obtained from G\_2 alongside the curves obtained from G\_data (Q11b).  
- **Report Deliverables:**  
  - Integrate the comparative recognition curves figure for G\_2 (Q11b).  
  - Write the comprehensive comparative analysis explaining the key differences in predictor performance between G\_2 and G\_data, detailing why timestamp randomization alters the predictive power of each individual metric (Q11b).

## 4\. Key Implementation Standards

1. **Random Seed Standardization:** Because the 1000-iteration randomized tie-breaking procedure involves stochastic sampling, all members computing recognition rates (DANIEL, JACEK, JAKUB) must use a standardized random seed (such as `seed = 42`) to guarantee identical numerical reproducibility.  
2. **Space & Plot Management:** With an absolute maximum limit of 4 pages for 11 distinct questions, figures must be compact and multi-panel (e.g., side-by-side subplots). Each person's combined text and figures should occupy roughly 0.6 to 0.7 pages.  
3. **Handling Disconnected Nodes / Unobserved Contacts:** In the event that a node has zero contacts within an observation window \[1, t\] or its first contact time Z\_i is unobserved, ensure tie ranks are handled deterministically through DANIEL's tie-breaker implementation.