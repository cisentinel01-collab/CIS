import asyncio
from typing import Dict, Any, List
from backend.app.schemas.playbook import PlaybookSchema, StepSchema

class WorkflowExecutor:
    def __init__(self, actions_registry: Dict[str, Any]):
        self.actions = actions_registry
        self.suspended_workflows = {} # {execution_id: state}

    async def execute_playbook(self, playbook: PlaybookSchema, context: Dict[str, Any], execution_id: str):
        print(f"Starting playbook execution: {playbook.name} ({execution_id})")
        steps_map = {step.id: step for step in playbook.steps}
        current_step_id = playbook.steps[0].id if playbook.steps else None

        await self._run_from_step(current_step_id, steps_map, context, execution_id)

    async def _run_from_step(self, step_id: str, steps_map: Dict[str, StepSchema], context: Dict[str, Any], execution_id: str):
        current_step_id = step_id
        while current_step_id:
            step = steps_map[current_step_id]

            if step.action.type == "human_approval":
                print(f"Workflow {execution_id} suspended for approval at step {step.name}")
                self.suspended_workflows[execution_id] = {
                    "next_step": step.next_step,
                    "steps_map": steps_map,
                    "context": context
                }
                return # Suspend execution

            success = await self.execute_step(step, context)
            if success:
                current_step_id = step.next_step
            else:
                current_step_id = step.on_failure

        print(f"Finished playbook execution for {execution_id}")

    async def resume_workflow(self, execution_id: str, approved: bool):
        if execution_id not in self.suspended_workflows:
            return False

        state = self.suspended_workflows.pop(execution_id)
        if approved:
            await self._run_from_step(state["next_step"], state["steps_map"], state["context"], execution_id)
        return True

    async def execute_step(self, step: StepSchema, context: Dict[str, Any]) -> bool:
        print(f"Executing step: {step.name}")
        action_type = step.action.type

        if action_type in self.actions:
            action_func = self.actions[action_type]
            try:
                await action_func(step.action.parameters, context)
                return True
            except Exception as e:
                print(f"Action failed: {e}")
                return False
        else:
            print(f"Unknown action type: {action_type}")
            return False

# Action Implementations
async def block_ip(params, context):
    ip = params.get("ip") or context.get("source_ip")
    print(f"BLOCKING IP: {ip}")
    await asyncio.sleep(0.1)

async def notify_slack(params, context):
    channel = params.get("channel")
    message = params.get("message")
    print(f"NOTIFY SLACK: [{channel}] {message}")
    await asyncio.sleep(0.1)

actions_registry = {
    "block_ip": block_ip,
    "notify_slack": notify_slack
}
