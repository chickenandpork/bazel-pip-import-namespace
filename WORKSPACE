load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

#
# Let's do some Python3
#
# Not currently using bazelbuild/bazel-federation: bazel-3.0.0 is released
# after bazel-federation-0.0.1 so using bazel-federation puts us back a major
# rev. Using git_repository to bring in a versioned should-have-been-released
# pip_import(python_interpreter= ..) named parameter

git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "94677401bc56ed5d756f50b441a6a5c7f735a6d4",
    shallow_since = "1573842889 -0500",
)
load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

# Only needed if using the packaging rules.
load("@rules_python//python:pip.bzl", "pip_repositories")
pip_repositories()


# pip_install() to create @amc_pip
# Note that //:requirements.txt should be pip-compile'd to declare all dependencies
#
# This pip_import has Secret Cow Powers that makes us rpefer this specific repos, but we're not
# using them in this example.

http_archive(
    name = "com_github_ali5h_rules_pip",
    strip_prefix = "rules_pip-2.1.1",
    sha256 = "f4644c7fc13c70e8de005f8cac63c9b209203ebb8cc7ca6cb55c3a42b558e2a6",
    urls = [ "https://github.com/ali5h/rules_pip/archive/2.1.1.tar.gz" ]
)

# pip-based dependencies
load("@com_github_ali5h_rules_pip//:defs.bzl", "pip_import")
pip_import(
    name = "amc_pip",
    python_interpreter = "python3",
    requirements = "//:requirements.txt",
)

load("@amc_pip//:requirements.bzl", "pip_install")
pip_install()

# vim: ts=8 et sw=4 sts=4 :

