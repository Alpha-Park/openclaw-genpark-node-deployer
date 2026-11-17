---
name: genpark-node-deployer
description: Autonomous infrastructure engine to provision and host OpenClaw nodes.
version: 1.0.0
---

# genpark-node-deployer

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.

## Overview
This skill operates as a DevOps engineer for the OpenClaw ecosystem. It connects to Cloud service APIs (like DigitalOcean, Hetzner, AWS) to spin up new Virtual Private Servers, configures Docker, and automatically deploys a fresh instance of an OpenClaw agent node without needing a human to touch an SSH terminal.

## Core Capabilities
- **Infrastructure Provisioning**: Securely purchase and spin up compute instances using user-provided API keys.
- **Node Configuration**: Automatically run initialization scripts to install Docker, Node.js, and pull the latest `openclaw` core repositories.
- **Health Monitoring**: Check the heartbeat of deployed nodes and ensure the agent processes remain active.

## Usage Guide
When a user asks to deploy a new agent node:
1. Verify if the user has configured their Cloud Provider API keys.
2. Formulate the API payload to request a server (e.g., Ubuntu 22.04 LTS, 2GB RAM minimum).
3. Once the server IP is returned, execute remote startup scripts to launch the OpenClaw agent.
4. Return the IP, active ports, and Node ID to the user.
