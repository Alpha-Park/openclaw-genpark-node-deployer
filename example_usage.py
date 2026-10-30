# -*- coding: utf-8 -*-
from client import OpenClawGenParkNodeDeployer

deployer = OpenClawGenParkNodeDeployer()

nodes = [
    {"node_id": "edge-node-01", "cpu_millicores": 8000, "ram_mb": 32768, "gpu_units": 1},
    {"node_id": "edge-node-02", "cpu_millicores": 4000, "ram_mb": 16384, "gpu_units": 0},
    {"node_id": "edge-node-03", "cpu_millicores": 4000, "ram_mb": 16384, "gpu_units": 0}
]

tasks = [
    {"task_id": "inference-engine", "cpu_millicores": 4000, "ram_mb": 16384, "gpu_units": 1},
    {"task_id": "web-crawler", "cpu_millicores": 2000, "ram_mb": 4096, "gpu_units": 0},
    {"task_id": "payment-signer", "cpu_millicores": 1000, "ram_mb": 2048, "gpu_units": 0},
    {"task_id": "mcp-gateway", "cpu_millicores": 1500, "ram_mb": 4096, "gpu_units": 0}
]

# 1. Multi-dimensional BFD Bin Packing
packing = deployer.schedule_multi_dimensional_bin_packing(nodes, tasks)
print(f"Scheduling Status: Success={packing['scheduling_success']} ({packing['total_tasks_scheduled']} scheduled)")
print(f"Cluster CPU Util: {packing['cluster_cpu_utilization_pct']}%, RAM Util: {packing['cluster_ram_utilization_pct']}%")

# 2. Canary Deployment Rollout
canary = deployer.calculate_rolling_canary_deployment_schedule(total_replicas=20)
print(); print(f"Canary Rollout: Total={canary['total_replicas']}, Max Surge={canary['max_surge_replicas']}")
for step in canary['canary_steps']:
    print(f"  Step {step['step']}: Canary {step['canary_replicas']} pods ({step['canary_target_pct']}%), Bake {step['bake_time_minutes']} min")

# 3. Cluster Load Shannon Entropy
entropy = deployer.evaluate_cluster_node_health_entropy([
    {"node_id": "edge-node-01", "cpu_utilization_pct": 45.0},
    {"node_id": "edge-node-02", "cpu_utilization_pct": 50.0},
    {"node_id": "edge-node-03", "cpu_utilization_pct": 48.0}
])
print(); print(f"Cluster Load Entropy: Ratio={entropy['entropy_ratio']} ({entropy['cluster_balance_status']})")
