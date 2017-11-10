gumoniter
===

GPU user moniter, a collection of python scripts to collect gpu usages

Environment Setup
---
- This script runs on admin node, slave nodes should have `gpustat` installed.
```bash
pip install gpustat
```
- slave nodes must be able to ssh without password, it can be achieved by `ssh-key-copy`

Configure
---
This script can be configured in file 'config'.
  - `interval`: collects data for every *interval* minutes
  - `hosts`: a list of hostname or ip_address (`ssh`able)
  - `log_path`: log files path. One file for one day.

Architecture
---

- moniter.py: a data collector that queries GPUs and processes information from nodes.
- report.py: a post-process script that compute and report the desired metrics from collected data.
