from backend.app.services.siem.rules import RuleEngine
import yaml

def test_correlation():
    rules_yaml = """
rules:
  - id: brute_force_detected
    name: Brute Force Correlation
    type: correlation
    severity: high
    mitre_attack: ["T1110"]
    condition:
      event_type: auth_failure
      threshold: 3
      window_seconds: 60
"""
    engine = RuleEngine(rules_yaml)

    event = {"event.type": "auth_failure", "message": "failed login"}

    # Send 2 events - no alert
    assert len(engine.evaluate(event)) == 0
    assert len(engine.evaluate(event)) == 0

    # Send 3rd event - alert!
    alerts = engine.evaluate(event)
    assert len(alerts) == 1
    assert alerts[0]["rule_name"] == "Brute Force Correlation"
    assert "T1110" in alerts[0]["mitre_attack"]
    print("Correlation and MITRE mapping verified.")

if __name__ == "__main__":
    test_correlation()
