import pathlib
import os
import uuid

from atomicwrites import atomic_write as _backend_writer
from atomicwrites import AtomicWriter
from contextlib import contextmanager
from tempfile import NamedTemporaryFile


class SuffixWriter(AtomicWriter):
    def get_fileobject(self, **kwargs):
        """
        By subclassing the Atomic writer, suffix writer only requires the override of one method
        """
        suffix = pathlib.Path(self._path).suffix
        f = super().get_fileobject(suffix=suffix, **kwargs)
        return f


@contextmanager
def atomic_write(file, mode="w", as_file=True, **kwargs):
    """Write a file atomically
    :param file: str or :class:`os.PathLike` target to write
    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string
    :param kwargs: anything else needed to open the file
    :raises: FileExistsError if target exists
    Example::
        with atomic_write("hello.txt") as f:
            f.write("world!")
    """

    # If the write fails, then restore the original configuration file
    if os.path.isfile(file):
        save_path = file
        tmp = file + ".{}.old".format(str(uuid.uuid4().hex)[:12])
        os.rename(file, tmp)

    try:
        suffix = pathlib.Path(file).suffix

        atomic_tmp_file = NamedTemporaryFile(mode=mode, delete=False, suffix=suffix)
        if as_file:
            yield_obj = atomic_tmp_file
        else:
            yield_obj = atomic_tmp_file.name

        yield yield_obj

        if os.path.exists(atomic_tmp_file.name):
            os.rename(atomic_tmp_file.name, file)
    except IOError:
        os.rename(tmp, file)

    finally:
        if os.path.exists(atomic_tmp_file.name):
            os.remove(atomic_tmp_file.name)
