#!/usr/bin/env python3
import atheris
import sys
import fuzz_helpers
import io
from contextlib import contextmanager

with atheris.instrument_imports(include=['libtiff']):
    from libtiff import TIFFfile

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.BytesIO()
    sys.stderr = io.BytesIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

ctr = 0

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    global ctr
    ctr += 1
    with nostdout():
        try:
            with fdp.ConsumeTemporaryFile(suffix='.tif', as_bytes=True) as f:
                TIFFfile(f)
        except ValueError:
            return -1
        except IndexError as e:
            if 'out of bounds' in str(e):
                return -1
        except TypeError:
            if ctr > 100:
             raise
        return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
