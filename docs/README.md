# Building the documentation

To generate the documentation, make sure you've installed the Sphinx library and it is accessible in the PATH environment variable.

In the command prompt, run `make.bat html`from the docs directory.

This will generate the documentation files in the "build" subfolder under "docs".

`release_docs.bat` is a convenience script used to copy a subset of the generated files into the "release" folder as the public-facing documentation. This might not be needed if the documentation is hosted online.
