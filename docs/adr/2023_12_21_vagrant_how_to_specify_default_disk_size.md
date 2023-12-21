# Vagrant: How to Specify Default Disk Size

* Status: accepted
* Date: 2023-12-21

## Context and Problem Statement

Some projects end up being quite large. This means the default 40GB reaches it limits. This ADR is
about how to change the default disk size.

## Decision Drivers

* Simple
* Extendable - In future we might want to add more disks

## Considered Options

### Use the config.json with a disks map and make a default key for the primary vagrant disk

How such a map could look a like:

```json
{
    "disks": {
        "default": {
            "size": "100GB"
        }
    }
}
```

* Good, because it is obvious what it does
* Good, because it is simple to implement
* Good, because we can add more disks
* Good, because every disk should be unique and with a map it is not possible to have the same disk
  names
* Bad, because the reserved "default" disk is kind a confusing, when not known
* Bad, because it might feel like magic, when this map is optional and not always used

## Decision Outcome

Chosen
option: "[Use the config.json with a disks map and make a default key for the primary vagrant disk](#use-the-configjson-with-a-disks-map-and-make-a-default-key-for-the-primary-vagrant-disk)".

It is kind a good enough. So let's go down this route

## References

* [Vagrant: Disks Usage](https://developer.hashicorp.com/vagrant/docs/disks/usage)
