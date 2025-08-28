# homelab

This repository serves as a central storage for all things related to my personal homelab. It is intended to organize, configure, and document various self-hosted services and tools that power my home infrastructure.

## Current Contents

- **n8n.yaml**: Configuration for the n8n automation service.

## Accessing the Kubernetes Cluster (via Tailscale)

Use the steps below to access the k3s cluster from your laptop using the kubeconfig generated on the homelab VM.

### Prerequisites

The homelab VM is online with k3s running.

Tailscale is connected on both the VM and your laptop.

A kubeconfig exists on the VM at ~/k3s-tailscale.yaml (server address points to the VM’s Tailscale IP).

### Commands

```shell
# Create local kube config directory if it doesn't exist
mkdir -p ~/.kube

# Copy kubeconfig from the homelab VM to your laptop
scp <VM_USERr>@<TAILSCALE_IP>:~/k3s-tailscale.yaml ~/.kube/k3s.yaml

# Test connectivity to the cluster using the copied kubeconfig
kubectl --kubeconfig ~/.kube/k3s.yaml get nodes
```

> Tip: If you already use a different kubeconfig, keep this file separate (as above) and reference it explicitly with --kubeconfig to avoid changing your default context.

## Future Plans

- [ ] Add configurations and documentation for additional services (e.g., monitoring, media servers, backup solutions, etc.).

- [ ] Maintain scripts and deployment files for easy setup and management (including secret creation scripts and GitOps workflows).

Feel free to explore or use these resources for your own homelab setup!