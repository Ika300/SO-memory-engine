# Installation

SO Memory Engine currently depends on SO Memory Kernel.

If you only want to run the complete free trial on Windows, start here:

```bat
setup_free_trial.bat
```

This installs Kernel, Engine, bundled Extractor Free, and runs `quickstart.py`.

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

## 4. Install bundled Extractor Free

From `SO_Memory_Engine`:

```bash
py -3 -m pip install -e SO_Extractor_Free
```

On non-Windows systems:

```bash
python -m pip install -e SO_Extractor_Free
```

## 5. Verify

```bash
py -3 quickstart.py
py -3 examples\quickstart_demo.py
py -3 -m unittest discover -s tests -p '*test*.py' -v
py -3 benchmarks\run_benchmarks.py
py -3 benchmarks\run_comparative_benchmarks.py
```

Expected current local result:

```text
Engine tests: 35/35 passed
Behavioral benchmarks: 6/6 passed
Comparative benchmarks: 3/3 passed
```

## Current alpha limitation

SO Memory Kernel is not yet assumed to be available from PyPI.

That means `pip install so-memory-engine` is not the current installation path. The current alpha path is editable local installation from cloned repositories.

This is intentionally stated plainly to avoid giving users a broken install command.
