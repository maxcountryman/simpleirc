# simpleirc

[![build status](https://secure.travis-ci.org/maxcountryman/simpleirc.png?branch=master)](https://travis-ci.org/#!/maxcountryman/simpleirc)

An IRC connection layer written in Python.

## Why

Decoupling the IRC connection layer from wahtever application might be using it
frees up that application to behave however it might like. For instance, an
application that consumes simpleirc as a layer might be stopped, reloaded, and
then started again without disrupting the underlying connection. This also
means that multiple applications can consume the same connection simultaneously
without any extra work. Finally, simpleirc presents a simple socket protocol so
that applications which use it can be written in any language that can
manipulate a TCP socket.

## Installation

```sh
$ pip install simpleirc
```

## Usage

Simpleirc may be invoked from the command line like this:

```sh
$ simpleirc "irc.strangeloop.io" 6697 "foo" "foo" "Foo the Bar" 1
```

The syntax here is `<server> <port> <nick> <user> <realname> <ssl>`. This will
initialize a connecton to the IRC server. The package will do simple
connection maintenance, such as PONGing on PING.

To interact with the connection layer, send JSON blobs suffixed with <CR> <LF>
over the wire to the simpleirc UNIX socket like so:

```python
>>> import socket
>>> sender = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
>>> listener = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
>>> listener.bind('/tmp/foo.sock')
```

The `sender` socket will provide a line to the simpleirc layer. Messages may be
sent to either register a socket connection you would like simpleirc to
broadcast all messages it receives to (multiple sockets may be registered) or
send a payload back to the connected service. Respectively, these are invoked
as follows:

```python
>>> import json
>>> payload = json.dumps({'register': '/tmp/foo.sock'})' + '\r\n'
>>> sender.sendto(payload, '/tmp/simpleirc.sock')
```

```python
>>> payload = json.dumps({'join': ['#voxinfinitus']}) + '\r\n'
>>> sender.sendto(payload, '/tmp/simpleirc.sock')
```

Finally once an application's listening socket has been registered with the
simpleirc connection you can recieve message from the connection layer like
this:

```python
>>> while True: listener.recv(4096)
... 
```
