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
`google.cloud.datastore` is provided by `@amc_pip`
`@amc_pip` compiles its deliverable from `requirements.txt`
`requirements.txt` is `pip-compile`'d from `requirements.in`
`@amc_pip:google-cloud-datastore` is provided to the test build by dependency in BUILD: `requirement("google-cloud-datastore"),

It's suggested that the directory for `google.cloud.bigquery` is eclipsing the directory for `google.cloud.datastore`
