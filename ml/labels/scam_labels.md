# Zero-Shot Candidate Labels

Candidate labels fed to the zero-shot classifier for scam-script tagging.
Tune wording during testing — label phrasing strongly affects zero-shot
accuracy.

```
- digital arrest / fake CBI or ED officer
- fake courier or parcel (customs) scam
- KYC / bank account update fraud
- OTP / UPI PIN phishing
- investment or stock trading scam
- loan app harassment / extortion
- electricity bill disconnection scam
- job offer / work-from-home scam
- lottery or prize scam
- SIM swap / telecom fraud
- legitimate / not a scam
```

## Notes
- Keep a separate short list for the WhatsApp quick-check (fewer labels = faster,
  clearer results).
- Consider hierarchical labels later (category -> subtype) for the intel graph.
