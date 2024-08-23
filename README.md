# ticket_297240

Ticket 297240






## Approach 2

Use conda

https://anaconda.org/hcc/cellranger


## [FAILS] Approach 1: use Python files on clusters

```
 module load bioinfo-tools lz4/1.9.2 cellranger/8.0.1
python
```

```
import sys
sys.path.append('/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/')
from cellranger import *
```

### With `module load lz4/1.9.2`

```
 module load bioinfo-tools lz4/1.9.2 cellranger/8.0.1
python
```

```
import sys
sys.path.append('/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/')
from cellranger import *
```

```
>>> import cellranger.matrix as cr_matrix
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/cellranger/matrix.py", line 19, in <module>
    import cellranger.cr_io as cr_io
  File "/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/cellranger/cr_io.py", line 17, in <module>
    import lz4.frame as lz4
ModuleNotFoundError: No module named 'lz4'
```

However, there is no Python code for `lz4` on the cluster:

```
[richel@rackham2 1.9.2]$ pwd
/sw/libs/lz4/1.9.2

[richel@rackham2 1.9.2]$ find . | grep py
./rackham/src/contrib/debian/copyright
./rackham/src/contrib/meson/GetLz4LibraryVersion.py
./rackham/src/contrib/meson/InstallSymlink.py
./rackham/src/tests/test-lz4-list.py
./rackham/src/tests/test-lz4-speed.py
./rackham/src/tests/test-lz4-versions.py
```


### No module load lz4

```
 module load bioinfo-tools cellranger/8.0.1
python
```

```
import sys
sys.path.append('/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/')
from cellranger import *
```

```
>>> import cellranger.matrix as cr_matrix
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/cellranger/matrix.py", line 19, in <module>
    import cellranger.cr_io as cr_io
  File "/sw/bioinfo/Chromium-cellranger/8.0.1/bianca/lib/python/cellranger/cr_io.py", line 17, in <module>
    import lz4.frame as lz4
ModuleNotFoundError: No module named 'lz4'
```

