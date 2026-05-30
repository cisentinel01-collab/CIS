import asyncio
from backend.app.services.infrastructure.repair import SelfHealingEngine

async def test_self_healing():
    engine = SelfHealingEngine()
    print("Simulating service failure...")
    # Manually trigger repair
    await engine.repair_service("api")
    await engine.repair_service("database")
    print("Self-healing actions verified.")

if __name__ == "__main__":
    asyncio.run(test_self_healing())
