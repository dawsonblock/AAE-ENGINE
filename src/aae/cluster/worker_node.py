"""cluster/worker_node — represents a single distributed worker process.

A WorkerNode registers itself with the cluster, polls a task queue,
executes tasks through a local ExecutionRouter, and reports results back.
"""
from __future__ import annotations

import asyncio
import logging
import platform
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

log = logging.getLogger(__name__)


class NodeStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    DRAINING = "draining"
    OFFLINE = "offline"


@dataclass
class NodeInfo:
    node_id: str
    hostname: str
    worker_type: str          # "planner" | "agent" | "sandbox"
    status: NodeStatus = NodeStatus.IDLE
    current_task: Optional[str] = None
    tasks_completed: int = 0
    tasks_failed: int = 0
    started_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)

    def uptime(self) -> float:
        return time.time() - self.started_at


class WorkerNode:
    """Async worker that dequeues and executes tasks.

    Parameters
    ----------
    worker_type:
        Logical role of this worker (planner / agent / sandbox).
    queue_adapter:
        Queue from which to consume tasks.
    execution_router:
        Handles the actual task execution.
    task_callback:
        Called with ``(task_id, result)`` after each execution.
    concurrency:
        Max parallel tasks per node.
    poll_interval:
        Seconds between queue poll attempts when queue is empty.
    """

    def __init__(
        self,
        worker_type: str,
        queue_adapter: Any | None = None,
        execution_router: Any | None = None,
        task_callback: Optional[Callable[[str, Any], None]] = None,
        concurrency: int = 1,
        poll_interval: float = 2.0,
    ) -> None:
        self.info = NodeInfo(
            node_id=str(uuid.uuid4()),
            hostname=platform.node(),
            worker_type=worker_type,
        )
        self._queue = queue_adapter
        self._router = execution_router
        self._callback = task_callback
        self._concurrency = concurrency
        self._poll_interval = poll_interval
        self._sem = asyncio.Semaphore(concurrency)
        self._running = False
        self._tasks: List[asyncio.Task[None]] = []

    async def start(self) -> None:
        self._running = True
        self.info.status = NodeStatus.IDLE
        log.info(
            "worker_node id=%s type=%s started",
            self.info.node_id[:8],
            self.info.worker_type,
        )
        self._tasks.append(asyncio.create_task(self._poll_loop()))
        self._tasks.append(asyncio.create_task(self._heartbeat_loop()))

    async def stop(self) -> None:
        self._running = False
        self.info.status = NodeStatus.DRAINING
        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self.info.status = NodeStatus.OFFLINE
        log.info("worker_node id=%s stopped", self.info.node_id[:8])

    def status(self) -> Dict[str, Any]:
        return {
            "node_id": self.info.node_id,
            "hostname": self.info.hostname,
            "worker_type": self.info.worker_type,
            "status": self.info.status.value,
            "tasks_completed": self.info.tasks_completed,
            "tasks_failed": self.info.tasks_failed,
            "uptime_s": self.info.uptime(),
        }

    async def _poll_loop(self) -> None:
        while self._running:
            task = await self._dequeue()
            if task is None:
                await asyncio.sleep(self._poll_interval)
                continue
            async with self._sem:
                await self._execute(task)

    async def _heartbeat_loop(self) -> None:
        while self._running:
            self.info.last_heartbeat = time.time()
            await asyncio.sleep(10)

    async def _dequeue(self) -> Optional[Dict[str, Any]]:
        if self._queue is None:
            await asyncio.sleep(self._poll_interval)
            return None
        try:
            return await self._queue.consume(worker_type=self.info.worker_type)
        except Exception as exc:
            log.debug("dequeue error: %s", exc)
            return None

    async def _execute(self, task: Dict[str, Any]) -> None:
        task_id = task.get("task_id", "?")
        self.info.status = NodeStatus.BUSY
        self.info.current_task = task_id
        try:
            if self._router:
                result = await self._router.route(
                    action=task.get("action", "run_command"),
                    payload=task.get("payload", {}),
                    timeout=float(task.get("timeout", 120)),
                )
            else:
                await asyncio.sleep(0.1)
                result = {"status": "dry_run"}
            self.info.tasks_completed += 1
            if self._callback:
                self._callback(task_id, result)
        except Exception as exc:
            self.info.tasks_failed += 1
            log.error("task %s failed: %s", task_id, exc)
        finally:
            self.info.status = NodeStatus.IDLE
            self.info.current_task = None
