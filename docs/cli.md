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
* `data`: Work with the experiment data.

## `exp-coord s3i`

Play around with S3I. This wont invoke any reactions afterwards, as when using the run commands.

**Usage**:

```console
$ exp-coord s3i [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get-token`
* `message`
* `event`

### `exp-coord s3i get-token`

**Usage**:

```console
$ exp-coord s3i get-token [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord s3i message`

**Usage**:

```console
$ exp-coord s3i message [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Get a message from the message queue.
* `send`: Send a message to the message queue.

#### `exp-coord s3i message get`

Get a message from the message queue.

**Usage**:

```console
$ exp-coord s3i message get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `exp-coord s3i message send`

Send a message to the message queue.

**Usage**:

```console
$ exp-coord s3i message send [OPTIONS] ENDPOINT CONTENT
```

**Arguments**:

* `ENDPOINT`: [required]
* `CONTENT`: [required]

**Options**:

* `--help`: Show this message and exit.

### `exp-coord s3i event`

**Usage**:

```console
$ exp-coord s3i event [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Get an event from the event queue.
* `send`: Send an event to the event queue.
* `add-topic`: Subscribe to a topic.

#### `exp-coord s3i event get`

Get an event from the event queue.

**Usage**:

```console
$ exp-coord s3i event get [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `exp-coord s3i event send`

Send an event to the event queue.

**Usage**:

```console
$ exp-coord s3i event send [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: [required]

**Options**:

* `--help`: Show this message and exit.

#### `exp-coord s3i event add-topic`

Subscribe to a topic.

**Usage**:

```console
$ exp-coord s3i event add-topic [OPTIONS] TOPIC
```

**Arguments**:

* `TOPIC`: [required]

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
* `all`: Run the specified pipeline until all...
* `single`: Run the message processing pipeline a...
* `forever`: Start the experiment coordinator and run...

### `exp-coord run test`

Run a test to check if setup and teardown works correctly.

**Usage**:

```console
$ exp-coord run test [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord run all`

Run the specified pipeline until all messages have been processed.

**Usage**:

```console
$ exp-coord run all [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `message`: Process all messages from the queue.
* `event`: Process all events from the queue.

#### `exp-coord run all message`

Process all messages from the queue.

**Usage**:

```console
$ exp-coord run all message [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `exp-coord run all event`

Process all events from the queue.

**Usage**:

```console
$ exp-coord run all event [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord run single`

Run the message processing pipeline a single time.

**Usage**:

```console
$ exp-coord run single [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `message`: Process a single message from the queue.
* `event`: Process a single event from the queue.

#### `exp-coord run single message`

Process a single message from the queue.

**Usage**:

```console
$ exp-coord run single message [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `exp-coord run single event`

Process a single event from the queue.

**Usage**:

```console
$ exp-coord run single event [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `exp-coord run forever`

Start the experiment coordinator and run it forever, or until the messages run out.

**Usage**:

```console
$ exp-coord run forever [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--interval INTEGER`: [default: 60]
* `--exit-on-failure / --no-exit-on-failure`: [default: exit-on-failure]
* `--help`: Show this message and exit.

## `exp-coord data`

Work with the experiment data.

**Usage**:

```console
$ exp-coord data [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `images`

### `exp-coord data images`

**Usage**:

```console
$ exp-coord data images [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `load-all`

#### `exp-coord data images load-all`

**Usage**:

```console
$ exp-coord data images load-all [OPTIONS] OUTPUT_DIR
```

**Arguments**:

* `OUTPUT_DIR`: [required]

**Options**:

* `--help`: Show this message and exit.
