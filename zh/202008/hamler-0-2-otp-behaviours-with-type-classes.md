

我们在这里很高兴地和大家分享 Hamler 0.2 版本发布的消息！

Hamler 是一门构建在 [Erlang](https://www.erlang.org/) 虚拟机(VM)上的 [Haskell](https://www.haskell.org/) 风格的强类型(Strongly-typed)编程语言，独特地结合了编译时的类型检查推导，与对运行时高并发和软实时能力的支持。

![HamlerCompilerDesign](https://static.emqx.net/images/15dc96a3d0ae43081a138cac15c2546d.png)

Hamler 0.2 现已支持大部分 Erlang 的并发编程特性，包括基于 Actor Model 的 Message Passing Concurrency 和 OTP Behaviours。

## 关于 Actor Model

1974年，卡尔-休伊特教授发表了论文《Actor model of computation》。文中，他阐述了 Actor 作为一个计算实体，它会对收到的消息作出回应，并可以并发地进行以下操作：

- 向其他 Actor 发送有限数量的消息
- 创建有限数量的新 Actor
- 指定下一个收到的消息所要使用的行为

随着多核计算和大规模分布式系统的兴起，Actor 模型因其天然的并发性、并行性和分布式变得越来越重要。

## Process and Mailbox

Hamler/Erlang 中的 Actor 被定义为一个进程，它的工作方式就像一个 OS 进程。每个进程都有自己的内存，由一个 Mailbox、一个 Heap、一个 Stack 和一个包含进程信息的 Process Control Block(PCB) 组成。

![Process](https://static.emqx.net/images/9aebe5ddeae7568a8c283fd1fa567dad.png)

Erlang 中的进程是非常轻量的，我们可以在一个正在运行的 Erlang 虚拟机上快速创建数百万个进程。

## Message Passing Concurrency

"Message passing concurrency（MPS）是两个或多个进程之间没有共享资源情况下的并发，它们通过仅传递消息进行通信。" Actor Model 就是 MPS 模型的一个实现。

*参考资料：*

*[MessagePassingConcurrency](https://wiki.c2.co/?MessagePassingConcurrency)*

*[AlanKayOnMessaging](https://wiki.c2.com/?AlanKayOnMessaging)*

**Ping/Pong示例**：

```
import Prelude
import Control.Process (selfPid)

go :: Process ()
go = do
  self <- selfPid
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

**Receive ... after示例**：

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

**Selective Receive 示例**：

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

Hamler 采用类型类(TypeClass)实现 OTP Behaviour。

TypeClass 定义了具有类似 operation 的一组类型。在我们的实现中，使用 typeclass 来对不同 OTP Behaviour 的类型进行区分。通过为每个 Behavour 定义一个 typeclass 的方式，我们对这些 Behaviour 做了某种程度上的抽象，并在一定程度上增加了类型约束。

### GenServer Behaviour

Generic Server Behaviour 是对 *客户端-服务器* 关系模型中服务器的抽象。如图所示，在该模型的服务器侧，所有的通用操作都可以被封装成为一个模块。与 Erlang 一样，Hamler 将其封装为 GenServer 的模块。不同的是在 Hamler 中 GenServer 由类型类进行定义，它所有的回调函数和参数都必须受到类型约束，它在具备 Erlang 的 `gen_server` 特性的同时，也保证了类型的安全。以 `handleCall` 和 `handleCast` 为例：

*参考资料 [Erlang gen_server Behaviour](https://erlang.org/doc/design_principles/gen_server_concepts.html)*。

![ClientServerMode](https://static.emqx.net/images/03ca074fb68effed09640b7c28103b4c.png)

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

GenStatem Behaviour 抽象了对于 **事件驱动的有限状态机(Event-driven Finite State Machine)** 中通用的操作。对于该类型的状态机来说，它以触发状态转换的事件作为输入，而在状态转换过程中执行的动作作为输出，并得到新的状态。其模型如下：

```
State(S) x Event(E) -> Actions(A), State(S')
```

与 Erlang 中的实现类似，Hamler 使用 **GenStatem** 类型类对此状态机的通用操作进行封装。在 `GenStatem` 中仅提供一个事件处理的回调函数。其声明如下：

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

**Supervisor Behaviour** 抽象了进程间容错的通用操作，它作为一个特殊的进程，以 **监督者(Supervisor)** 的角色管理其子进程，并在出现异常时重启相关的子进程，以提高系统的容错能力。

在 Hamler 中，这类行为被封装为 **Supervisor** 的类型类，并提供一个 `init` 回调函数来配置监督者的行为和子进程列表。这里的实现与 Erlang 中的 `supervisor` 是一致的。

### Supervision Tree

监督者可以监控上文提到的 `GenServer` 或 `GenStatem` 生成的进程，同样也可以监控另外一个监督者。这便构成了 **监控树(Supervision Tree)**。如下图所示：

![SupervisorTree](https://static.emqx.net/images/9091ca68398a470a2d35e88b93824221.png)

其中矩形表示一个监督者，圆表示一个工作者（它可以是一个 GenServer，GenStatem 或其它任意的进程）。当有进程异常退出时，监督者会按回调函数中配置的方式进行重启，例如：

- '1' 表示 `one_for_one`：仅重启异常退出的子进程。
- 'a' 表示 `one_for_all`：重启该监督者下所有的子进程。

参考资料：[Supervision Principles](https://erlang.org/documentation/doc-4.9.1/doc/design_principles/sup_princ.html) [Erlang Supervisor Behaviour](https://erlang.org/doc/design_principles/sup_princ.html)

**A Supervisor Example**

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

## 欢迎加入 Hamler 编程语言社区

Hamler 函数编程语言从发起即是一个开源项目，项目托管在 GitHub: https://github.com/hamler-lang/ 。 **Hamler** 目前由 [EMQ - 杭州映云科技有限公司](https://www.emqx.cn/about) 研发团队主导开发，计划在 2020 年底前发布 0.5 版本用于 **EMQ X** 6.0 的开发。

## EMQ 公司介绍 

**EMQ - 杭州映云科技有限公司**致力于成为全球领先的消息与流处理开源软件企业，聚焦服务于新产业周期的 5G&IoT、边缘计算(Edge)与云计算(Cloud)市场。 **EMQ** 研发团队主要采用 Erlang、Haskell 等函数编程语言，开发高并发、高可靠、软实时的大规模分布式系统