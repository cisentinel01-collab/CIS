import asyncio
from backend.app.schemas.playbook import PlaybookSchema, StepSchema, ActionSchema
from backend.app.services.soar.engine import WorkflowExecutor, actions_registry

async def test_human_approval():
    playbook = PlaybookSchema(
        id="p1",
        name="Approval Test",
        description="Testing approval logic",
        trigger_condition={"event": "sensitive_action"},
        steps=[
            StepSchema(
                id="s1",
                name="Ask Permission",
                action=ActionSchema(id="a1", type="human_approval", parameters={}),
                next_step="s2"
            ),
            StepSchema(
                id="s2",
                name="Critical Action",
                action=ActionSchema(id="a2", type="block_ip", parameters={"ip": "1.1.1.1"}),
                next_step=None
            )
        ]
    )

    executor = WorkflowExecutor(actions_registry)
    execution_id = "exec_001"

    # Start execution - should suspend
    await executor.execute_playbook(playbook, {}, execution_id)
    assert execution_id in executor.suspended_workflows
    print("Workflow suspended as expected.")

    # Resume execution
    print("Resuming workflow...")
    await executor.resume_workflow(execution_id, approved=True)
    assert execution_id not in executor.suspended_workflows
    print("Workflow finished as expected.")

if __name__ == "__main__":
    asyncio.run(test_human_approval())
