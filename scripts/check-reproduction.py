"""Check the exact content Rorix uses for NuGet source reproduction."""

import hashlib
import sys
import xml.etree.ElementTree as ET
import zipfile


def significant_entries(path):
    with zipfile.ZipFile(path) as archive:
        entries = {}
        for name in archive.namelist():
            normalized = name.replace("\\", "/").lower()
            if (
                normalized in {".signature.p7s", "[content_types].xml", "_rels/.rels"}
                or normalized.startswith("package/services/metadata/core-properties/")
            ):
                continue
            entries[normalized] = hashlib.sha256(archive.read(name)).hexdigest()
        nuspec_name = next(name for name in archive.namelist() if name.endswith(".nuspec"))
        nuspec = ET.fromstring(archive.read(nuspec_name))
        namespace = {"n": "http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd"}
        repository = nuspec.find("n:metadata/n:repository", namespace)
        dependencies = nuspec.findall("n:metadata/n:dependencies/n:group/n:dependency", namespace)
        return entries, repository.attrib if repository is not None else {}, [item.attrib for item in dependencies]


def main():
    first, second, expected_commit = sys.argv[1:]
    first_entries, first_repository, first_deps = significant_entries(first)
    second_entries, second_repository, second_deps = significant_entries(second)
    expected_repository = "https://github.com/Authaz/rorix-registry-ga-fixture"
    expected_deps = [{"id": "Humanizer.Core", "version": "[3.0.10]", "exclude": "Build,Analyzers"}]
    for repository, dependencies in [(first_repository, first_deps), (second_repository, second_deps)]:
        assert repository.get("url") == expected_repository, repository
        assert repository.get("commit") == expected_commit, repository
        assert dependencies == expected_deps, dependencies
    assert first_entries == second_entries, {
        key: (first_entries.get(key), second_entries.get(key))
        for key in sorted(first_entries.keys() | second_entries.keys())
        if first_entries.get(key) != second_entries.get(key)
    }
    print("Source commit, dependency, DLL, and normalized package entries match.")


if __name__ == "__main__":
    main()
