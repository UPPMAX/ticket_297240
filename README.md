# ticket_297240

Ticket 297240

## Approach 5: Use Singularity from BZL file

Due to file that 10x uses <https://github.com/10XGenomics/cellranger/blob/main/conda_spec.bzl>

Here is a Docker file: https://hub.docker.com/r/chainguard/bazel

Docker pull command:

```
docker pull chainguard/bazel:latest
```

```
bazel build conda_spec.bzl
```

Build Singularity file:

```
Bootstrap: docker
From: chainguard/bazel:latest

%post
    # From https://github.com/brucemoran/Singularity/blob/8eb44591284ffb29056d234c47bf8b1473637805/shub/bases/recipe.CentOs7-R_3.5.2#L21
    echo 'export LANG=en_US.UTF-8 LANGUAGE=C LC_ALL=C LC_CTYPE=C LC_COLLATE=C  LC_TIME=C LC_MONETARY=C LC_PAPER=C LC_MEASUREMENT=C' >> $SINGULARITY_ENVIRONMENT

    cd /opt
    git clone https://github.com/10XGenomics/cellranger
    cd cellranger

    bazel build conda_spec.bzl

%runscript
python "$@"
```

Build:

```
./build_container.sh
```

Error:

```
ERROR: The 'build' command is only supported from within a workspace (below a directory having a WORKSPACE file).
See documentation at https://bazel.build/concepts/build-ref#workspace
FATAL:   While performing build: while running engine: exit status 2
```

Use tip from https://stackoverflow.com/q/61869719 .

Then:

```
./build_container.sh
```

Gives error:

```
+ touch WORKSPACE
+ bazel build conda_spec.bzl
Extracting Bazel installation...
Starting local Bazel server and connecting to it...
WARNING: --enable_bzlmod is set, but no MODULE.bazel file was found at the workspace root. Bazel will create an empty MODULE.bazel file. Please consider migrating your external dependencies from WORKSPACE to MODULE.bazel. For more details, please refer to https://github.com/bazelbuild/bazel/issues/18958.
WARNING: Target pattern parsing failed.
ERROR: Skipping 'conda_spec.bzl': couldn't determine target from filename 'conda_spec.bzl'
ERROR: couldn't determine target from filename 'conda_spec.bzl'
INFO: Elapsed time: 7.913s
INFO: 0 processes.
ERROR: Build did NOT complete successfully
FATAL:   While performing build: while running engine: exit status 1
```

Added tip from https://raw.githubusercontent.com/10XGenomics/cellranger/main/conda_spec.bzl to add content to WORKSPACE.

Build again:

```
+ echo 'load(":conda_spec.bzl", "anaconda_workspace")'
+ echo 'anaconda_workspace()'
+ bazel build conda_spec.bzl
Extracting Bazel installation...
Starting local Bazel server and connecting to it...
WARNING: --enable_bzlmod is set, but no MODULE.bazel file was found at the workspace root. Bazel will create an empty MODULE.bazel file. Please consider migrating your external dependencies from WORKSPACE to MODULE.bazel. For more details, please refer to https://github.com/bazelbuild/bazel/issues/18958.
ERROR: Error computing the main repository mapping: Every .bzl file must have a corresponding package, but '//:conda_spec.bzl' does not have one. Please create a BUILD file in the same or any parent directory. Note that this BUILD file does not need to do anything except exist.
Computing main repo mapping: 
FATAL:   While performing build: while running engine: exit status 1
```

OK, create an empty BUILD file ...




With content in the BUILD file:
Run again, new error:

```
+ touch BUILD
+ bazel build conda_spec.bzl
Extracting Bazel installation...
Starting local Bazel server and connecting to it...
WARNING: --enable_bzlmod is set, but no MODULE.bazel file was found at the workspace root. Bazel will create an empty MODULE.bazel file. Please consider migrating your external dependencies from WORKSPACE to MODULE.bazel. For more details, please refer to https://github.com/bazelbuild/bazel/issues/18958.
ERROR: Failed to load Starlark extension '@@tenx_bazel_rules//rules:conda_package_repository.bzl'.
Cycle in the workspace file detected. This indicates that a repository is used prior to being defined.
The following chain of repository dependencies lead to the missing definition.
 - @@tenx_bazel_rules
This could either mean you have to add the '@@tenx_bazel_rules' repository with a statement like `http_archive` in your WORKSPACE file (note that transitive dependencies are not added automatically), or move an existing definition earlier in your WORKSPACE file.
ERROR: Error computing the main repository mapping: cycles detected during computation of main repo mapping
Computing main repo mapping: 
FATAL:   While performing build: while running engine: exit status 37
```


## Approach 4: Use Singularity from conda


https://anaconda.org/hcc/cellranger


Approach 5 seems easier.

## Approach 3: Use conda from module

Loading the conda module:

```
module load conda
```

Works:

```
[richel@rackham1 ~]$ module load conda
The variable CONDA_ENVS_PATH contains the location of your environments. Set it to your project's environments folder if you have one.
Otherwise, the default is ~/.conda/envs. Remember to export the variable with export CONDA_ENVS_PATH=/proj/...

You may run "source conda_init.sh" to initialise your shell to be able
to run "conda activate" and "conda deactivate" etc.
Just remember that this command adds stuff to your shell outside the scope of the module system.

REMEMBER TO USE 'conda clean -a' once in a while
```

Naive install fails:

```
conda install cellranger
```

With error:

```
[richel@rackham1 ~]$ conda install cellranger
Retrieving notices: ...working... done
Channels:
 - file:///sw/apps/conda/latest/rackham/local_repo/conda-forge
 - file:///sw/apps/conda/latest/rackham/local_repo/scilifelab-lts
 - file:///sw/apps/conda/latest/rackham/local_repo/r
 - file:///sw/apps/conda/latest/rackham/local_repo/main
 - file:///sw/apps/conda/latest/rackham/local_repo/bioconda
 - file:///sw/apps/conda/latest/rackham/local_repo/free
 - file:///sw/apps/conda/latest/rackham/local_repo/pro
 - file:///sw/apps/conda/latest/rackham/local_repo/qiime2
 - file:///sw/apps/conda/latest/rackham/local_repo/biocore
 - file:///sw/apps/conda/latest/rackham/local_repo/dranew
 - file:///sw/apps/conda/latest/rackham/local_repo/r2018.11
 - file:///sw/apps/conda/latest/rackham/local_repo/nvidia
 - file:///sw/apps/conda/latest/rackham/local_repo/pytorch
 - file:///sw/apps/conda/latest/rackham/local_repo/anaconda
 - defaults
 - conda-forge
Platform: linux-64
Collecting package metadata (repodata.json): - subdir mismatch
\ subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
- subdir mismatch
\ subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
done
Solving environment: failed

PackagesNotFoundError: The following packages are not available from current channels:

  - cellranger

Current channels:

  - file:///sw/apps/conda/latest/rackham/local_repo/conda-forge
  - file:///sw/apps/conda/latest/rackham/local_repo/scilifelab-lts
  - file:///sw/apps/conda/latest/rackham/local_repo/r
  - file:///sw/apps/conda/latest/rackham/local_repo/main
  - file:///sw/apps/conda/latest/rackham/local_repo/bioconda
  - file:///sw/apps/conda/latest/rackham/local_repo/free
  - file:///sw/apps/conda/latest/rackham/local_repo/pro
  - file:///sw/apps/conda/latest/rackham/local_repo/qiime2
  - file:///sw/apps/conda/latest/rackham/local_repo/biocore
  - file:///sw/apps/conda/latest/rackham/local_repo/dranew
  - file:///sw/apps/conda/latest/rackham/local_repo/r2018.11
  - file:///sw/apps/conda/latest/rackham/local_repo/nvidia
  - file:///sw/apps/conda/latest/rackham/local_repo/pytorch
  - file:///sw/apps/conda/latest/rackham/local_repo/anaconda
  - defaults
  - https://conda.anaconda.org/conda-forge/linux-64
  - https://conda.anaconda.org/conda-forge/noarch

To search for alternate channels that may provide the conda package you're
looking for, navigate to

    https://anaconda.org

and use the search bar at the top of the page.
```

Do conda install from the doc at https://anaconda.org/hcc/cellranger:

```
conda install hcc::cellranger
```

Fails too:

```
[richel@rackham1 ~]$ conda install hcc::cellranger
Channels:
 - file:///sw/apps/conda/latest/rackham/local_repo/conda-forge
 - file:///sw/apps/conda/latest/rackham/local_repo/scilifelab-lts
 - file:///sw/apps/conda/latest/rackham/local_repo/r
 - file:///sw/apps/conda/latest/rackham/local_repo/main
 - file:///sw/apps/conda/latest/rackham/local_repo/bioconda
 - file:///sw/apps/conda/latest/rackham/local_repo/free
 - file:///sw/apps/conda/latest/rackham/local_repo/pro
 - file:///sw/apps/conda/latest/rackham/local_repo/qiime2
 - file:///sw/apps/conda/latest/rackham/local_repo/biocore
 - file:///sw/apps/conda/latest/rackham/local_repo/dranew
 - file:///sw/apps/conda/latest/rackham/local_repo/r2018.11
 - file:///sw/apps/conda/latest/rackham/local_repo/nvidia
 - file:///sw/apps/conda/latest/rackham/local_repo/pytorch
 - file:///sw/apps/conda/latest/rackham/local_repo/anaconda
 - defaults
 - hcc
 - conda-forge
Platform: linux-64
Collecting package metadata (repodata.json): / subdir mismatch
- subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
/ subdir mismatch
- subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
done
Solving environment: / warning  libmamba Added empty dependency for problem type SOLVER_RULE_UPDATE
failed

PackagesNotFoundError: The following packages are not available from current channels:

  - hcc::cellranger

Current channels:

  - file:///sw/apps/conda/latest/rackham/local_repo/conda-forge
  - file:///sw/apps/conda/latest/rackham/local_repo/scilifelab-lts
  - file:///sw/apps/conda/latest/rackham/local_repo/r
  - file:///sw/apps/conda/latest/rackham/local_repo/main
  - file:///sw/apps/conda/latest/rackham/local_repo/bioconda
  - file:///sw/apps/conda/latest/rackham/local_repo/free
  - file:///sw/apps/conda/latest/rackham/local_repo/pro
  - file:///sw/apps/conda/latest/rackham/local_repo/qiime2
  - file:///sw/apps/conda/latest/rackham/local_repo/biocore
  - file:///sw/apps/conda/latest/rackham/local_repo/dranew
  - file:///sw/apps/conda/latest/rackham/local_repo/r2018.11
  - file:///sw/apps/conda/latest/rackham/local_repo/nvidia
  - file:///sw/apps/conda/latest/rackham/local_repo/pytorch
  - file:///sw/apps/conda/latest/rackham/local_repo/anaconda
  - defaults
  - https://conda.anaconda.org/hcc
  - https://conda.anaconda.org/conda-forge/linux-64
  - https://conda.anaconda.org/conda-forge/noarch

To search for alternate channels that may provide the conda package you're
looking for, navigate to

    https://anaconda.org

and use the search bar at the top of the page.

```

Using -c:

```
[richel@rackham1 ~]$ conda install -c hcc cellranger
Channels:
 - hcc
 - file:///sw/apps/conda/latest/rackham/local_repo/conda-forge
 - file:///sw/apps/conda/latest/rackham/local_repo/scilifelab-lts
 - file:///sw/apps/conda/latest/rackham/local_repo/r
 - file:///sw/apps/conda/latest/rackham/local_repo/main
 - file:///sw/apps/conda/latest/rackham/local_repo/bioconda
 - file:///sw/apps/conda/latest/rackham/local_repo/free
 - file:///sw/apps/conda/latest/rackham/local_repo/pro
 - file:///sw/apps/conda/latest/rackham/local_repo/qiime2
 - file:///sw/apps/conda/latest/rackham/local_repo/biocore
 - file:///sw/apps/conda/latest/rackham/local_repo/dranew
 - file:///sw/apps/conda/latest/rackham/local_repo/r2018.11
 - file:///sw/apps/conda/latest/rackham/local_repo/nvidia
 - file:///sw/apps/conda/latest/rackham/local_repo/pytorch
 - file:///sw/apps/conda/latest/rackham/local_repo/anaconda
 - defaults
 - conda-forge
Platform: linux-64
Collecting package metadata (repodata.json): | subdir mismatch
/ subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
- subdir mismatch
\ subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
subdir mismatch
done
Solving environment: / warning  libmamba Added empty dependency for problem type SOLVER_RULE_UPDATE
failed

LibMambaUnsatisfiableError: Encountered problems while solving:
  - nothing provides openssl >=1.1.1,<1.1.2.0a0 needed by python-2.7.15-h9bab390_2

Could not solve for environment specs
The following packages are incompatible
├─ cellranger is installable with the potential options
│  ├─ cellranger 3.0.2 would require
│  │  └─ python >=2.7,<2.8.0a0  with the potential options
│  │     ├─ python [2.7.10|2.7.11|...|2.7.9], which can be installed;
│  │     └─ python 2.7.15 would require
│  │        └─ openssl >=1.1.1,<1.1.2.0a0 , which does not exist (perhaps a missing channel);
│  └─ cellranger 3.0.2 would require
│     └─ python <3  with the potential options
│        ├─ python [2.7.10|2.7.11|...|2.7.9], which can be installed;
│        ├─ python 2.7.15, which cannot be installed (as previously explained);
│        └─ python [1.0.1|1.2|...|2.6.9], which can be installed;
└─ pin-1 is not installable because it requires
   └─ python 3.12.* , which conflicts with any installable versions previously reported.

Pins seem to be involved in the conflict. Currently pinned specs:
 - python 3.12.* (labeled as 'pin-1')

```

Seems unsolvable on Rackham


From https://anaconda.org/hcc/repo/installers:

> To install a conda package from this channel, run:

```
conda install --channel "HCC" package
```

Takes us back to the earlier tried:

```
./conda install --channel "HCC" cellranger
```

with error:

```
richel@richel-N141CU:~/anaconda3/bin$ ./conda install --channel "HCC" cellranger
Channels:
 - HCC
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: failed

LibMambaUnsatisfiableError: Encountered problems while solving:
  - nothing provides bcftools 1.9.* needed by cellranger-3.0.2-py27_1

Could not solve for environment specs
The following package could not be installed
└─ cellranger is not installable because it requires
   └─ bcftools 1.9.* , which does not exist (perhaps a missing channel).

```




## [ABANDON] Approach 2: Use conda from local install

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


## Thanks for the help 10x!

From <https://github.com/10XGenomics/cellranger/tree/main>:

> Please note that this source code is made available only for informational
> purposes. 10x does not provide support for interpreting,
> modifying, building, or running this code.

Thanks 10x!