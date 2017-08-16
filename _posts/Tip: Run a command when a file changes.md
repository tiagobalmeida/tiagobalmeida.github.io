# Tip: Run a command when a file changes

## The problem

Say you'd like to run a command when a file changes, automatically. 

For example, I'm using this to call the LessCSS compiler when I save the .less file.

i.e. in this example, I'd like to run the following command everytime the style.less file is changed:

```bash
lessc src/css/style.less > src/css/style.css
```

## Solution

Install the inotify-tools package
```bash
sudo apt install inotify-tools
```

To set up a command to run automatically, we can do this:

```bash
while inotifywait -e close_write src/css/style.less; do lessc src/css/style.less > src/css/style.css; done
```

More generally, the syntax is the following:

```bash
while inotifywait -e close_write /my/file; do mycommand; done
```

Awesome!
