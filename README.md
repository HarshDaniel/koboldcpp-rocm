# koboldcpp-ROCm for AMD

An AMD ROCm port of [KoboldCpp](https://github.com/LostRuins/koboldcpp), a lightweight application for running GGUF language models locally with a built-in web interface.

## Features

- CPU inference and AMD GPU acceleration through ROCm/hipBLAS.
- Full or partial GPU layer offloading.
- Support for GGUF language models, with compatibility for older GGML models where supported.
- KoboldAI Lite interface with chat, adventure, instruct, and storywriter modes.
- OpenAI-compatible and other API endpoints.
- Image generation, speech-to-text, text-to-speech, vision, and other features available in KoboldCpp.

## Quick Linux install

Clone the repository, build the ROCm version, and start the GUI:

```sh
git clone https://github.com/HarshDaniel/koboldcpp-rocm.git
cd koboldcpp-rocm
make LLAMA_HIPBLAS=1 -j4
python ./koboldcpp.py
```

When the GUI appears, select **Use hipBLAS (ROCm)** and set the number of GPU layers. The server is normally available at `http://localhost:5001`.

## Linux

Build the ROCm backend from source:

```sh
make LLAMA_HIPBLAS=1 -j4
```

Start the GUI:

```sh
python koboldcpp.py
```

Or start directly from the command line:

```sh
python koboldcpp.py --usecublas --gpulayers 18 --contextsize 4096 --model /path/to/model.gguf
```

The `--usecublas` option is the historical command-line name used by KoboldCpp for the hipBLAS/ROCm backend. Adjust `--gpulayers` to fit your GPU memory.

## Obtaining GGUF Models

KoboldCpp does not include model weights. Download models in `.gguf` format from a trusted model host, then select the file in the GUI or pass it with `--model`.

- [Hugging Face GGUF models](https://huggingface.co/models?library=gguf&sort=trending)
- [Bartowski's GGUF models](https://huggingface.co/bartowski)
- [Unsloth's GGUF models](https://huggingface.co/unsloth)
- [KoboldAI models](https://huggingface.co/KoboldAI)
- [GGUF conversion tools](https://kcpptools.concedo.workers.dev) for converting and quantizing compatible models yourself.

Choose a quantization that fits your available RAM or VRAM. `Q4_K_M` is a common starting point, while larger quantizations generally require more memory.

## Fedora

Fedora's ROCm packages may place LLVM tools outside the paths expected by the build system. Install the required development packages:

```sh
sudo dnf install rocblas-devel hipblas-devel rocm-llvm
```

If the LLVM tools are installed under `/usr/lib64/llvm17/bin`, create the expected links:

```sh
sudo mkdir -p /opt/rocm/llvm/bin
sudo ln -s /usr/lib64/llvm17/bin/clang /opt/rocm/llvm/bin/clang
sudo ln -s /usr/lib64/llvm17/bin/clang++ /opt/rocm/llvm/bin/clang++
sudo ln -s /usr/lib64/rocm/llvm/bin/amdgpu-arch /opt/rocm/llvm/bin/amdgpu-arch
```

Then follow the [Linux](#linux) build instructions.

## Improving Performance

- Increase `--gpulayers` until the model uses most of the available VRAM without running out of memory.
- Use `--contextsize` carefully; larger contexts require more memory.
- Try `--usecublas mmq` or `--usecublas mmq lowvram` for ROCm systems when appropriate.
- Use `--threads` and `--blasthreads` to tune CPU work for your system.
- If you encounter crashes, try `--noblas`, `--noavx2`, or `--nommap`.
- Run `python koboldcpp.py --help` to see all available options.

## Third-party resources

These community resources are unofficial and may be outdated or unmaintained:

- [KoboldCpp Wiki](https://github.com/LostRuins/koboldcpp/wiki)
- [KoboldCpp API documentation](https://lite.koboldai.net/koboldcpp_api)
- [KoboldAI Discord](https://koboldai.org/discord)
- [KoboldCpp Docker images](https://hub.docker.com/r/koboldai/koboldcpp)

## Considerations

- Model files are not distributed with this repository.
- ROCm support depends on your GPU, ROCm version, distribution, and installed drivers.
- GPU offloading improves speed but uses VRAM; reduce the number of GPU layers if loading fails.
- Only download model files and binaries from sources you trust.
- This fork focuses on AMD ROCm support. For general KoboldCpp support, consult the [upstream project](https://github.com/LostRuins/koboldcpp).

## License

- KoboldCpp and KoboldAI Lite are licensed under the [GNU Affero General Public License v3.0](https://github.com/LostRuins/koboldcpp/blob/concedo/LICENSE).
- The underlying [llama.cpp](https://github.com/ggml-org/llama.cpp) project is licensed under the MIT License.
- Other bundled components may have their own licenses; see their source files and license notices.

## Notes

- API endpoints are available under `/api`; an OpenAI-compatible API is available under `/v1` when the server is running.
- Run `python koboldcpp.py --help` for the complete command-line reference.
- Contributions and bug reports are welcome through the [issue tracker](https://github.com/HarshDaniel/koboldcpp-rocm/issues).

## Where can I download model files?

The best place to find GGUF text models is [Hugging Face](https://huggingface.co/models?library=gguf). Search for a model name followed by `GGUF`, and choose a quantization that fits your hardware. For image-generation models, [Civitai](https://civitai.com/) is another commonly used source.
