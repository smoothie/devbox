# Vagrant: Which File System to Use?

* Status: accepted
* Date: 2023-12-22

## Context and Problem Statement

Vagrant lets us share folders to guest machines. A couple of file systems are allowed. Each
comes with benefits and drawbacks.

The goal of this ADR is to decide which file system to use.

Focusing on NFS, rsync, zfs, Vagrant Synced Folders

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

The Vagrant NFS way is a two-way sync.

* Good, because it is usually fast enough.
* Good, because NFS supports user and groups.
* Good, because it is a two-way sync.
* Good, because it does not lock us into a specific provider.
* Good, because it does not lock us into a specific platform.
* Bad, because it needs quite some setup (nfs-server).
* Bad, because when unknown working with a nfs-server, this might come with some learning-curve.
* Bad, because when using the default way and changing user and/or groups on the guest might lead to
  invalid permissions on the host.
* Bad, because making use of user and group changes, we need an additional vagrant
  plugin ([6][6]).

### rsync

The Vagrant way for [rsync][2] is a one-way sync.

* Good, because it could be fast ([3][3]).
* Good, because it does not lock us into a specific provider.
* Good, because it does not lock us into a specific platform.
* Bad, because Vagrant official way is one-way sync ([2][2]). A two-way sync is comfort to not miss
  on dev machines.
* Bad, because Vagrant plugins related to two-way syncs seem to be unmaintained or not used.
* Bad, because when using rsync and having stuff automatically synced to the guest, we need to keep
  an additional command running.
* Bad, because when mapping the scenarios why people love rsync ([4][4], [5][5]) to what we're
  trying to do, it does not fit.

### zfs

ZFS is not a Vagrant shared folder type.

The idea is to use ZFS on the host, to increase performance.

Since this, not a shared folder, I just keep this idea flying around without digging deeper if good
or bad.

### Vagrant Synced Folders

Vagrant comes with vendor specific default shared folders, such as VirtualBox.

That's another two-way sync.

* Good, because easy to set up.
* Good, because it is a two-way sync.
* Good, because it does not lock us into a specific platform.
* Bad, because it locks us into a specific provider.
* Bad, because relatively limited options to configure the shared folder behavior.
* Bad, because performance ([3][3]).

## Decision Outcome

Chosen option: "[NFS](#nfs)".

In a later [ADR](TBD_2023_12_23_vagrant_nfs_how_to_allow_chowning.md) I will dig deeper into how to allow chown inside the guest without changing host permissions.

## References

* [1][1]: Vagrant on how to set up NFS
* [2][2]: Vagrant on how to set up rsync
* [3][3]: Jeff Geerling on Vagrant VMs performance in NFS, rsync and shared folder (2014)
* [4][4]: Steve Newsted a quick intro into what rsync does
* [5][5]: Michael Stapelberg with some experiences where rsync was a game changer for him
* [6][6]: A Vagrant community plugin: vagrant-bindfs

[1]: https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs

[2]: https://developer.hashicorp.com/vagrant/docs/synced-folders/rsync

[3]: https://www.jeffgeerling.com/blogs/jeff-geerling/nfs-rsync-and-shared-folder

[4]: https://www.redhat.com/sysadmin/sync-rsync

[5]: https://michael.stapelberg.ch/posts/2022-06-18-rsync-article-1-scenarios/

[6]: https://github.com/gael-ian/vagrant-bindfs
