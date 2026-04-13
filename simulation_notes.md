# Moisture locking simulations

## Experiment Plan

### Tier 1 — Total moisture locking (3 phases)

| Name | Experiment # | CO2 | ROW | ARC |
|---|---|---|---|---|
| PI Baseline | 1.1 | PI | Free | Free |
| 1% Baseline response | 1.2 | 1% ramping up | Free | Free |
| Locked both 1% | 1.3 | 1% ramping up | Locked (PI) | Locked (PI) |
| ARC Locked - 1% | 1.4 | 1% ramping up | Free | Locked (PI) |
| ROW Locked - 1% | 1.5 | 1% ramping up | Locked (PI) | Free |

**Warmer base state**
- 1.2 - 1.1: Total response to rampant CO2
- 1.3 - 1.1: Response to CO2 increase without moistening\*
- 1.5 - 1.1: Response to CO2 increase without ROW moistening\*
- 1.4 - 1.1: Response to CO2 increase without ARC moistening\*
- 1.2 - 1.3: Role of moistening
- 1.2 - 1.4: Role of Arctic moistening
- 1.2 - 1.5: Role of ROW moistening

**Cooler base state**
- 1.2 - 1.3: Role of global moistening
- 1.5 - 1.3: Role of ARC moistening
- 1.4 - 1.3: Role of ROW moistening

\*Include spurious effect of locking a region.

---

### Tier 2 — Cloud locking (only condensates)

| Name | Experiment # | CO2 | Sp. Hum. | Clouds |
|---|---|---|---|---|
| Cloud locked ARC | 2.1 | 1% ramping up | Free | ARC locked (PI) |
| Cloud locked ROW | 2.2 | 1% ramping up | Free | ROW locked (PI) |
| Cloud locked global | 2.3 | 1% ramping up | Free | ARC & ROW locked (PI) |

**Warmer base state**
- 2.1 - 1.1: Effect of warming without Arctic cloud increase*
- 2.2 - 1.1: Effect of warming without ROW cloud increase*
- 2.3 - 1.1: Effect of warming without global cloud increase*
- 1.2 - 2.1: Role of Arctic cloud increase*
- 1.2 - 2.2: Role of ROW cloud increase*
- 1.2 - 2.3: Role of cloud increase*
- 2.2 - 2.3: Role of Arctic cloud increase*
- 2.1 - 2.3: Role of ROW cloud increase*

\*Includes spurious effect of locking a region.

---
## Run setup

The case directories for the simulations are in the following directory on Perlmutter `/global/homes/a/aaudette/cases_E3SM/cloud_locking_runs/production`. 


```bash
CASEDIR="/global/homes/a/aaudette/cases_E3SM/cloud_locking_runs/production/1850_free"

/global/u2/a/aaudette/E3SM/cime/scripts/create_newcase --case "${CASEDIR}" --compset 1850SOI_EAM%CMIP6_ELM%SPBC_MPASSI_MPASO_MOSART_SGLC_SWAV --res ne30pg2_EC30to60E2r2 --mach pm-cpu --project m4426

```

Once the case has been created, the water tracer part can be be configured using the run_setup module in this directory. See the `README.md` inside the `run_setup/` directory. 



