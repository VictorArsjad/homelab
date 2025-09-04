# Homelab Docker Architecture

## Network

```
[Internet]
    │
    ▼
[Nginx Proxy Manager LXC]  ← sole owner of :80/:443, ACME, public DNS
    │  (HTTP reverse proxy only; TLS terminated here)
    ▼
[Traefik on Ubuntu VM]     ← internal router for Docker apps (n8n, future)
    │
    ├─► n8n (Docker)
    └─► other Docker services
```

### Rules of engagement

- **NPM = edge**. Main external gateway on ports 80/443, managing domains & SSL for all your exposed services.
- **Traefik = internal**. Internal router for Docker apps (like n8n). It only needs to talk to NPM or ngrok, not bind directly to 80/443 on the host.
  - Listen on an **internal port** (e.g., `:8081`) only.
- **Forwarding model**. In NPM, each “Proxy Host” points to Traefik’s internal HTTP port (e.g., `traefik.vm.lan:8081`) with the path/host you want.

### Advantages

- Keeps your GUI-friendly edge (NPM) for quick host/cert tweaks across LXCs & VMs.
- Leverages Traefik’s Docker auto-discovery and labels for internal apps—no manual vhost files.
- Avoids ACME/routing duplication, port conflicts, and redirect loops.
