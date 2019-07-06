# Release Instructions

This document contains all the necessary instructions to release the
project and to generate the corresponding changelog.

## Versioning

We follow the [PEP0440](https://www.python.org/dev/peps/pep-0440/)
versioning standard when releasing `cssi` library. Please read the
[versioning](./VERSIONING.md) guidelines document carefully before
attempting any release related tasks.

## Creating a Release

### Install Changelog Generator

We have used the `git-changelog` package to automate the changelog
generation process. Click
[here](https://pypi.org/project/git-changelog/) to learn more about
`git-changelog`. Execute the below command to install the package on
your machine.

```bash
pip install git-changelog
```

### Using the release script

We have created a script to automate the taging and versioning of the
releae pipeline. Follow the bellow guidelines when using the release
script.

NOTE: Execute the release script from the root directory.

```bash
sh ./scripts/release.sh $release_type $release_level
```

Replace the `$release_type` and `$release_level` with the corresponding
values.

#### Examples

1.  Major release - From 1.9 to 2.0

<!-- end list -->

```bash
sh ./scripts/release.sh major final
```

2.  Minor release - From 1.1.x to 1.2

<!-- end list -->

```bash
sh ./scripts/release.sh minor final
```

3.  Patch release - From 1.1.3 to 1.1.4

<!-- end list -->

```bash
sh ./scripts/release.sh patch final
```

4.  Major Alpha release - From 1.9.2 to 1.0a0

<!-- end list -->

```bash
sh ./scripts/release.sh major alpha
```

6.  Release next beta - From 0.1b2 to 0.1b3

<!-- end list -->

```bash
sh ./scripts/release.sh prenext beta
```
