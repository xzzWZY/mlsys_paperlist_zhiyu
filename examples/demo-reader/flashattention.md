---
paper_id: "arxiv:2205.14135"
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
url: "https://arxiv.org/abs/2205.14135"
year: 2022
venue: "arXiv"
topics: [compilers-kernels, architectures]
example_added_at: "2026-09-30T16:00:00Z"
---

## Summary
FlashAttention computes exact attention with an IO-aware tiled algorithm. It reduces transfers between GPU high-bandwidth memory and on-chip SRAM, avoiding materialization of the full attention matrix.

## Relevance to my research
Example discussion prompt: which other model operations are limited by memory traffic, and could benefit from a similar IO-aware design?

## Limitations / Questions
How does the benefit vary with sequence length and GPU architecture? This example is included only to demonstrate the submission format.
