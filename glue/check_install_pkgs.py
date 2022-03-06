from google.cloud import storage
import pkg_resources
installed_packages = pkg_resources.working_set
for package in installed_packages:
    print(package)
