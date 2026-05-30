import yaml
import json
from typing import List, Dict, Any

class RuleEngine:
    def __init__(self, rules_yaml: str):
        self.rules = yaml.safe_load(rules_yaml).get("rules", [])
        self.event_history = [] # For temporal correlation

    def evaluate(self, event: dict):
        self.event_history.append(event)
        # Keep last 1000 events for correlation
        if len(self.event_history) > 1000:
            self.event_history.pop(0)

        alerts = []
        for rule in self.rules:
            if rule.get("type") == "correlation":
                if self._check_correlation(rule, event):
                    alerts.append(self._build_alert(rule, event))
            elif self._matches(rule["condition"], event):
                alerts.append(self._build_alert(rule, event))
        return alerts

    def _build_alert(self, rule, event):
        alert = {
            "rule_id": rule["id"],
            "rule_name": rule["name"],
            "severity": rule["severity"],
            "mitre_attack": rule.get("mitre_attack", []),
            "event": event
        }
        return alert

    def _check_correlation(self, rule, current_event):
        # Simple temporal correlation: X events of type Y in Z seconds
        condition = rule["condition"]
        target_event_type = condition["event_type"]
        threshold = condition["threshold"]
        window = condition["window_seconds"]

        # In a real app, use timestamps to filter the window
        count = sum(1 for e in self.event_history if e.get("event.type") == target_event_type)
        return count >= threshold

    def _matches(self, condition: dict, event: dict):
        field = condition.get("field")
        value = condition.get("value")
        operator = condition.get("operator", "eq")

        event_value = self._get_nested_field(event, field)

        if operator == "eq":
            return event_value == value
        elif operator == "contains":
            return value in str(event_value)
        return False

    def _get_nested_field(self, data, field_path):
        keys = field_path.split('.')
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        return data

# MITRE ATT&CK Mapping Example
mitre_mapping = {
    "brute_force": {"tactic": "Credential Access", "technique": "T1110"},
    "malware_detected": {"tactic": "Execution", "technique": "T1204"}
}
