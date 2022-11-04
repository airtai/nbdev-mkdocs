# `nbdev_mkdocs`

**Usage**:

```console
$ nbdev_mkdocs [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `new`: Creates files in **mkdocs** subdirectory...
* `prepare`: Prepares files in **mkdocs/docs** and then...
* `preview`: Prepares files in **mkdocs/docs** and then...

## `nbdev_mkdocs new`

Creates files in **mkdocs** subdirectory needed for other **nbdev_mkdocs** subcommands

**Usage**:

```console
$ nbdev_mkdocs new [OPTIONS]
```

**Options**:

* `--root-path TEXT`: [default: .]
* `--help`: Show this message and exit.

## `nbdev_mkdocs prepare`

Prepares files in **mkdocs/docs** and then runs **mkdocs build** command on them 

**Usage**:

```console
$ nbdev_mkdocs prepare [OPTIONS]
```

**Options**:

* `--root-path TEXT`: [default: .]
* `--help`: Show this message and exit.

## `nbdev_mkdocs preview`

Prepares files in **mkdocs/docs** and then runs **mkdocs serve** command on them 

**Usage**:

```console
$ nbdev_mkdocs preview [OPTIONS]
```

**Options**:

* `--root-path TEXT`: [default: .]
* `--help`: Show this message and exit.

