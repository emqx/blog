One of the defining features of [EMQX](https://www.emqx.io) is its support of clustering: messages in the MQTT topics are forwarded between the broker nodes transparently for the clients. We are developing a system that is fault-tolerant, has high throughput and low latency. Individual nodes can be shut down, restarted or even paused for a long period of time, but the cluster as a whole continues to serve traffic. 

In order to sync and replicate metadata throughout the cluster more efficiently, we've developed Mria: a lightweight eventually-consistent database management system. These features help us create a low-latency, horizontally scalable system, but they also significantly raise the requirements for testing. Development of distributed systems is a notoriously hard problem: some of the most basic assumptions about how the code is executed are not applicable when any part of the system can suddenly die or stutter, when network connections between the nodes may disappear, and the clocks on the different nodes may not be in sync. 

This post is aimed for Erlang and Elixir developers, and it covers some of the unusual and advanced testing techniques that we employ in EMQX and Mria database. We'll talk about chaos engineering in the Erlang applications, model checking, trace-based testing and cluster performance benchmarking. 

# Problem statement

There are two common approaches to testing: 

1. Black box testing, where the tests interact with the system under test (SUT) unknowingly of its internal state. 
2. White box testing, where the tests are fully aware of the system's inner workings, and they may inspect the SUT's state for correctness. 

Black box approach is usually used for testing a fully assembled system. It can find integration problems, but usually it's not great at catching subtle implementation bugs, such as race conditions. 

Traditional white box testing relies on inspecting the internal state of the SUT. It can target subtle implementation details, but the complexity of the test scenarios is typically limited, because the testcase must model the state of the system, either explicitly (as in [stateful property-based tests](http://proper.softlab.ntua.gr/)) or implicitly. The more state deviates from the initial blank slate, the more complex it becomes. 

EMQ X deals with the external traffic that can be malformed or even malicious. It should keep functioning even if some clients are misbehaving. Thankfully, Erlang programming language that we're using was designed with this problem in mind. In a well designed Erlang application, the state of the system is partitioned between multiple processes organized in a supervision tree. If state of one of the processes deviates from normal, the process detects this as early as possible, terminates itself, and lets the supervisor deal with the consequences. Usually supervisor replaces a failed worker process with a healthy one. It creates a small traffic disturbance for one or a few clients, but the system as a whole heals. 

With this design, bugs that may cause corruption of the state are contained, and the system as a whole is not compromised. This approach to fault-tolerance is very elegant, but it creates some challenges for testing: 

1. The partitioned state is harder to inspect 

2. State of a self-healing system, that can drop the incorrect state and replace it with the normal, is very hard to model 

3. Correctness of the supervision tree design should also be tested 

4. Furthermore, state of a distributed system is spread across different hosts 

In order to address these challenges we've decided to move away from analyzing state of the SUT, and focus on inspecting the sequences of actions that it performs. This allows to circumnavigate all the problems mentioned above. Analyzing the execution trace of the system is not exactly a novel idea: it has been studied extensively in the academia and it lies in the foundation of many modern model checkers. However, applying this approach directly to the application-level testing is quite uncommon, and deserves more attention. We'll discuss some real-live examples of this approach in the following chapter. 

# Trace-based testing 

So what is an execution trace? It's a list of side effects that the program performs. For example, *strace* tool prints a list of syscalls performed by a process: 

```
$ strace echo "hello world"
...
newfstatat(1, "", {st_mode=S_IFCHR|0666, st_rdev=makedev(0x1, 0x3), ...}, AT_EMPTY_PATH) = 0 
ioctl(1, TCGETS, 0x7ffc227ed410)        = -1 ENOTTY (Inappropriate ioctl for device) 
write(1, "hello world\n", 12)           = 12 
...
```

By looking at an strace output the programmer can see how the program interacts with the OS and spot problems, like reading a file that doesn't exist. Even more common example is a regular debug log of an application. 

So, to put an idea of trace-based testing in a nutshell: if humans can find bugs by looking at the logs, so can computers. 

# Instrumenting code 

Of course, using the regular textual logs as an input for the tests would be unsustainable. Thankfully, the industry is moving towards structured logs, which are easy to process by both machines and humans. [Snabbkaffe](https://github.com/kafka4beam/snabbkaffe), a tool that we use for trace-based testing uses structured log messages. 

Let's take a look at some real-life code instrumented using snabbkaffe trace points. [Mria](https://github.com/emqx/mria/) project utilizes trace-based testing to a great extent, so we will mostly refer to it in the future examples. One of the main processes in Mria is *mria_rlog_replica*, that is responsible for receiving transaction logs from the upstream server and applying them to the local replica. This process has been implemented as a *gen_statem*, because it is crucial that it goes through certain stages in a specified order:

![gen_statem](https://static.emqx.net/images/c3bcfc9d513f82e381940b9c20246dc1.png)

When a mria replica joins the cluster, it needs to copy the entire contents of the table from the upstream server first. It does so by asking the upstream core node to traverse the tables and send all the key/value pairs back. While this is happening, the replica process resides in bootstrap state. However, the table is constantly being changed by the write operations that are happening in parallel, and these changes needs to be applied on top of data transferred during the bootstrap stage. So, while bootstrap stage is going on, the replicant node receives the transaction logs from the upstream core node and queues them up for later. Once the bootstrapping is done, the replica process proceeds to replaying the saved transaction logs. While doing so, it resides in local_replay state. Once it reaches the end of the saved transaction log, it enters normal state where it applies transaction logs in the real time, and the local data can be consumed by the business applications. 

Let's look at a short snippet of code taken from this module:

```
-module(mria_rlog_replica).

-behaviour(gen_statem).

%% We need to include a header file that defines trace macros:
-include_lib("snabbkaffe/include/trace.hrl").

...

handle_state_trans(OldState, State, Data) ->
    ?tp(info, state_change,
        #{ from => OldState
         , to => State
         }),
    keep_state_and_data.
```

Every time the state machine enters a new state, it emits a trace event with kind state_change and a few parameters. This is one of the many trace events that are used in the tests.

The trace points serve multiple purposes: 

- They are collected to an execution trace that can be inspected at the end of the testcase 
- The testcase can wait for a certain event, and wake up immediately once the system emits it. This is an elegant alternative to sleeps in the tests, it makes tests run much faster and it lets us forget about tuning timeouts forever. 
- In a test build trace points can be used to inject faults into the system 
- They can be used to inject process schedulings into the system 

A trace captured during execution of the testcase may look like this: 

```
...
#{'$kind' => rlog_replica_start,
  node => 'n2@localhost',
  shard => test_shard,
  '~meta' => #{domain => [mria,rlog,replica],gl => <21003.170.0>,node => 'n2@localhost',pid => <21003.238.0>,shard => test_shard,time => -576460747034753}
 }.
#{'$kind' => state_change,
  from => disconnected,
  to => bootstrap,
  '~meta' => #{domain => [mria,rlog,replica],gl => <21003.170.0>,node => 'n2@localhost',pid => <21003.238.0>,shard => test_shard,time => -576460747034571}
 }.
...
```

Let's go through all these features. 

## Trace specifications 

As we discussed in the previous chapter, it's important that the state machine goes through the specified states in a certain order. Given the event trace of the system, we can easily implament a rule that verifies this property. Below you can find a test found in the actual check: 

```
replicant_bootstrap_stages(Trace0) ->
    Trace = ?of_domain([mria, rlog, replica|_], Trace0),
    ?causality( #{?snk_kind := state_change, to := disconnected, ?snk_meta := #{pid := _Pid}}
              , #{?snk_kind := state_change, to := bootstrap,    ?snk_meta := #{pid := _Pid}}
              , Trace
              ),
    ?causality( #{?snk_kind := state_change, to := bootstrap,    ?snk_meta := #{pid := _Pid}}
              , #{?snk_kind := state_change, to := local_replay, ?snk_meta := #{pid := _Pid}}
              , Trace
              ),
    ?causality( #{?snk_kind := state_change, to := local_replay, ?snk_meta := #{pid := _Pid}}
              , #{?snk_kind := state_change, to := normal,       ?snk_meta := #{pid := _Pid}}
              , Trace
              ).
```

It can be split in two parts: 

- First it extracts relevant events from the execution trace
- Then for every state_change event happening in any process, it verifies that the process transitions to a correct next state. 

So how it is different from the traditional approach to testing state machines using stateful property-based testing?

- First of all, the model of the state machine is much simpler. We only specify the expected causal relationship between the state transitions as a pure function operating on a list of historical events. Execution of the testcase and verifying the properties are untangled.
- The state machine runs inside a fully assembled application, together with its supervision tree, instead of a simulated environment controlled by [PropER](http://proper.softlab.ntua.gr/Tutorials/PropEr_testing_of_generic_servers.html). This way we can catch integration problems on the application level.
- Moreover, the release runs in a distributed Erlang cluster with a real upstream core node. So the testcase can catch integration problems on the protocol level. 

This method has one shortcoming in comparison with the traditional stateful property-based testing approach, though. Property-based tests can plan for more rare sequences of events, and therefore they can explore the state space more reliably. In the next chapters we'll talk how to mitigate this problem. 

Trace-based testing has another advantage: in a fault-tolerant system some errors may be easy to overlook, because the system recovers automatically. While this is great for running a system in production, it is not desirable in the test environment. Adding trace points in the error recovery paths solves this problem, because the testcase can easily verify absence of unexpected recovery events.

## Testing supervisors with fault injection

Supervisors are the glue that keep Erlang applications together. Tuning the supervision trees is more of an art than a science, however. We've changed that by applying chaos engineering approach to the Erlang processes. 

Snabbkaffe allows to inject a crash into any trace point using a special macro: 

```
?inject_crash( #{?snk_kind := state_change, to := normal}
             , snabbkaffe_nemesis:random_crash(0.1)
             )
```

This macro allows to specify a match pattern for the trace events that should result in crash, and a fault scenario. There is a variety of fault scenarios, that allow to emulate real life scenarios like a temporary failure of an external resource, unstable network connection, and more:

```
snabbkaffe_nemesis:always_crash()
snabbkaffe_nemesis:recover_after(10)
snabbkaffe_nemesis:random_crash(0.1)
snabbkaffe_nemesis:periodic_crash(_Period = 10, _DutyCycle = 0.5, _Phase = math:pi())
```

Typically we create a separate "fault-tolerance" test suite that injects a wide variety of crashes into the SUT, and let it run under traffic for a prolonged period of time. Then the suite runs the checks on the collected traces of the SUT to make sure it recovers reliably and correctly. 

## Scheduling injections 

Another feature of the trace points is that they can be used to conditionally delay execution of an Erlang process. This is called scheduling injection. To explain why it's useful, let's get back to the replicant state machine. We want to make sure that it handles all the transactions happening in the upstream cluster, regardless of the local state. In order to test this we delay state transitions until a certain number of upstream transactions is produced and vice versa. It is done by adding thefollowing code in the beginning of the testcase:



```
%% 1. Commit some transactions before the replicant start:
?force_ordering(#{?snk_kind := trans_gen_counter_update, value := 5},
                #{?snk_kind := state_change, to := disconnected}),
%% 2. Make sure the rest of transactions are produced after the agent starts:
?force_ordering(#{?snk_kind := subscribe_realtime_stream},
                #{?snk_kind := trans_gen_counter_update, value := 10}),
%% 3. Make sure transactions are sent during TLOG replay:
?force_ordering(#{?snk_kind := state_change, to := bootstrap},
                #{?snk_kind := trans_gen_counter_update, value := 15}),
%% 4. Make sure some transactions are produced while in normal mode
?force_ordering(#{?snk_kind := state_change, to := normal},
                #{?snk_kind := trans_gen_counter_update, value := 25})
```

Scheduling injection allows to verify absence of race conditions in the otherwise unlikely execution paths. Both error and scheduling injection fully support the distributed Erlang. 

# Concuerror model checker

The last testing technique that we will touch on in this post is model checking. [Concuerror](https://concuerror.com/) is an ultimate tool for verifying concurrent systems, because it explores all possible execution paths of the concurrent program. 

Previously we mentioned the algorithm of making a database replica using dirty reads and replaying the transaction log. This algorithm does not look immediately obvious, so we apply Concuerror to verify it. Since Concuerror doesn't support Erlang distribution, we emulate both upstream and downstream databases on a single machine.

First the testcase creates two tables, and populates the source table with some data: 

```
SourceTab = ets:new(source, [public, named_table]),
ReplicaTab = ets:new(replica, [public, named_table]),
%% Insert some initial data:
ets:insert(source, {1, 1}),
ets:insert(source, {2, 2}),
ets:insert(source, {3, 3}),
...
```

Then it starts three processes: importer, bootstrapper and replica. Importer emulates a process that is responsible for importing real-time transactions to the upstream database. Importer process only writes data to the source table. Bootstrapper process emulates a temporary worker process that sends the contents of the source table to the replica process. And the replica process emulates a simplified version of mria_rlog_replica state machine that was discussed in the previous chapter.

```
Replica = spawn_link(fun replica/0),
register(replica, Replica),
%% "importer" process emulates mnesia_tm:
spawn_link(fun importer/0),
%% "bootstrapper" process emulates bootstrapper server:
spawn_link(fun bootstrapper/0),
```

Importer process inserts the transaction ops to the source table emulating the business logic modifying the table. It also sends the ops to the replica process, so it can replay them later:

```
importer() ->
    Ops = [ {write, 3, 3}
          ...
          , {write, 5, 5}
          ...
          , {delete, 5}
          ],
    lists:map(fun(OP) ->
                      import_op(source, OP),
                      replica ! {tlog, OP}
              end,
              Ops)
```

At the same time the bootstrapper process traverses the source table and sends data to the replica process:

```
bootstrapper() ->
    {Keys, _} = lists:unzip(ets:tab2list(source)),
    [replica ! {bootstrap, K, V} || K <- Keys, {_, V} <- ets:lookup(source, K)],
    replica ! bootstrap_done.
```

The replica process starts in boostrap state, where it receives the messages from the bootstrap process, and once it receives the last message, it can replay the queued ops: 

```
replica() ->
    receive
        {bootstrap, K, V} ->
            import_up(replica, {write, K, V}),
            replica();
        bootstrap_done ->
            replay()
    end.

replay() ->
    receive
        {tlog, Op} ->
            import_op(replica, Op),
            replay();
        last_trans ->
            ok
    end.
```

Finally, when everything is done, the testcase verifies that the contents of the two tables are the same: 

```
SrcData = lists:sort(ets:tab2list(source)),
RcvData = lists:sort(ets:tab2list(replica)),
?assertEqual(SrcData, RcvData)
```

When Concuerror executes this code, it shuffles every ets operation, every message send and message received in any way possible, to make sure the algorithm is free of race conditions and deadlocks. 

Concuerror is a unique tool that can give unprecedented confidence in the correctness of the algorithm, next only to a formal proof, but it requires careful design of both business logic and the testcases. Concuerror supports most of the Erlang features with some exceptions, so the application code sometimes needs to work around these limitations. Also time and memory complexity of the model grows exponentially, so it should be kept simple to be reasonable in a CI.
