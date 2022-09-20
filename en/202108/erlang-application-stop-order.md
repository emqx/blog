An EMQX troubleshooting case study.

Key words: emqx, shutdown crash, shutdown order, race condition

[EMQX](https://github.com/emqx/emqx) is an open-source MQTT broker built on Erlang/OTP which can serve massive amount of TCP/TLS connections. The underlying library for listening and accepting MQTT connections is called [`esockd`](https://github.com/emqx/esockd)

## The trouble

Often (especially under heavy load), when shutdown the broker, we may observe error logs like below.

```erlang
2021-04-20 20:44:39.035 [error]     supervisor: 'esockd_connection_sup - <0.2384.0>'
    errorContext: connection_shutdown_error
    reason: {shutdown,
                {gen_server,call,
                    [<0.2355.0>,{subscribe,<<"device/ca80169898/+/">>}]}}
    offender: [{pid,[<0.17517.29>]},
               {name,connection},
               {mfargs,
                   {emqx_connection,start_link,
                       [[{deflate_options,[]},
                         {max_conn_rate,1000},
                         {active_n,100},
                         {zone,external}]]}}]
```

The only way to explain it, is that by the time when shutting down connections from `esockd_connection_sup`, the `emqx_broker` process is being shutdown (hence causing `gen_server` caller to `EXIT` with reason `{shutdown, TheCall}` .

To reason why such shutdown order may happen, we need to take a closer look at the `emqx`and [`esockd`](https://github.com/emqx/esockd) applications.

In EMQX, `emqx` app depends on `esockd` app, so `esockd` is start prior to `emqx`. Shutdown is, as expected, done in the reversed order: `emqx` is stopped before `esockd`

EMQX delegates its process supervision to `esockd`, in `emqx_app:stop/1`, it first tries to stop all `esockd` listeners (and supervised connection processes) like this:

```erlang
 -spec(stop(State :: term()) -> term()).
 stop(_State) ->
     ok = emqx_alarm_handler:unload(),
     emqx_boot:is_enabled(listeners)
       andalso emqx_listeners:stop().
```

All should work as expected ? No, not really, from the injected `io:format` logs, it looks confusing: it seems that `emqx_sup` is stopped before socket showdown, but the logs are mixed.

```
(emqx@127.0.0.1)1> Stop dashboard listener on 0.0.0.0:18083 successfully.
Stop http:management listener on 0.0.0.0:8081 successfully.
2021-07-27T14:47:54.614910+02:00 [notice] stomp#1:tcp stopped on 0.0.0.0:61613
stopped all children esockd_connection_sup
Stop stomp stomp#1:tcp listener on 0.0.0.0:61613 successfully.
Stop mqttsn mqttsn#1:udp listener on 0.0.0.0:1884 successfully.
2021-07-27T14:47:54.616168+02:00 [notice] exproto#1:tcp stopped on 0.0.0.0:7993
stopped all children esockd_connection_sup
Stop exproto exproto#1:tcp listener on 0.0.0.0:7993 successfully.
terminated emqx_broker {broker_pool,40} # supervisor shutdown
terminated emqx_broker {broker_pool,39}
terminated emqx_broker {broker_pool,38}
....
emqx_app:stop/1 start
2021-07-27T14:47:54.650683+02:00 [notice] default:mqtt_ssl stopped on 0.0.0.0:8883
stopped all children esockd_connection_sup # esockd stop children done
2021-07-27T14:47:54.651288+02:00 [notice] default:mqtt_tcp stopped on 0.0.0.0:1883
stopped all children esockd_connection_sup
2021-07-27T14:47:54.652625+02:00 [notice] internal:mqtt_internal stopped on 127.0.0.1:11883
stopped all children esockd_connection_sup
emqx_app:stop/1 end
2021-07-27T14:47:54.655330+02:00 [info] [Modules] Unload emqx_mod_presence module successfully.
2021-07-27T14:47:54.655457+02:00 [info] [Modules] Unload emqx_mod_recon module successfully.
esockd_app:stop/1
[os_mon] memory supervisor port (memsup): Erlang has closed
[os_mon] cpu supervisor port (cpu_sup): Erlang has closed
```

Let's dig deeper:

In Erlang [documentation](http://erlang.org/doc/apps/kernel/application.html#Module:stop-1)

> Module:stop(State)

This function is called whenever an application has stopped. It is intended to be the opposite of Module:start/2 and is to do any necessary cleaning up. The return value is ignored....

Confirm in source code: [application_master.erl](https://github.com/erlang/otp/blob/ac5e1abc389e6b252da8e5e5dc29d7cd976a8b4d/lib/kernel/src/application_master.erl#L372-L379)

```erlang
loop_it(Parent, Child, Mod, AppState) ->
      receive
      {Parent, get_child, Ref} ->
          Parent ! {child, Ref, Child, Mod},
          loop_it(Parent, Child, Mod, AppState);
      {Parent, terminate} ->
          NewAppState = prep_stop(Mod, AppState),
          exit(Child, shutdown),
          receive
          {'EXIT', Child, _} -> ok
          end,
          catch Mod:stop(NewAppState),
          exit(normal);
```

Meaning, in EMQX, `emqx_sup` is stopped before the listeners.

## The fix

The fix is simple, make use of the `application` behaviour's `prep_stop/1` callback.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
