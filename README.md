# laoshi (老師)

CLI application for learning Chinese. I wanted to have an interactive
experience while I use the terminal, so I made this app.

## Installation

```commandline
pip install laoshi
```

If you want to manage your AnkiDecks with laoshi, you'll need:
- [Anki](https://apps.ankiweb.net/)
- [AnkiConnect](https://git.foosoft.net/alex/anki-connect)

This allows us to make HTTP calls to your Anki application, you're
going to need to have Anki open.

## Usage

```commandline
  cli application to learn chinese.

Options:
  --help  Show this message and exit.

Commands:
  cc           Convert characters
  manage-deck  Manage deck group
  translate    Translate a phrase 
```

You're able to convert characters, manage an Anki deck or translate a phrase.

```commandline
Usage: laoshi cc [OPTIONS] WORD

  Convert characters

Options:
  -t, --to [traditional|simplified|pinyin]

```

The manage-deck subcommand allows you to create a deck from one seed word or phrase using `create-deck`,
you can also add notes with `add-note`:

```commandline
Usage: laoshi manage-deck [OPTIONS] COMMAND [ARGS]...

  Manage deck group

Options:
  --help  Show this message and exit.

Commands:
  add-note     add note function for click
  create-deck  Create a deck function for click
```

Lastly you can translate phrases or words with `translate`, by default we use english, but you can change that:

```
Usage: laoshi translate [OPTIONS] PHRASE

  Translate a phrase

Options:
  -t, --to TEXT
  --help         Show this message and exit.
```

Examples:
```commandline
➜  ~ laoshi translate 服饰  
apparel
```

```commandline
➜  ~ laoshi cc -t pinyin 服饰
fúshì
```

```commandline
➜  ~ python -m laoshi.main manage-deck add-note -c simplified hsk5+ 涉及 # You have to create the AnkiDeck first.
```