# ROCm performance benchmark matrix

Use the same GGUF, context, prompt, and ROCm version for every run. Record prompt
processing and generation separately; a setting that improves one can regress the
other.

Build the normal HIP binary first:

```sh
make LLAMA_HIPBLAS=1 -j"$(nproc)"
```

For each model, run the matrix below with `--benchmark results.csv`. Start with
full KV offload and Flash Attention enabled. `--lowvram` and unified memory are
capacity fallbacks, not performance defaults.

| Variant | Settings |
| --- | --- |
| Baseline | `--usehipblas --gpulayers -1 --batchsize 512` |
| Prompt throughput | repeat with `--batchsize 1024` and `2048` if memory permits |
| GEMM path | compare default MMQ with `--nommq` |
| Long context | repeat baseline using `--quantkv q8_0` and `--quantkv q4_0` |
| hipBLASLt | rebuild with `LLAMA_HIPBLASLT=1`, then repeat the baseline |
| HIP graphs | compare the default with `LLAMA_HIP_GRAPHS=0` |
| Multi-GPU | test layer split first, then a measured `--tensor-split` ratio |

VMM is disabled by default. Only test `LLAMA_HIP_VMM=1` on a known-good ROCm
release, and keep it off if allocation failures, corrupted output, or regressions
appear. Include GPU, `gfx` target, ROCm version, model quantization, context,
batch size, prompt tokens/s, generation tokens/s, and peak VRAM in every result.
