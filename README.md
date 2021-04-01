readable
========
[![pipeline status][pipeline]][homepage]
[![coverage report][coverage]][homepage]

Check and improve the spelling and grammar of documents.

Installation
------------
```shell
# Using a modern dependency manager:
$ make install

# ... or using a legacy pip:
$ make pip-install-development
```

Development
-----------
```shell
# Create a virtual machine:
docker-machine create \
    --driver virtualbox \
    --virtualbox-cpu-count 2 \
    --virtualbox-disk-size 20480 \
    --virtualbox-memory 2048 \
    readable

# Build or rebuild the services:
docker-compose build \
    --force-rm \
    --no-cache \
    --pull \
    --quiet

# Start or restart the services:
docker-compose up \
    --detach \
    --force-recreate \
    --no-build \
    --remove-orphans
```

Vendored dependencies
---------------------
- [jQuery][jquery_homepage] `v3.6.0`
- [Bootstrap][bootstrap_homepage] `v4.6.0` ([custom theme][minimal_homepage])
- [Font Awesome][fontawesome_homepage] `v5.15.3`

Distribution
------------
This project is licensed under the terms of the [MIT License](LICENSE).

Links
-----
- Website: <https://readable.pw>
- Coverage report: <https://coverage.readable.pw>
- Code: <https://gitlab.com/amalchuk/readable>
- GitHub mirror: <https://github.com/amalchuk/readable>

[homepage]: <https://gitlab.com/amalchuk/readable>
[pipeline]: <https://gitlab.com/amalchuk/readable/badges/master/pipeline.svg?style=flat-square>
[coverage]: <https://gitlab.com/amalchuk/readable/badges/master/coverage.svg?style=flat-square>

[jquery_homepage]: <https://jquery.com>
[bootstrap_homepage]: <https://getbootstrap.com>
[minimal_homepage]: <https://gitlab.com/amalchuk/minimal>
[fontawesome_homepage]: <https://fontawesome.com>
