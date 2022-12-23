# No command line executables found in console_scripts in settings.ini file.

To document CLI commands, please ensure that the entry points registered in `console_scripts` in the `settings.ini` file are valid or add new entry points.

If you do not want this page to be rendered as part of the documentation, please remove the following lines from the **mkdocs/summary_template.txt** file and build the docs again.

```
- CLI
{cli}
```

