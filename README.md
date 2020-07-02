# bazel pip_import Namespace Example

If you don't have `google-cloud-bigquery` nor `google-cloud-datastore` installed in your user or system -level libs, then this code will fail on a basic `bazel test //...`:

(repro for issue https://github.com/ali5h/rules_pip/issues/35)

```
macosx-10-15-5:bazel-pip-import-namespace allanc$ bazel clean && bazel test //...
INFO: Starting clean.
INFO: Analyzed target //:test_ns (41 packages loaded, 1777 targets configured).
INFO: Found 1 test target...
FAIL: //:test_ns (see /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__/bazel-out/darwin-fastbuild/testlogs/test_ns/test.log)
Target //:test_ns up-to-date:
  bazel-bin/test_ns
INFO: Elapsed time: 1.728s, Critical Path: 1.23s
INFO: 2 processes: 2 darwin-sandbox.
INFO: Build completed, 1 test FAILED, 6 total actions
//:test_ns                                                               FAILED in 0.7s
  /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__/bazel-out/darwin-fastbuild/testlogs/test_ns/test.log

INFO: Build completed, 1 test FAILED, 6 total actions
macosx-10-15-5:bazel-pip-import-namespace allanc$ cat /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__/bazel-out/darwin-fastbuild/testlogs/test_ns/test.log
exec ${PAGER:-/usr/bin/less} "$0" || exit 1
Executing tests from //:test_ns
-----------------------------------------------------------------------------
Traceback (most recent call last):
  File "/private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/sandbox/darwin-sandbox/5/execroot/__main__/bazel-out/darwin-fastbuild/bin/test_ns.runfiles/__main__/test_ns.py", line 3, in <module>
    from google.cloud import datastore
ImportError: cannot import name 'datastore' from 'google.cloud' (unknown location)
macosx-10-15-5:bazel-pip-import-namespace allanc$ 
```

Note that `google.cloud.datastore` is provided by `google-cloud-datastore-1.25.0`
`google.cloud.datastore` is provided by `@ali5h_pip`
`@ali5h_pip` compiles its deliverable from `requirements.txt`
`requirements.txt` is `pip-compile`'d from `requirements.in`
`@ali5h_pip:google-cloud-datastore` is provided to the test build by dependency in BUILD: `requirement("google-cloud-datastore"),

It's suggested that the directory for `google.cloud.bigquery` is eclipsing the directory for `google.cloud.datastore`

## Still Broken on MacOS-10.15.5

ali5h tested in:
(export PYTHONPATH="" ; export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/allanc/bin ;  bash -x bazel-out/darwin-fastbuild/bin/test_ns.runfiles/bazel_tools/tools/python/py3wrapper.sh) * "mac, python 3.8"
 * "also tested on linux" (unsure what version)


### Working Docker Container

In helping me debug, `ali5h` asked about a docker container to repro -- this was like the ultimately-controlled buildenv.

This container works:
```
docker run --rm -it  \
    -w /code -v $(pwd):/code \
    -e LC_ALL=C.UTF-8 -e LANG=C.UTF-8 \
    l.gcr.io/google/bazel:3.3.0 \
test //...
```

### bazel test -s //...

In my non-docker environment (macOS-10.15.5, Python-3.7.3 from XCode) I was still getting failures, and `bazel test -s //...` gave no immediate help, but helped identify the wrapper:

 * Look for `TEST_SRCDIR`, which is `PYTHON_RUNFILES` as well

```
bazel-pip-import-namespace allanc$ test -s  //...
INFO: Analyzed target //:test_ns (0 packages loaded, 0 targets configured).
INFO: Found 1 test target...
SUBCOMMAND: # //:test_ns [action 'Testing //:test_ns', configuration: 12c9f5b38ca9023465976bb4b98a011d02814ec73529bdcfee2e76a895d9598f]
(cd /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__ && \
  exec env - \
    EXPERIMENTAL_SPLIT_XML_GENERATION=1 \
    JAVA_RUNFILES=bazel-out/darwin-fastbuild/bin/test_ns.runfiles \
    PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/allanc/bin:/usr/local/snap/Python.framework/Versions/3.8/bin \
    PYTHON_RUNFILES=bazel-out/darwin-fastbuild/bin/test_ns.runfiles \
    RUNFILES_DIR=bazel-out/darwin-fastbuild/bin/test_ns.runfiles \
    RUN_UNDER_RUNFILES=1 \
    TEST_BINARY=./test_ns \
    TEST_INFRASTRUCTURE_FAILURE_FILE=bazel-out/darwin-fastbuild/testlogs/test_ns/test.infrastructure_failure \
    TEST_LOGSPLITTER_OUTPUT_FILE=bazel-out/darwin-fastbuild/testlogs/test_ns/test.raw_splitlogs/test.splitlogs \
    TEST_PREMATURE_EXIT_FILE=bazel-out/darwin-fastbuild/testlogs/test_ns/test.exited_prematurely \
    TEST_SIZE=medium \
    TEST_SRCDIR=bazel-out/darwin-fastbuild/bin/test_ns.runfiles \
    TEST_TARGET=//:test_ns \
    TEST_TIMEOUT=300 \
    TEST_TMPDIR=_tmp/ab2e2aa63a202e32a87097fdb942a1ac \
    TEST_UNDECLARED_OUTPUTS_ANNOTATIONS=bazel-out/darwin-fastbuild/testlogs/test_ns/test.outputs_manifest/ANNOTATIONS \
    TEST_UNDECLARED_OUTPUTS_ANNOTATIONS_DIR=bazel-out/darwin-fastbuild/testlogs/test_ns/test.outputs_manifest \
    TEST_UNDECLARED_OUTPUTS_DIR=bazel-out/darwin-fastbuild/testlogs/test_ns/test.outputs \
    TEST_UNDECLARED_OUTPUTS_MANIFEST=bazel-out/darwin-fastbuild/testlogs/test_ns/test.outputs_manifest/MANIFEST \
    TEST_UNDECLARED_OUTPUTS_ZIP=bazel-out/darwin-fastbuild/testlogs/test_ns/test.outputs/outputs.zip \
    TEST_UNUSED_RUNFILES_LOG_FILE=bazel-out/darwin-fastbuild/testlogs/test_ns/test.unused_runfiles_log \
    TEST_WARNINGS_OUTPUT_FILE=bazel-out/darwin-fastbuild/testlogs/test_ns/test.warnings \
    TEST_WORKSPACE=__main__ \
    TZ=UTC \
    XML_OUTPUT_FILE=bazel-out/darwin-fastbuild/testlogs/test_ns/test.xml \
  external/bazel_tools/tools/test/test-setup.sh ./test_ns)
SUBCOMMAND: # //:test_ns [action 'Testing //:test_ns', configuration: 12c9f5b38ca9023465976bb4b98a011d02814ec73529bdcfee2e76a895d9598f]
(cd /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__ && \
  exec env - \
    PATH=/usr/bin:/bin \
    TEST_BINARY=./test_ns \
    TEST_NAME=//:test_ns \
    TEST_SHARD_INDEX=0 \
    TEST_TOTAL_SHARDS=0 \
  external/bazel_tools/tools/test/generate-xml.sh bazel-out/darwin-fastbuild/testlogs/test_ns/test.log bazel-out/darwin-fastbuild/testlogs/test_ns/test.xml 0 1)
FAIL: //:test_ns (see /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__/bazel-out/darwin-fastbuild/testlogs/test_ns/test.log)
Target //:test_ns up-to-date:
  bazel-bin/test_ns
INFO: Elapsed time: 0.700s, Critical Path: 0.60s
INFO: 2 processes: 2 darwin-sandbox.
INFO: Build completed, 1 test FAILED, 2 total actions
//:test_ns                                                               FAILED in 0.2s
  /private/var/tmp/_bazel_allanc/a49d8885b6fea93ab0d1c9501f98ba01/execroot/__main__/bazel-out/darwin-fastbuild/testlogs/test_ns/test.log

INFO: Build completed, 1 test FAILED, 2 total actions
```

 * OK, `TEST_SRCDIR=bazel-out/darwin-fastbuild/bin/test_ns.runfiles`
 * relative to build directory

...so I tried:
```
(export PYTHONPATH="" ; \
    export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/allanc/bin ;  
    bash -x bazel-out/darwin-fastbuild/bin/test_ns.runfiles/bazel_tools/tools/python/py3wrapper.sh)
```

This gave an interactive shell (and with a bit of help from`@yarbelk on stackoverflow` (https://stackoverflow.com/a/14050282/1712731) I got a clue:

```
>>> import importlib
>>> print(importlib.util.find_spec("google.cloud.datastore"))
None
>>> print(importlib.util.find_spec("google.cloud")
ModuleSpec(name='google.cloud', loader=<_frozen_importlib_external._NamespaceLoader object at 0x10ee5f710>, submodule_search_locations=_NamespacePath(['/Users/allanc/Library/Python/3.7/lib/python/site-packages/google/cloud']))
```

The error seems to be a mix of two things:
1. Non-hermetic: the local environment is tainting the build, and needs to be removes or sanitized
1. The namespace issue in python: the first matching namespace ('google') was changed, and on failure, did not check any other
1. BONUS: the things we needed in the `bazl` build were not installed on the hsot system, and should not be.

## Recommendation

Eliminate the namespace in local system dependencies.  At most naive, this is a simple deletion of the `google` namespace:

```
python3 -m pip uninstall google-<whatever is there>
```
If that doesn't remove the `python/site-packages/google` directory, go harder:
```
rm -fr /Users/allanc/Library/Python/3.7/lib/python/site-packages/google
```

Note that this can affect the use of `google.*` python libs later, so this may not be ideal, but it can be mitigated by -- for example -- using only Python-3.8 for bazel builds, and using Python-3.7 for local hacking; or, fiddling with the PATH so that when building with `bazel`, the `/usr/bin/python3` resolves to a really sparse `site-packages` path.  It's the `python3` binary in the path, not the `PYTHONPATH`, but you can set a specific absolute path in your `WORKSPACE` file:

```
ali5h_import(
    ...
    python_interpreter = "/usr/local/hermetic/super-clean/python3",
    ...
)
```

Lastly, the option that is most predictable yet can take a while to build (ensure you have a local build-cache server):  There's an example of building a new, clean python3 as part of the build process.  This is the slowest, yet most reliable result.

TODO: track it down and ptovide a reference

### Fixed

post-deletion (note that the command deleted from my personal python site-packages, not system), I have:

```
>>> import importlib
>>> print(importlib.util.find_spec("google.cloud.datastore"))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.7/lib/python3.7/importlib/util.py", line 94, in find_spec
    parent = __import__(parent_name, fromlist=['__path__'])
ModuleNotFoundError: No module named 'google'
```

