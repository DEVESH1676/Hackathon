import sys
import os
sys.path.append(os.getcwd())
from core.classifier import TicketClassifier

clf = TicketClassifier()
title = "VPN connection fails for remote users"
desc = "Users are unable to establish VPN connections, receiving error 619. This is affecting the entire remote sales team. Initial checks in Splunk show high load on the primary VPN concentrator."

result = clf.classify(title, desc)
print(f"Method: {result['method']}")
print(f"Confidence: {result['confidence']}")
print(f"Category: {result['category']}")
