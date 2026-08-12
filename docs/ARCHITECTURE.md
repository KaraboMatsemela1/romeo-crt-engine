# Architecture

```text
Source Registry / Research Notes
             |
             v
      Strategy Knowledge Base
             |
             v
       Frozen Strategy Spec
             |
             v
Market Data -> Market State -> CRT Detector -> Candidate Setup
                                            |
                                            v
                                      Setup Scoring
                                            |
                                            v
                                      Risk Engine
                                  /                    \
                                 v                      v
                          Backtest/Paper          Execution Adapter
                                                       |
                                                       v
                                                     Broker
                                                       |
                                                       v
                                                Reconciliation
                                                       |
                                                       v
                                              Journal / Feature Store
                                                       |
                                                       v
                                               Learning Candidates
```

## Module boundaries

- `market_data`: provider-neutral data contracts and ingestion
- `sessions`: timezone-aware trading windows
- `structure`: generic market-structure primitives
- `liquidity`: generic liquidity/sweep primitives
- `crt`: frozen CRT state machine/rules
- `signals`: candidate setup contracts
- `scoring`: deterministic/ML ranking, never broker authority
- `risk`: independent authorization and sizing
- `portfolio`: positions/equity/exposure model
- `execution`: paper/live broker adapters and reconciliation
- `backtest`: historical event loop and fill simulation
- `journal`: immutable-ish decision/order/trade audit events
- `learning`: offline candidate-model pipeline

## Dependency direction

Core market and strategy modules must not depend on a specific broker. Risk must not import an LLM client. Execution must consume explicit approved intents, not free-form natural-language decisions.
