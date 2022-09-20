Erlang is a general-purpose, concurrent, functional programming language, as
well as a garbage-collected runtime system.The Erlang runtime system is known
for its designs that are well suited for systems with the following
characteristics:

- Distributed
- Fault-tolerant
- Soft real-time
- Hot swapping, Highly available, non-stop applications where code can be changed
- without stopping a system （1）

## Better for building distributed system and distributed computing

Built from the ground up with concurrency and distributed computing in mind
Erlang has strong roots with the telecom industry in which concurrent processes
are normal. It’s designed to be concurrent, to be used for distributed computing
and to be scalable.<br> It is also great for writing distributed applications.
Erlang is made to be parallel and distributed, so it’s very easy to write code
that uses multiple processor cores, it’s also very easy to write applications
that span multiple servers, comparing to that you have to using actor lib in
Scala to write parallel programs.

## Better fault tolerance

Fault tolerance means that a system has the property to continue operating even
though one or more components have failed. For Erlang systems, this means that
the system is kept running even if for example a user has to drop a phone call
rather than forcing everyone else to do so.<br> Erlang has better fault
tolerance than Scala, because its VM ensures full share-nothing isolation
between processes (actors) — right down to having separate heaps and garbage
collection for each. This is something that Scala cannot achieve, because it is
built on top of the JVM. (3)

For Erlang systems, this means that the system is kept running even if for
example a user has to drop a phone call rather than forcing everyone else to do
so.<br> In order to achieve this, Erlang’s VM gives you:

* Knowledge of when a process died and why that happened
* The ability to force processes to die together if they depend on each other and
if one of them has a fault
* A logger that logs every uncaught exception
* Nodes that can be monitored so that you find out when they go down
* The ability to restart failed processes (or groups of them)

## Better soft real-time support due to Erlang actor scheduling

Both Erlang and Scala are using actor model (contrast with other threads based
concurrent models). In the actor model, each object is an actor. This is an
entity that has a mailbox and a behavior. Messages can be exchanged between
actors, which will be buffered in the mailbox. Upon receiving a message, the
behavior of the actor is executed, upon which the actor can: send a number of
messages to other actors, create a number of actors and assume new behavior for
the next message to be received.

Erlang uses a preemptive scheduler for the scheduling of processes. When they
have executed for a too long period of time (usually measured in the amount of
methods invoked or the amount of CPU-cycles used), or when they enter a receive
statement with no messages available, the process is halted and placed on a
scheduling queue.This allows for a large number of processes to run, with a
certain amount of fairness. Long running computations will not cause other
processes to become unresponsive. Erlang run-time environment has support for
symmetric multiprocessing (SMP)This means that it is able to schedule processes
in parallel on multiple CPUs, allowing it to take advantage of multi-core
processors. The functional nature of Erlang allows for easy parallelization. An
Erlang lightweight process (actor) will never run in parallel on multiple
processors, but using a multi-threaded run-time allows multiple processes to run
at the same time. Big performance speedups have been observed using this
technique.

Scala makes the distinction between thread-based and event-based actors.<br>
Thread-based actors are actors which each run in their own JVM thread. They are
scheduled by the Java thread scheduler, which uses a preemptive priority-based
scheduler. When the actor enters a receive block, the thread is blocked until
messages arrive. Thread-based actors make it possible to do long-running
computations, or blocking I/O operations inside actors, without hindering the
execution of other actors.There is an important drawback to this method: each
thread can be considered as being heavy-weight and uses a certain amount of
memory and imposes some scheduling overhead. When large amounts of actors are
started, the virtual machine might run out of memory or it might perform
suboptimal due to large scheduling overhead.

In situations where this is unacceptable, event-based actors can be used.
Event-based actors provide a more light-weight alternative, allowing for very
large numbers of concurrently running actors. However, they should not be used
for parallelism: since all actors execute on the same thread, there is no
scheduling fairness. (4)

## Hot swapping

Since Erlang was designed for reliability, hot swapping code (replacing code in
runtime) is built in.<br> The JVM has some support for hot swapping code.
Classes can be changed, but due to the static type system, method signatures can
not be changed — only the content of a method. In a real-time system it may not
be possible to stop the system in order to implement code upgrades. For these
cases Erlang gives you dynamic code upgrade support for free when using OTP. The
mechanism is very easy to understand and works as follows:

* Start the app
* Edit the code
* Recompile

That’s all that is needed, the app updates with the new code while it’s still
running and tests are run automatically. (5)

Because Akka (Scala’s actor library)can’t magically patch over the JVM’s shared
memory model:
[https://doc.akka.io/docs/akka/snapshot/](https://doc.akka.io/docs/akka/snapshot/).
And because the JVM does global stop-the-world garbage collection, which makes
soft real-time implausible because of the unpredictability of GC affecting your
actors. Erlang has per-process heaps. Basically the Erlang VM was created for
this use case while the JVM was not, and its not something you can just add with
a library.

(1)Erlang (programming language)
[https://en.wikipedia.org/wiki/Erlang_(programming_language)](https://en.wikipedia.org/wiki/Erlang_(programming_language))<br>
(2)[https://www.slant.co/versus/116/11675/~scala_vs_erlang](https://www.slant.co/versus/116/11675/~scala_vs_erlang)<br>
(3)[https://www.scala-lang.org/old/node/1070.html](https://www.scala-lang.org/old/node/1070.html)<br>
(4)Concurrency in Erlang & Scala: The Actor Model
[https://rocketeer.be/articles/concurrency-in-erlang-scala/](https://rocketeer.be/articles/concurrency-in-erlang-scala/)<br>
(5)The multicore crises: Scala vs. Erlang
[https://www.infoq.com/news/2008/06/scala-vs-erlang](https://www.infoq.com/news/2008/06/scala-vs-erlang)

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
