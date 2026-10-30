# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Node Deployer Client
Pure Python Standard Library (Zero External Dependencies)
Implements multi-dimensional bin-packing (Best Fit Decreasing) and rolling blue-green canary deployment scheduling.
"""

import math
from typing import Dict, Any, List, Optional

class OpenClawGenParkNodeDeployer:
    """
    Infrastructure orchestration and container scheduling engine for multi-agent workloads.
    """

    def __init__(self):
        pass

    def schedule_multi_dimensional_bin_packing(
        self,
        nodes: List[Dict[str, Any]],
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Schedules agent workloads onto compute nodes using Multi-Dimensional Best Fit Decreasing (BFD).
        Evaluates CPU millicores, RAM MB, and GPU units.
        
        Fitness metric: Euclidean distance of leftover capacity vector.
        """
        # Copy nodes state
        available_nodes = []
        for n in nodes:
            available_nodes.append({
                "node_id": n.get("node_id", f"node_{len(available_nodes)}"),
                "total_cpu": float(n.get("cpu_millicores", 4000)),
                "total_ram": float(n.get("ram_mb", 16384)),
                "total_gpu": float(n.get("gpu_units", 0)),
                "remaining_cpu": float(n.get("cpu_millicores", 4000)),
                "remaining_ram": float(n.get("ram_mb", 16384)),
                "remaining_gpu": float(n.get("gpu_units", 0)),
                "assigned_tasks": []
            })

        # Sort tasks descending by composite resource weight
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (
                float(t.get("cpu_millicores", 500)) * 1.0 +
                float(t.get("ram_mb", 1024)) * 0.25 +
                float(t.get("gpu_units", 0)) * 5000.0
            ),
            reverse=True
        )

        unassigned_tasks = []

        for task in sorted_tasks:
            t_id = task.get("task_id", "task")
            t_cpu = float(task.get("cpu_millicores", 500))
            t_ram = float(task.get("ram_mb", 1024))
            t_gpu = float(task.get("gpu_units", 0))

            best_node = None
            min_residual_norm = float("inf")

            for node in available_nodes:
                if (node["remaining_cpu"] >= t_cpu and
                    node["remaining_ram"] >= t_ram and
                    node["remaining_gpu"] >= t_gpu):
                    
                    # Residual capacity after placement
                    res_cpu = (node["remaining_cpu"] - t_cpu) / max(node["total_cpu"], 1.0)
                    res_ram = (node["remaining_ram"] - t_ram) / max(node["total_ram"], 1.0)
                    res_gpu = (node["remaining_gpu"] - t_gpu) / max(node["total_gpu"], 1.0) if node["total_gpu"] > 0 else 0.0

                    residual_norm = math.sqrt(res_cpu**2 + res_ram**2 + res_gpu**2)
                    
                    if residual_norm < min_residual_norm:
                        min_residual_norm = residual_norm
                        best_node = node

            if best_node:
                best_node["remaining_cpu"] -= t_cpu
                best_node["remaining_ram"] -= t_ram
                best_node["remaining_gpu"] -= t_gpu
                best_node["assigned_tasks"].append({
                    "task_id": t_id,
                    "cpu_millicores": t_cpu,
                    "ram_mb": t_ram,
                    "gpu_units": t_gpu
                })
            else:
                unassigned_tasks.append(t_id)

        # Compute cluster utilization
        tot_cpu = sum(n["total_cpu"] for n in available_nodes)
        tot_ram = sum(n["total_ram"] for n in available_nodes)
        rem_cpu = sum(n["remaining_cpu"] for n in available_nodes)
        rem_ram = sum(n["remaining_ram"] for n in available_nodes)

        cpu_util = round(((tot_cpu - rem_cpu) / tot_cpu * 100.0) if tot_cpu > 0 else 0.0, 2)
        ram_util = round(((tot_ram - rem_ram) / tot_ram * 100.0) if tot_ram > 0 else 0.0, 2)

        return {
            "scheduling_success": len(unassigned_tasks) == 0,
            "total_tasks_scheduled": len(sorted_tasks) - len(unassigned_tasks),
            "unassigned_tasks_count": len(unassigned_tasks),
            "unassigned_tasks": unassigned_tasks,
            "cluster_cpu_utilization_pct": cpu_util,
            "cluster_ram_utilization_pct": ram_util,
            "node_assignments": available_nodes
        }

    def calculate_rolling_canary_deployment_schedule(
        self,
        total_replicas: int,
        max_surge_pct: float = 25.0,
        max_unavailable_pct: float = 20.0,
        canary_step_percentages: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Calculates phased canary progression steps, blast radius bounds, and health gate criteria.
        """
        if canary_step_percentages is None:
            canary_step_percentages = [10, 25, 50, 100]

        total = max(1, total_replicas)
        max_surge = max(1, math.ceil(total * (max_surge_pct / 100.0)))
        max_unavailable = max(0, math.floor(total * (max_unavailable_pct / 100.0)))
        min_available = total - max_unavailable

        schedule = []
        for step_idx, pct in enumerate(canary_step_percentages):
            target_canary_count = math.ceil(total * (pct / 100.0))
            baseline_count = total - target_canary_count
            
            schedule.append({
                "step": step_idx + 1,
                "canary_target_pct": pct,
                "canary_replicas": target_canary_count,
                "baseline_replicas": baseline_count,
                "max_allowed_failures": max(1, math.floor(target_canary_count * 0.05)),
                "bake_time_minutes": 15 if pct < 50 else 30
            })

        return {
            "total_replicas": total,
            "max_surge_replicas": max_surge,
            "max_unavailable_replicas": max_unavailable,
            "min_healthy_threshold": min_available,
            "canary_steps": schedule
        }

    def evaluate_cluster_node_health_entropy(
        self,
        node_metrics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluates cluster load imbalance using Shannon entropy across CPU and memory loads.
        High entropy indicates even distribution; low entropy signals hotspot concentration.
        """
        if not node_metrics:
            return {
                "node_count": 0,
                "load_entropy": 0.0,
                "max_possible_entropy": 0.0,
                "entropy_ratio": 0.0,
                "cluster_balance_status": "EMPTY"
            }

        n = len(node_metrics)
        if n == 1:
            return {
                "node_count": 1,
                "load_entropy": 1.0,
                "max_possible_entropy": 1.0,
                "entropy_ratio": 1.0,
                "cluster_balance_status": "BALANCED_SINGLE_NODE"
            }

        cpu_loads = [max(0.01, float(m.get("cpu_utilization_pct", 10.0))) for m in node_metrics]
        total_cpu = sum(cpu_loads)
        
        # Probabilities
        probs = [c / total_cpu for c in cpu_loads]
        
        # Shannon Entropy H = - sum(p * log2(p))
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        max_entropy = math.log2(n)
        ratio = round(entropy / max_entropy, 4) if max_entropy > 0 else 1.0

        if ratio >= 0.90:
            status = "OPTIMALLY_BALANCED"
        elif ratio >= 0.75:
            status = "MODERATELY_BALANCED"
        else:
            status = "IMBALANCED_HOTSPOTS_DETECTED"

        return {
            "node_count": n,
            "load_entropy": round(entropy, 4),
            "max_possible_entropy": round(max_entropy, 4),
            "entropy_ratio": ratio,
            "cluster_balance_status": status
        }
