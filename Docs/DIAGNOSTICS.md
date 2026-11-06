# Local diagnostics

Diagnostics stay on your computer. Nothing in this feature uploads them.
Before sharing any report or log, review it yourself. Existing engine and
launcher logs can contain local paths, usernames, command-line arguments and
game-specific information. Do not share your game files or saves.

## Crash reports

The game writes `crash-report.json` under the common launcher user directory,
not in the game data folder or next to the executable:

- Windows: `%LOCALAPPDATA%\Harry Potter 2\User\crash-report.json`
- macOS: `~/Library/Application Support/Harry Potter 2/User/crash-report.json`
- Linux: `${XDG_DATA_HOME:-~/.local/share}/harry-potter-2/User/crash-report.json`

The reporter prints the attempted path to standard error. If the directory
cannot be prepared, that fallback path may instead be relative to the working
directory. Reports are overwritten by a later crash. Test harnesses can set
`HP2_ARTIFACT_DIR` to an existing directory to override the location.

On Windows the report records the exception code, address, module basename
and module-relative offset. It is not a minidump or a complete stack trace,
and reporting is best-effort after a crash. The POSIX reporter's existing
optional engine-log tail is **off** by default; set
`HP2_CRASH_INCLUDE_LOG_TAIL=1` before launch only if you accept that it may
contain private paths or other sensitive log content.

## Input capture troubleshooting

Set `HP2_INPUT_DIAGNOSTICS=1` in the environment before launching the game.
The engine log then records capture requests, focus/window transitions and
SDL relative-mode results. The new records contain window IDs and state flags,
not key presses, mouse movement, save contents, or paths. Diagnostic logging
is off when the variable is absent or is anything other than `1`.

The engine log also records the configured build version, Git revision as
known at CMake configure time (with `-dirty` for tracked changes), platform,
and launcher data-source selection. This selection is not proof that the
imported data was validated. The renderer already reports its OpenGL details
in the engine log. Existing logs may still contain personal information even
when input diagnostics are disabled.
