# Installation

SO Memory Engine currently depends on SO Memory Kernel.

During alpha development, both repositories should be cloned side by side.

Recommended local layout:

```text
Desktop/
  SO_Memory_Kernel/
  SO_Memory_Engine/
```

## 1. Clone both repositories

```bash
git clone https://github.com/Ika300/so-memory-kernel.git SO_Memory_Kernel
git clone https://github.com/Ika300/SO-memory-engine.git SO_Memory_Engine
```

## 2. Install Kernel locally

From `SO_Memory_Engine`:

```bash
py -3 -m pip install -e ..\SO_Memory_Kernel
```

On non-Windows systems:

```bash
python -m pip install -e ../SO_Memory_Kernel
```

## 3. Install Engine locally

From `SO_Memory_Engine`:

```bash
py -3 -m pip install -e .
```

On non-Windows systems:

```bash
python -m pip install -e .
```

## 4. Verify

```bash
py -3 quickstart.py
py -3 -m unittest discover -s tests -p '*test*.py' -v
py -3 benchmarks\run_benchmarks.py
py -3 benchmarks\run_comparative_benchmarks.py
```

Expected current local result:

```text
Engine tests pass
Behavioral benchmarks pass
Comparative benchmarks pass
```

## Windows helper

You may run:

```bat
setup_engine_demo.bat
```

This installs Kernel and Engine locally, then runs the Engine-only quickstart.

## Current alpha limitation

SO Memory Kernel is not yet assumed to be available from PyPI.

That means `pip install so-memory-engine` is not the current installation path. The current alpha path is editable local installation from cloned repositories.

This is intentionally stated plainly to avoid giving users a broken install command.