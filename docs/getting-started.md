## Setup

In general we aim to be close as possible what the docs of the systems propose.

## Vagrant

### VirtualBox

### libvirt with GPU passthrough

Steps:
1. Setup the host system
2. Confirm permissions
3. Enable the libvirt service
4. 

**1. Setup the host system**

```shell
sudo apt-get purge vagrant-libvirt
sudo apt-mark hold vagrant-libvirt
sudo apt-get update && \
    sudo apt-get install -y qemu libvirt-daemon-system ebtables libguestfs-tools \
        vagrant ruby-fog-libvirt

```
- [Source](https://vagrant-libvirt.github.io/vagrant-libvirt/)

Provide the VFIO/IOMMU for GPU passthrough.
1. edit the `/etc/default/grub`

```shell
sudo update-grub
sudo reboot

```
2. Remove the GPU from host:

```
lspci -nn | grep -i nvidia
# Beispiel: 01:00.0 VGA compatible controller: NVIDIA Corporation 10de:1b80
#            01:00.1 Audio device: NVIDIA Corporation 10de:10f0

# Kernel-Module blacklisten:
echo "blacklist nouveau" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
echo "options vfio-pci ids=10de:1b80,10de:10f0" | sudo tee /etc/modprobe.d/vfio.conf
# -> Hier: GPU + Audio-Device PCI IDs angeben

sudo update-initramfs -u
sudo reboot

```

3. Check that stuff is in the machine

```shell
lspci -nnk | grep -A3 VGA
```
