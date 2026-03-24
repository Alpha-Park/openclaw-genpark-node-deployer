---
name: genpark-node-deployer
description: Autonomous infrastructure engine to provision and host OpenClaw nodes.
version: 1.0.0
---

# genpark-node-deployer

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
