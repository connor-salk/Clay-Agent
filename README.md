# Clay Agent

This project now supports two layers:

- a Clay knowledge refresh layer that keeps official Clay guidance current
- the main product: a Cresting Wave Clay advisor that can give practical, step-by-step help inside Clay

The knowledge refresh layer is complete enough for v1. It monitors official Clay documentation, stores snapshots, detects meaningful changes, updates reference notes, and logs each run in a lightweight, readable way.

The main product focus is now the Cresting Wave Clay advisor. That advisor should help build high-quality contact lists, improve targeting against the ideal customer profile, and apply Clay with the judgment of a strong sales engineer rather than a generic research assistant.

## Project Layout

- `references/` for Clay research and working notes
- `prompts/` for reusable prompt templates
- `src/` for simple refresh and update scripts
- `data/snapshots/` for saved source snapshots
- `logs/` for refresh history
- `plan.md` for the current project plan

## Current Focus

The refresh system is now stable enough to serve as the v1 knowledge layer. From here, the primary work shifts to building the Cresting Wave Clay advisor on top of that knowledge base without overengineering the repo.
