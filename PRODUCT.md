# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS/JS in a single `index.html` (user choice). No build step; opens by double-click. Delivered as a local file only (no publishing).

## Users

University students presenting a discrete-event simulation (DES) project live in class, projected on a screen, explaining each deliverable to a teacher and classmates. Secondary: the teacher following along against the grading rubric.

## Product Purpose

Interactive web app that solves "Escenario 2 – Gasolinera": a single-server FIFO queue simulated for 100 vehicles × 5 (or 10) replications. It must make every rubric deliverable visible, easy to understand and verifiable: data analysis + χ² + inverse transform (8 pts), live DES simulator + manual trace (10 pts), replications + inference (6 pts), technical / critical / scenario questions (6 pts).

## Positioning

Every number shown is computed live from the official data and a reproducible seeded PRNG (Mulberry32), so the presenter can change seeds, double replications or add a second pump in front of the audience and the answers update with the evidence.

## Operating Context

Projected in a classroom (large screen, distance reading), driven by the presenter with mouse/keyboard. Spanish language. Units: minutes.

## Capabilities and Constraints

- Official data: Tll {1:10, 2:15, 3:15, 4:7, 5:3}; Ts {2:5, 3:10, 4:20, 5:10, 6:5}; N = 50.
- 1 server, FIFO, 100 customers/replica, start empty at t = 0, 95% confidence, 10% max relative error, main indicator mean wait in queue Wq.
- ρ = λ/μ = 4.00/2.56 = 1.5625 > 1 — the system is unstable; the queue grows by design.
- Views map 1:1 to the rubric modules.

## Evidence on Hand

Only the official frequency tables above. No real fuel-station footage, brand or customer data; nothing may be fabricated beyond simulated output.

## Product Principles

1. Every claim is backed by a number computed on screen.
2. Teach step by step: formula, then substitution, then result.
3. Reproducible: same seed, same result, always.
4. Readable from the back of the classroom.
