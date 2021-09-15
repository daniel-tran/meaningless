:: Generates a set of release documentation from the Sphinx output
:: This script might be removed if this documentation is hosted online

@echo off
pushd %~dp0

set builddir=.\build\html\
set releasedir=..\docs\

if not exist %releasedir% (
    mkdir %releasedir%
)

if exist %builddir% (
    robocopy %builddir% %releasedir% *.html /E
    robocopy %builddir% %releasedir% *.js /E
    robocopy %builddir% %releasedir% *.css /E
    robocopy %builddir% %releasedir% *.png /E
)

popd
@echo on
