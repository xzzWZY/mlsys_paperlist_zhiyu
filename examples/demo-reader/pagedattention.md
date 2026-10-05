---
paper_id: "arxiv:2309.06180"
title: "Efficient Memory Management for Large Language Model Serving with PagedAttention"
url: "https://arxiv.org/abs/2309.06180"
year: 2023
venue: "arXiv"
topics: [llm-inference, hardware-systems]
example_added_at: "2026-10-05T16:00:00Z"
---

## Summary
PagedAttention manages the KV cache in blocks, borrowing ideas from virtual memory. The vLLM serving system uses this design to reduce fragmentation and share cache memory, enabling larger batches.

## Relevance to my research
Example discussion prompt: how do cache allocation and request scheduling interact when serving workloads with different sequence lengths?

## Limitations / Questions
How would the tradeoffs change for workloads dominated by short requests? This is an illustrative reading note, not a claim that the account owner has read the paper.
