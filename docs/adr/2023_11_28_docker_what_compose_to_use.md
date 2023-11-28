# Docker: What compose (plugin vs binary) to use?

* Status: accepted
* Date: 2023-11-28

## Context and Problem Statement

Docker provides two ways to install docker-compose. This ADR tries to decide which compose to use.

## Decision Drivers

* Ease of use
* Stability

## Considered Options

### Use `docker-compose` binary

That's the way old people like me know. We are used to install docker-cli and let it be, 
parallel we install docker-compose, which we most of the time are using to up/down our containers.

Until docker compose v2 this was the way to go.

* Good. It's known for years.
* Bad. It needs a separate binary.
* Bad. It is no longer the recommended way for docker[¹][1].
* Bad. It is no longer the default way for geerlingguy roles[²][2].

### Use docker compose plugin

Since compose v2 this is the recommended way.

Basically docker has a plugin functionality and there is the compose plugin. 

The idea is to integrate docker related CLI's, like the docker-compose, into the docker-cli.

* Good. Fewer binaries to install.
* Good. Uses same commands as docker-compose.
* Good. Because it is the recommended way[¹][1].

### Being strict of the choice: No

We got two options to use. So there is the question: Should we allow using both ways?

* Good. We are more flexible.
* Bad. Those are two separate ways of how to install and handle each way. That might add complexity 
  of allowing both ways. While there is no real reason for allowing both ways.

### Being strict of the choice: Yes

We got two options to use. So there is question: Should we allow using both ways?

* Good. Because the docker role need only to know how to install and handle stuff in one way.
* Bad. It is less flexible.

## Decision Outcome

Chosen option: "[Use docker compose plugin](#use-docker-compose-plugin)", because it is simple and 
the recommended way. So it is probably the long term stable option.

Additional option: "[Being strict of the choice: Yes](#being-strict-of-the-choice-yes)", because it comes with less complexity when 
we only have one way to provide. Maybe at some point we learn that there are good reason's to allow 
the docker-compose way... but for now YAGNI.

## References

* [1][1]: Docker on compose v2 and the new compose command.
* [2][2]: Geerlingguy mentioning switching to docker compose way, soon.

[1]: https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command
[2]: https://github.com/geerlingguy/ansible-role-docker/issues/375#issuecomment-1258701068
