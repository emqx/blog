
## Introducing Hamler 0.2

We are proud to announce that Hamler 0.2 has been released.

**Hamler** is a strongly-typed functional programming language running on Erlang VM.

![HamlerCompilerDesign](https://static.emqx.net/images/3f8ad72d2095e22f1f855fb21c7c7fba.png)

Hamler 0.2 will support most of Erlang's concurrent programming features, including Actor Model and OTP Behaviours.

## About Actor Model

Professor Carl Hewitt published the famous paper Actor model of computation in 1974. In the thesis, he elaborates that:

An Actor is a computational entity that, in response to a message it receives, can concurrently:

- send a finite number of messages to other Actors;
- create a finite number of new Actors;
- designate the behaviour to be used for the next message it receives.

With the rise of multi-core computing and large-scale distributed systems, the Actor Model is becoming increasingly important because of its concurrent, parallel and distributed nature.

## Process and Mailbox

An actor in Hamler/Erlang is defined as a process, which works similarly to an OS process. Each process has its own memory, composed of a mailbox, a heap, a stack and a process control block(PCB) with information about the process.

![Process](https://static.emqx.net/images/d11dfdc2f22c79d5e4d514be83c7cfe5.png)

Processes in Erlang are very lightweight. We can create millions of processes on a running Erlang virtual machine.

## Message Passing Concurrency

"Message passing concurrency (MPS) is concurrency among two or more processes where there is no shared region between the two processes, and they communicate by passing messages." Actor Model is one example of MPS model.

*Reference:* *[MessagePassingConcurrency](https://wiki.c2.com/?MessagePassingConcurrency)*, *[Alan Kay On Messaging](https://wiki.c2.com/?AlanKayOnMessaging)*

**Example: Ping/Pong**

```
import Prelude

go :: Process ()
go = do
  self <- getSelf
  pid <- spawn loop
  pid ! (self, :ping)
  receive
    :pong -> println "Pong!"
  pid ! :stop

loop :: Process ()
loop =
  receive
    (from, :ping) -> do
      println "Ping!"
      from ! :pong
      loop
    :stop -> return ()
```

**Example: Receive ... after**

```
go :: Process ()
go = do
  pid <- spawn recvAfter
  pid ! :foo

recvAfter :: Process ()
recvAfter =
  receive
    :bar -> println "recv bar"
  after
    1000 -> println "timeout"
```

**Example: Selective Receive**

```
go :: Process ()
go = do
  pid <- spawn selectiveRecv
  pid ! :bar
  pid ! :foo

selectiveRecv :: Process ()
selectiveRecv = do
  receive :foo -> println "foo"
  receive :bar -> println "bar"
```

## OTP Behaviours

Hamler implements OTP Behaviours with Type Classes.

Type classes define groups of types related by their operations. In this case, we use type class to group types with certain behaviours. By defining a typeclass for each behaviour, we can provide some abstraction over these behaviours and add type constraint to some extent. However, though the solution works fine, it is obvious the implementation is not complete and requires further investigation.

### GenServer Behaviour

`gen_server` module in Erlang provides the server of a client-server relation. As shown in the graph, the model is usually used for resource management operations where multiple clients need to share a common resource. All the operations in Server are abstracted by the module. So process implemented via this module will have a standard set of functions. This fits quite well with the idea of type class. Therefore, We implemented `gen_server` with type class `GenServer `. This way, the behaviours of the server are constraint by its type. For example, `handleCall` and `handleCast` represent the operations of a certain type of server, and their behaviours are determined by their types.

*Reference: [Erlang gen_server Behaviour](https://erlang.org/doc/design_principles/gen_server_concepts.html)*

![ClientServerMode](https://static.emqx.net/images/8562ae276509440287ba7475e0b8b628.png)

**GenServer Typeclass**

```
class GenServer req rep st | req -> rep, rep -> st, st -> req where
  handleCall :: HandleCall req rep st
  handleCast :: HandleCast req rep st
```

**A simple Server Example**

```
module Demo.Server
  ( start
  , inc
  , dec
  , query
  ) where

import Prelude
import Control.Behaviour.GenServer
  ( class GenServer
  , HandleCall
  , HandleCast
  , Init
  , startLinkWith
  , initOk
  , call
  , cast
  , noReply
  , reply
  , shutdown
  )
import System.IO (println)

data Request = Inc | Dec | Query
data Reply = QueryResult Integer
data State = State Integer

name :: Atom
name = :server

start :: Process Pid
start = startLinkWith name (init 20)

inc :: Process ()
inc = cast name Inc

dec :: Process ()
dec = cast name Dec

query :: Process Integer
query = do
  QueryResult i <- call name Query
  return i

instance GenServer Request Reply State where
  handleCall = handleCall
  handleCast = handleCast

init :: Integer -> Init Request State
init n = initOk (State n)

handleCall :: HandleCall Request Reply State
handleCall Query _from (State i) = do
  println "Call: Query"
  reply (QueryResult i) (State i)
handleCall _req _from st =
  shutdown :badRequest st

handleCast :: HandleCast Request Reply State
handleCast Inc (State n) = do
  println "Cast: Inc"
  noReply $ State (n+1)
handleCast Dec (State n) = do
  println "Cast: Dec"
  noReply $ State (n-1)
handleCast _ st = noReply st
```

### GenStatem Behaviour

"For an Event-Driven Finite State Machine, the input is an event that triggers a state transition and the output is actions executed during the state transition"

```
State(S) x Event(E) -> Actions(A), State(S')
```

`gen_statem` module in Erlang has abstracted general operations for this State Machine. In Hamler, we use `GenStatem` to encapsulate `gen_statem`. However, in our implementation , we can see that current `GenStatem` only supports one call back mode which events are handled by one single call back function `handleEvent`.

*Reference: [gen_statem Behaviour](https://erlang.org/doc/design_principles/statem.html)*

**GenStatem Typeclass**

```
class GenStatem e s d | e -> s, s -> d, d -> e where
  handleEvent :: HandleEvent e s d
```

**CodeLock FSM Example**

```
module Demo.FSM.CodeLock
  ( name
  , start
  , push
  , stop
  ) where

import Prelude

import Control.Behaviour.GenStatem
  ( class GenStatem
  , Action(..)
  , EventType(..)
  , Init
  , OnEvent
  , initOk
  , handleWith
  , unhandled
  )
import Control.Behaviour.GenStatem as FSM

data Event = Button Integer | Lock
data State = Locked | Opened
data Data = Data
  { code :: [Integer]
  , length :: Integer
  , buttons :: [Integer]
  }

instance Eq State where
  eq Locked Locked = true
  eq Opened Opened = true
  eq _ _ = false

instance GenStatem Event State Data where
  handleEvent = handleWith [(Locked, locked), (Opened, opened)]

name :: Atom
name = :code_lock

start :: [Integer] -> Process Pid
start code = FSM.startLinkWith name (init code)

push :: Integer -> Process ()
push n = FSM.cast name (Button n)

stop :: Process ()
stop = FSM.stop name

init :: [Integer] -> Init Event State Data
init code = initOk Locked d
  where d = Data $ { code = reverse code
                   , length = length code
                   , buttons = []
                   }

locked :: OnEvent Event State Data
locked Cast (Button n) (Data d) =
  let buttons = take d.length [n|d.buttons]
   in if buttons == d.code then
        let actions = [StateTimeout 1000 Lock] in
            FSM.nextWith Opened (Data d{buttons = []}) actions
      else FSM.keep (Data d{buttons = buttons})

locked t e d = unhandled t e Locked d

opened :: OnEvent Event State Data
opened Cast (Button _) d = FSM.keep d

opened Timeout Lock d = do
  println "Timeout Lock"
  FSM.next Locked d

opened t e d = unhandled t e Opened d
```

## Supervisor Behaviour

Supervision model is used for programming fault-tolerant application. The basic idea is that if the child process goes wrong its supervisor can restart the worker. Supervisor behaviour abstracts this model.

Using instances of supervisor behaviour, we can create a supervision tree via a supervision start specification `init`. The tree in the graph is a typical example of a supervision tree. From the graph, we can see that supervisor can be a child of another supervisor.

- 1 means "one for one", so only the dead child is restarted by the supervisor.
- A means "one for all", so all the children will be terminated and restarted if one of them dies.

![SupervisorTree](https://static.emqx.net/images/dad77bd3c025207b849f53abe1365dec.png)

*Reference:* *[Supervision Principles](https://erlang.org/documentation/doc-4.9.1/doc/design_principles/sup_princ.html)*, *[Erlang Supervisor Behaviour](https://erlang.org/doc/design_principles/sup_princ.html)*

### A Supervisor Example

```
module Demo.Sup (start) where

import Prelude

import Demo.Event as Event
import Demo.Server as Server
import Demo.FSM.PushButton as FSM
import Control.Behaviour.Supervisor
  ( Init
  , initOk
  , Strategy(..)
  , childSpec
  , startSupWith
  )

name :: Atom
name = :sup

start :: Process Pid
start = startSupWith name init

init :: Init
init = initOk (OneForOne, 10, 100)
  [ childSpec "Demo.Event" Event.start
  , childSpec "Demo.Server" Server.start
  , childSpec "Demo.Statem" FSM.start
  ]
```

## Welcome to the Hamler community!

The Hamler functional programming language has been an open-source project since its inception and is hosted on GitHub: [https://github.com/hamler-lang/](https://github.com/hamler-lang/) . **Hamler** is currently being developed and maintained by the RD team of [EMQ Technologies Co., Ltd.](https://www.emqx.io/). We plan to release version 0.5 for the development of EMQ X 6.0 by the end of 2020.

To contribute to **Hamler** project:

- Report issues: submit any bugs, issues to [hamler/issues](https://github.com/hamler-lang/hamler/issues)
- Contribute code: Fork the project, and submit feature requests to [hamler-lang/hamler](https://github.com/hamler-lang/hamler)
- Submit a proposal: Fork the [hamler-wiki](https://github.com/hamler-lang/hamler-wiki) project and submit pull request