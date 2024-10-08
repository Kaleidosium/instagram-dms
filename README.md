# instagram_dms

Distraction-free way to view Instagram DMs on Desktop. Requires webview.

## Background

I get a lot of Instagram DMs, so I ended up checking it often, but this leads to me getting easily distracted by non-DM related things. So, I made this to control my Instagram usage.

This was primarily written for Windows, though I don't see why it shouldn't work on other Operating Systems, as long as you have webview.

## Usage

### Requirements

- Make sure you have [Rye](https://rye.astral.sh/) installed on your computer.

### Installation Steps

1. Get the code by either:

   ```bash
   git clone https://github.com/Kaleidosium/instagram_dms.git
   ```

   OR
   - Download and unzip from GitHub repository

2. Open a terminal/command prompt in the project folder and run:

   ```bash
   rye sync
   ```

3. Start the program with:

   ```bash
   rye run python src/instagram_dms.py
   ```

### Creating a Standalone Executable (Optional)

To create an executable file you can double-click to run:

```bash
# Windows, you might have to adjust for macOS/Linux
pyinstaller --onefile --windowed --icon=res/favicon.ico src/instagram_dms.py
```

The executable will be created in the `dist` folder.

That's it! The program should open in a window showing just your Instagram DMs (After you logged in, of course).

## License

MIT
