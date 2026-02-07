# AEGIS

AEGIS is an AWS based admission control system designed to protect backend APIs from traffic spikes.

Instead of allowing every incoming request to reach the backend blindly, AEGIS acts as an intelligent gatekeeper that decides whether a request should be accepted, queued, or rejected based on current system capacity and reuest priority.

## Architecture

![AEGIS Architecture](./diagrams/architecture.png)