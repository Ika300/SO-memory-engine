# Installation

SO Memory Engine currently depends on SO Memory Kernel.

The easiest alpha install is now one repository plus editable install.

## 1. Clone Engine

```bash
git clone https://github.com/Ika300/SO-memory-engine.git
cd SO-memory-engine
```

## 2. Install Engine

Windows:

```bash
py -3 -m pip install -e .
```

Non-Windows:

```bash
python -m pip install -e .
```

This installs SO Memory Kernel from its GitHub repository through the Engine dependency.

## 3. Run quickstart

Windows:

```bash
py -3 quickstart.py
```

Non-Windows:

```bash
python quickstart.py
```

The quickstart writes:

```text
outputs/engine_quickstart/context_pack.txt
outputs/engine_quickstart/context_pack.json
outputs/engine_quickstart/engine_result.json
```

## Windows helper

You may also run:

```bat
setup_engine_demo.bat
```

This installs the Engine and runs the Engine-only quickstart.

## Manual sibling-repository setup

Use this if you want to develop Kernel and Engine side by side, or if direct Git dependency installation fails. The default install uses the GitHub Kernel package; this manual setup restores local editable Kernel development.

Recommended local layout:

```text
Desktop/
  SO_Memory_Kernel/
  SO_Memory_Engine/
```

Clone both repositories:

```bash
git clone https://github.com/Ika300/so-memory-kernel.git SO_Memory_Kernel
git clone https://github.com/Ika300/SO-memory-engine.git SO_Memory_Engine
```

Install Kernel locally from `SO_Memory_Engine`:

```bash
py -3 -m pip install -e ..\SO_Memory_Kernel
```

Install Engine locally:

```bash
py -3 -m pip install -e .
```

On non-Windows systems:

```bash
python -m pip install -e ../SO_Memory_Kernel
python -m pip install -e .
```

## Verify

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

## Current alpha limitation

SO Memory Kernel is not yet assumed to be available from PyPI.

That means the current install path relies on GitHub or local editable installation. This is intentionally stated plainly to avoid giving users a broken PyPI-style expectation.