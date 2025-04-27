# Vagrant: How to run local LLMs

* Status: accepted
* Date: 2025-04-27

## Context and Problem Statement

I want to run LLMs. LLMs run (atm) best with NVIDIA GPU's. There is concept called 
"gpu_passthrough". With this concept we usually disconnect the GPU from the host and connect 
it to the virtual machine.

The goal of this ADR is to find out what options we got to run LLms.

At the time writing I am planning to use a small model like qwen2.5-1.5b.

## Decision Drivers

* Low-Maintenance
* Privacy-friendly (EU or self-hosted)
* Cost
* Speed of the response

## Considered Options

### Vagrant: VirtualBox without GPU passthrough

The bare Vagrant VirtualBox way.

* Good, because no need to touch the repo.
* Good, because it is cheap.
* Good, because it is self-hosted.
* Bad, bad, bad, because it is ultra-slow.

### Vagrant: libvirt with GPU passthrough

Vagrant in combination with libvirt and GPU passthrough. 

* Good, because it is self-hosted.
* Okay, because it is cheap, just okay because the hardware is the bottleneck here.
  * Background: A GPU is always attached to one device. So when the host is connected it the 
    * guest can not. This raised the hardware requirements to - at least having iGPU and be 
    * comfortable just be using that one.   
* Okay, because the GPU approach will lead to okayish response time.
* Bad, because it is complex to set up.

### Host: podman/docker approach

Using podman on the host directly 

* Good, because no need to touch the repo.
* Good, because it is self-hosted. 
* Good, because the setup is easy.
* Okay, because the GPU approach will lead to okayish response time.
* Bad, because the host gets more development related dependencies.

### External machine

Use a dedicated machine (in-house or via internets).

* Good, because no need to touch the repo.
* Good, because it is self-hosted. 
* Okay, because the GPU approach will lead to okayish response time or be cost intensive.
* Bad, because the host gets more development related dependencies.
* Bad, because the setup and maintenance is heavy.
* Bad, because it requires an infrastructure.

### Cloud

Use a cloud provider.

* Good, because no need to touch the repo.
* Good, because easy to set up.
* Good, because it is a two-way sync.
* Good, because it does not lock us into a specific platform.
* Bad, because it costs.
  * Note: Some providers seem to have good prices and are located in the EU: studio.nebius.com
* Bad, because it requires to have internet.

## Decision Outcome

I got my head around it and realized that having a LLM related support is not really something 
in scope here (yet). 

So instead the options which require no code changes are kind a good enough.

1. [Host: podman/docker approach](#host-podmandocker-approach)
2. [External machine](#external-machine)
3. [Cloud](#cloud)
