# Rorix Registry GA fixture

This package exists only to exercise Rorix's source-built NuGet admission and
dependency recovery flow. It has no network, file-system, process, or startup
behavior. `GaFixture.Check()` returns `forty-two` through Humanizer.Core 3.0.10.

The package is not a supported Rorix product. Its pinned source and public
NuGet artifact are used as an upstream baseline so a Test Org can prove an
all-cold root and dependency scan, hold, natural recovery, and isolated restore.
