# Overall aim of this library

I suppose one of the overall goals of Meaningless is **to provide an easy-to-use interface that developers can use to programatically interact with Bible passages**.

Having said that, I do acknowledge the existence of other Python libraries built to retrieve Bible passages, so you may want to investigate the following alternatives (as well as any that aren't listed) if they better suit your use case:

1. https://pypi.org/project/api-bible-sdk/
    - A Python interface based around an existing Bible API. Using this library requires an API key after creating an account and has a daily hard limit per account (see https://docs.api.bible/getting-started/rate-limiting/), but likely provides specific translation and language support that you might not otherwise find on Bible Gateway.
2. https://github.com/covode/bible-fetch
    - A standalone Python script that returns a requested passage from the Bible Gateway site. Useful if you are piping Bible passages to other command line tools.
3. https://pypi.org/project/biblehub/
    - A library that obtains Bible passages from https://biblehub.com/. Note that the developer acknowledges in the `README.md` that they are unlikely to continue supporting this project.
4. https://pypi.org/project/guibible/
    - A library that obtains Bible passages using a GUI client. It retrieves Bible passages from https://labs.bible.org, which means only the NET translation is supported.
5. https://github.com/scrollmapper/bible_databases
    - A collection of public domain Bibles in different storage formats. It can be useful if you need to load the entire Bible at once.
6. https://github.com/aaronjohnsabu1999/mBAB
    - An end-to-end project for obtaining Bible passages as a web application with its own dedicated backend database that stores Bible passages.

# Preservation of Biblical contents

To stay true to the Bible as much as possible, this library aims to provide ways to extract only the core text of passages. In that regard, items such as inline translation notes and footnote markers are considered removable.

# Meaningless ≠ Bible Gateway API

This library is **NOT** intended to be a full (unofficial) API for the Bible Gateway site. This is partly so that this library isn't directly constrained by limitations in the existing Bible Gateway search functionality, as well as not having to worry about supporting every single feature in the search functionality.
