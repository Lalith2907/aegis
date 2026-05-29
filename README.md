# AEGIS

AEGIS is an AWS-based admission control system designed to protect backend APIs from traffic spikes and overload conditions.

Instead of allowing every incoming request to reach the backend blindly, AEGIS acts as an intelligent gatekeeper that decides whether a request should be processed immediately, queued for later execution, or rejected based on current system capacity and request priority.

## Architecture

![AEGIS Architecture](./diagrams/Architecture.png)

## Key Features

* Intelligent request admission control
* Priority-aware request handling
* Load shedding using HTTP 429 responses
* Backpressure through controlled queueing
* Distributed request buffering using Amazon SQS
* Asynchronous worker-based processing
* Real-time system metrics and observability

## Components

### FastAPI Ingress Layer

Receives incoming API requests and forwards them to the AEGIS admission controller.

### AEGIS Core

Implements admission control policies and decides whether a request should be ACCEPTED, QUEUED, or REJECTED.

### Amazon SQS

Acts as a distributed message queue for buffering requests during overload conditions.

### Worker Service

Consumes queued requests from Amazon SQS and processes them asynchronously.

## Request Lifecycle

1. Client sends a request to the API.
2. AEGIS evaluates current system load and queue depth.
3. Request is classified as:

   * **ACCEPT** → Process immediately.
   * **WAIT** → Push to Amazon SQS.
   * **REJECT** → Return HTTP 429.
4. Worker processes queued requests from Amazon SQS.
5. Metrics are updated and exposed through the monitoring endpoint.