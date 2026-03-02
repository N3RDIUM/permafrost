# permafrost
A custom obsidian.md static site generator tailored for https://n3rdium.dev

## how it works
1. clones all repositories mentioned in permafrost.json (yes, you can build many
vaults at once!) (if the repos exist, it will run `git pull` instead).
2. extracts all metadata from the markdown files.
3. copies all html files directly to the build
4. builds html from markdown, applies the configured template
5. automatically adjusts wikilinks so that they don't break

