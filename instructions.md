# Running E3SM with source-aware numerical water tracers

## Getting the code. 

```bash
git clone -b ie3sm1.0 --recursive https://github.com/AlexAudette/E3SM.git E3SM_wtrc
```
If on Perlmutter, no need to change anything. If you are on another machine, I recommend you install the `maint-2.1` branch of E3SM first, and make sure this is running on your machine. To do this, follow these instructions from the [E3SM quickstart page](https://e3sm.org/model/running-e3sm/e3sm-quick-start/), which are copied in the [General E3SM information](#general-e3sm-information) section. Otherwise, continue here. 

```bash
cd E3SM_wtrc
```


## General E3SM information

### Get the Code

The E3SM code is available from Github. We only support obtaining the code with “git clone“.  You need at least version 2.0 or later of git. For access to all code versions, add an ssh key to github.  We will not be making .tar.gz or .zip files available at this time.

Open a terminal and issue the following commands:

```bash 
git clone -b <ref> --recursive https://github.com/E3SM-Project/E3SM.git
```

where <ref> is one of the following:

- maint-1.0
- maint-1.1
- maint-1.2
- maint-2.0
- maint-2.1

```bash 
cd E3SM
```

NOTE: Do not check out master unless you want to be on your own. We do not support general users on the master branch.

NOTE:  do not use .tar.gz or .zip files Github makes available because they do not include the code from git submodules.
### Input Data

E3SM model requires several input data files for initial and boundary conditions. On supported platforms, all the input data for supported cases is already available in world-readable local directories. For un-supported machines, you should NOT try to download all the inputdata at once.  The CIME case control system will download each missing file for each case you try to run.
Input data is kept on the following servers
E3SM-authored input data lives on the a world-readable http server at https://web.lcrc.anl.gov/public/e3sm/. 
Some cases may require CESM data, which can be obtained from the [CESM input data server](https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/), which is now world-readable without any authentication required.


The CIME case control system will automatically check each server for any missing input data files and download from the first one it finds.
Running E3SM

See [Step-by-Step](https://docs.e3sm.org/running-e3sm-guide/) guide to running E3SM for a very detailed explanation covering:

- Pre-Production
- Production
- Post-Processing
- Documentation
- Long-Term Archiving
- Publishing
- Appendix

This guide is tailored to the E3SM project or the so-called “ecosystem” projects (projects funded by DOE BER to work on some aspect of E3SM) and follows the E3SM processes, best practices, and procedures.

 
### Troubleshooting

Use github to post a question or report a bug (it requires a github account):

1) Report a bug in E3SM code https://github.com/E3SM-Project/E3SM/issues
2) Other questions about E3SM https://github.com/E3SM-Project/E3SM/discussions

---

The general E3SM [section](#running-e3sm-with-source-aware-numerical-water-tracers)