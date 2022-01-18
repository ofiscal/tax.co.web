Scripts in `common` can be used both when serving offline and online
(on the internet).
If things go normally, the only ones that should need explicit calling are
`*/create.sh` and `common/clean.sh`;
the others are called by those.

The commands in `by-hand.sh` is a collection of bash snippets --
for Docker and the host system, and for offline and online usage.
That's why it's not executable; it would make no sense to run them in series.
