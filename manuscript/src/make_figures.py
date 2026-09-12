#!/usr/bin/env python3
"""Deprecated shim. All figure code now lives in make_all_figures.py."""
import runpy, sys
sys.argv = [sys.argv[0]]
runpy.run_path("make_all_figures.py", run_name="__main__")
