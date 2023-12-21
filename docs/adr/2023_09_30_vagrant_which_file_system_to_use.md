# Vagrant: Which File System to Use?

* Status: draft
* Date: 2023-09-30

## Context and Problem Statement

Vagrant lets us share folders to guest machines. A couple of file systems are allowed. Each
comes with benefits and drawbacks.

The goal of this ADR is to decide which file system to use.

Focusing on NFS, rsync, zfs, Vagrant Shared Folders and Vagrant Synced Folders

## Decision Drivers

* Cross-Platform Compatibility (macOS, Windows, Linux)
* Independence from VM Provider Choice
* Ease of getting started
* Ease of use
    * Change of a file on the host should reflect the changes on the guest
    * Change of a file on the guest should reflect the changes on the host
    * Adding files on the guest/host should not lead to weird user permission errors on the
      host/guest
    * Stuff like npm run watch should be able to be notified about changes
* Performance
    * Evaluate how efficiently the solution handles tasks like npm or composer installs to avoid
      unnecessary delays

## Considered Options

### NFS

**TBD**

* Good, because 
* Bad, because 

### rsync

**TBD**

* Good, because 
* Bad, because 

### zfs

**TBD**

* Good, because 
* Bad, because 

### Vagrants Synced Folders

**TBD**

* Good, because 
* Bad, because 

## Decision Outcome

Chosen option: "[TBD](#nfs)".

TBD

## References

* none
