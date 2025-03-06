# CLI Documentation

Your friendly CLI interface for the experiment coordinator.

**Usage**:

```console
$ exp-coord [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `s3i`: Play around with S3I.
* `run`: Run the experiment coordinator, either...

## `exp-coord s3i`

Play around with S3I. This wont invoke any reactions afterwards, as when using the run commands.

**Usage**:

```console
$ exp-coord s3i [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-message`: Get a message from the message queue.
* `get-event`: Get an event from the event queue.
* `send-message`: Send a message to the message queue.
* `send-event`: Send an event to the event queue.

### `exp-coord s3i get-message`

Get a message from the message queue.

**Usage**:

```console
$ exp-coord s3i get-message [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord s3i get-event`

Get an event from the event queue.

**Usage**:

```console
$ exp-coord s3i get-event [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord s3i send-message`

Send a message to the message queue.

**Usage**:

```console
$ exp-coord s3i send-message [OPTIONS] ENDPOINT CONTENT
```

**Arguments**:

* `ENDPOINT`: [required]
* `CONTENT`: [required]

**Options**:

* `--help`: Show this message and exit.

### `exp-coord s3i send-event`

Send an event to the event queue.

**Usage**:

```console
$ exp-coord s3i send-event [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: [required]

**Options**:

* `--help`: Show this message and exit.

## `exp-coord run`

Run the experiment coordinator, either just once or as a server.

**Usage**:

```console
$ exp-coord run [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `test`: Run a test to check if setup and teardown...
* `single`: Process just one message or event from the...
* `forever`: Start the experiment coordinator and run...

### `exp-coord run test`

Run a test to check if setup and teardown works correctly.

**Usage**:

```console
$ exp-coord run test [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord run single`

Process just one message or event from the queue.

**Usage**:

```console
$ exp-coord run single [OPTIONS]
```

**Options**:

* `--only-message / --no-only-message`: [default: no-only-message]
* `--only-event / --no-only-event`: [default: no-only-event]
* `--help`: Show this message and exit.

### `exp-coord run forever`

Start the experiment coordinator and run it forever, or until the messages ran out.

**Usage**:

```console
$ exp-coord run forever [OPTIONS]
```

**Options**:

* `--stop-when-empty / --no-stop-when-empty`: Should the experiment coordinator stop when it doesn&#x27;t receive any messages anymore?  [default: stop-when-empty]
* `--help`: Show this message and exit.
