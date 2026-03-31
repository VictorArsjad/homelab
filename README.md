# Homelab

This repo hosts my homelab infrastructure, currently centered on Docker with Portainer-managed stacks. The older k3s manifests remain for reference but are no longer maintained.

## What’s Active Now

- Docker + Portainer for deployment and lifecycle management
- Stacks live under [docker/stacks](docker/stacks)
- Each stack is self-contained with its own compose file and, where applicable, a local `.env`

## Quick Start (Portainer)

- Open Portainer → Stacks → Add stack
- Choose one stack folder under [docker/stacks](docker/stacks) and use its compose file
  - Example files:
    - [docker/stacks/dockpeek/dockpeek-docker-compose.yaml](docker/stacks/dockpeek/dockpeek-docker-compose.yaml)
    - [docker/stacks/downloader/compose.yml](docker/stacks/downloader/compose.yml)
    - [docker/stacks/dozzle/compose.yml](docker/stacks/dozzle/compose.yml)
    - [docker/stacks/erate/compose.yaml](docker/stacks/erate/compose.yaml)
    - [docker/stacks/komodo/compose.yml](docker/stacks/komodo/compose.yml)
    - [docker/stacks/n8n/n8n-docker-compose.yaml](docker/stacks/n8n/n8n-docker-compose.yaml)
    - [docker/stacks/netdata/netdata-docker-compose.yaml](docker/stacks/netdata/netdata-docker-compose.yaml)
    - [docker/stacks/omnitools/omnitools-docker-compose.yaml](docker/stacks/omnitools/omnitools-docker-compose.yaml)
    - [docker/stacks/syncthing/compose.yaml](docker/stacks/syncthing/compose.yaml)
    - [docker/stacks/vaultwarden/vaultwarden-docker-compose.yaml](docker/stacks/vaultwarden/vaultwarden-docker-compose.yaml)
- If the stack references an `.env` file, create it in the same folder in Portainer’s editor or upload it via the “Environment variables”/“Env file” options. Do not commit secrets to the repo.

## Stacks Overview

- Dockpeek: lightweight Docker dashboard
  - Compose: [docker/stacks/dockpeek/dockpeek-docker-compose.yaml](docker/stacks/dockpeek/dockpeek-docker-compose.yaml)
  - Ports: 3420 → 8000, socket proxy on 2375 (local-only)
  - Env: [docker/stacks/dockpeek/dockpeek.env](docker/stacks/dockpeek/dockpeek.env) (set your own values)

- Downloader (JDownloader)
  - Compose: [docker/stacks/downloader/compose.yml](docker/stacks/downloader/compose.yml)
  - Persistent paths: `/srv/docker/downloader/{downloads,config}`

- Dozzle: container logs UI
  - Compose: [docker/stacks/dozzle/compose.yml](docker/stacks/dozzle/compose.yml)
  - Ports: 8080 → 8080

- Erate: BCA e-rate scraper and dashboard
  - An n8n workflow scrapes BCA money exchange (e-rate) data and stores it in a dedicated Postgres instance. A Grafana PDC (Private Datasource Connect) agent tunnels the database to Grafana Cloud so the data can be visualised remotely.
  - Dashboard: [BCA E-Rate (Grafana)](https://victorarsjad.grafana.net/d/vi8lfjp/bca-e-rate?orgId=1&from=now-7d&to=now&timezone=browser)
  - Compose: [docker/stacks/erate/compose.yaml](docker/stacks/erate/compose.yaml)
  - Env: [docker/stacks/erate/erate.env](docker/stacks/erate/erate.env) (DB credentials and Grafana PDC token)
  - Network: joins external `n8n_net` (shared with the n8n stack)
  - Volumes: `erate_pg_data`

- Komodo: homelab orchestration UI (Core + Periphery + FerretDB + Postgres)
  - Compose: [docker/stacks/komodo/compose.yml](docker/stacks/komodo/compose.yml)
  - Env: [docker/stacks/komodo/.env](docker/stacks/komodo/.env)
  - Ports: 9120 → 9120 (Core)

- n8n: automation platform with Postgres
  - Compose: [docker/stacks/n8n/n8n-docker-compose.yaml](docker/stacks/n8n/n8n-docker-compose.yaml)
  - Env: [docker/stacks/n8n/n8n.env](docker/stacks/n8n/n8n.env)
  - Ports: 5678 → 5678
  - Volumes: `n8n_data`, `n8n_pg_data`

- Netdata: monitoring, host network
  - Compose: [docker/stacks/netdata/netdata-docker-compose.yaml](docker/stacks/netdata/netdata-docker-compose.yaml)
  - Network mode: host; volumes bind host system paths

- Omni Tools
  - Compose: [docker/stacks/omnitools/omnitools-docker-compose.yaml](docker/stacks/omnitools/omnitools-docker-compose.yaml)
  - Ports: 8080 → 80

- Syncthing (+ Tailscale sidecar) and GitWatch
  - Compose: [docker/stacks/syncthing/compose.yaml](docker/stacks/syncthing/compose.yaml)
  - Access: via Tailnet (GUI bound to 127.0.0.1 inside container)
  - Volumes: `syncthing_config` and `/srv/docker/syncthing/obsidian`

- Vaultwarden (+ Tailscale sidecar)
  - Compose: [docker/stacks/vaultwarden/vaultwarden-docker-compose.yaml](docker/stacks/vaultwarden/vaultwarden-docker-compose.yaml)
  - Access: via Tailnet; TLS served by Tailscale serve config in [docker/stacks/vaultwarden/vault.json](docker/stacks/vaultwarden/vault.json)
  - Backup sidecar: `vaultwarden-backup` scheduled daily

## Environment & Secrets

- Each stack that needs secrets ships with an example `.env` in its folder. Provide your own secure values when deploying in Portainer.
- Keep secrets out of version control. Prefer Portainer’s env/secret management or host-level `.env` files that are not committed.
- Security notes
  - Avoid exposing `2375` (Docker socket proxy) to untrusted networks; bind to localhost or internal networks only.
  - Use strong, unique secrets for admin tokens, JWT keys, and DB credentials.
  - Tailscale-based stacks are intended for Tailnet-only access by design.

## Deprecated: k3s

- The k3s manifests under [k3s/](k3s) are no longer maintained and will be removed in the future. You can ignore them for day-to-day operations.

## Maintenance

- Updates: Use Portainer to pull latest images and redeploy per stack.
- Backups: Ensure persistent volumes/paths are included in your backup job
  - n8n: `n8n_data`, `n8n_pg_data`
  - Vaultwarden: `docker/stacks/vaultwarden/data/bitwarden`, plus the backup target at `/opt/Bitwarden-Backup`
  - Syncthing: `/srv/docker/syncthing/obsidian` and the `syncthing_config` volume
  - Komodo: `postgres-data`, `ferretdb-state`, and any configured backups path
  - Erate: `erate_pg_data`

## Open Questions

- Do you want these stacks wired to Portainer via Git (one stack per compose path) for one-click updates from this repo?
- Should I add sanitized `.env.example` files and a brief per-stack README where missing?
- Any services that should be exposed through a reverse proxy with TLS instead of direct host ports?
