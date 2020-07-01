# load("@rules_python//python:defs.bzl", "py_binary")
load("@amc_pip//:requirements.bzl", "requirement")

py_test(
  name = "test_ns",
  srcs = [
    "test_ns.py",
  ],
  #legacy_create_init=False,  # don't create __init__.py directories which break google.*
  deps = [
    requirement("google-cloud-datastore"),
    requirement("google-cloud-bigquery"),

    #requirement("cachetools"),                # required for google-auth
    #requirement("certifi"),                   # required for requests
    #requirement("chardet"),                   # required for requests
    #requirement("google-api-core[grpc]"),     # required for google-cloud-core
    #requirement("google-auth"),               # required for google-api-core
    #requirement("google-cloud-core"),         # required for google-cloud-bigquery, google-cloud-datastore
    #requirement("google-resumable-media"),    # required for google-cloud-bigquery
    #requirement("googleapis-common-protos"),  # required for google-api-core
    #requirement("grpcio"),                    # required for google-api-core
    #requirement("idna"),                      # required for requests
    #requirement("protobuf"),                  # required for googleapis-common-protos
    #requirement("pyasn1-modules"),            # required for google-auth
    #requirement("pyasn1"),                    # required for pyasn1-modules, rsa
    #requirement("pytz"),                      # required for google-api-core
    #requirement("requests"),                  # required for google-api-core
    #requirement("rsa"),                       # required for google-auth
    #requirement("six"),               # required for google-auth, google-resumable-media, grpcio, protobuf
    #requirement("urllib3"),                   # required for requests

  ],
)

