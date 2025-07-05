# Team Estimator CLI

A simple Python CLI to estimate various metrics for software projects.

## What It Does

- Calculates the minimum team needed to deliver a project in a given time.
- Estimates how long a fixed team will take to deliver a workload.

## Pre-Requisites

1. Docker
2. VsCode

## How to use

1. Run `docker-compose up`.
2. Open another terminal and run `docker exec -it team_estimator_cli bash`
3. Run `python -m team-estimator <options>`

## Allowed Options

1. **team_size** — Calculate the minimum viable team composition required to deliver a project within a given timeframe.
2. **delivery_timeline** — Estimate how long a fixed team will take to deliver a defined workload.
