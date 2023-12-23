# Vagrant(NFS): How to Allow `chown` on a Guest?

* Status: draft
* Date: 2023-12-23

## Context and Problem Statement

We need to chown on a guest. 

And it is important, that when we chown, the host does not change the permissions.

The goal of this ADR is to decide how to that.

## Decision Drivers

* Cross-Platform Compatibility (macOS, Windows, Linux)
* Independence from VM Provider Choice
* Ease of getting started
* Low maintenance effort
* Flexible
  * No need manually adding maps to users from host to guest
  * chown on the guest works
  * chown on a container in the guest works

## Considered Options

### Using vagrant-bindfs

As we sometimes need to change user and groups on the machine, we kind a need a way to allow this.

Some projects have used bindfs for this purpose.

After some local tests, I'm pretty sure this does not really work as we need it.

Use case for most people was something like, we have a vagrant box and the current user fails when
running chown.

The solution was to use bindfs to mount a directory with the already correct permission.

This leads to: chown won't do anything and not throw an error.

Maybe we can do some bindfs trickery when using map-ids, so all mount users are mapped to the
vagrant user... I wasn't able to make that work (yet). Even if it works, it is not sure if there is
quite some manual mapping involved or not.

In the devbox case what we need is running chown on the guest, maybe even in a mounted volume on a
guest's container, and not reflect those changes back to the host.

Long story short, this option in theory sounds good. Practically I misunderstood the claim:
> This allow you to change owner, group and permissions on files and, for example, work around NFS
> share permissions issues.

* Good, because
* Bad, because

### TBD

TBD

* Good, because
* Bad, because

## Decision Outcome

Chosen option: "[TBD](#nfs)".

TBD

## References

* [ADR which defined what file system to use](2023_12_22_vagrant_which_file_system_to_use.md)
