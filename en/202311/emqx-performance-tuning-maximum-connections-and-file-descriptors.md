While testing the performance of EMQX, if the number of client connections reaches a large number, you may find that EMQX cannot accept more connections, and the following error log appears in the console or `/var/log/emqx/emqx.log.N`:

```
[error] Accept error on 0.0.0.0:1883: EMFILE (Too many open files)
```

This indicates that the number of file descriptors opened by EMQX has reached the maximum limit. This is a resource limit enforced by Linux. If we want to lift this limit, we need to modify the corresponding kernel parameters of Linux.

In this article, we will introduce how to modify kernel parameters to increase the number of file descriptors that EMQX can use on Linux.

## What is a file descriptor?

A [file descriptor](https://en.wikipedia.org/wiki/File_descriptor) is an index created by the Linux system kernel for efficient management of open files. When we open a file using the following function call, fd is the file descriptor returned by the kernel:

```
fd = open("example.txt", O_RDWR)
```

Then, we can perform various read and write operations on the opened file through this `fd`. Linux will index the correct file according to `fd`.

In Linux systems, all resources can be treated as files. In addition to normal files such as text files and executable files, file directories, hardware devices, and network sockets (Network Socket) are also considered as files.

As an MQTT server, EMQX will create a socket for each newly connected client. Correspondingly, this will consume a file descriptor.

To prevent the process from inadvertently or maliciously opening too many file descriptors, the Linux system limits the number of file descriptors each user and process can open. The default limit is often hard to meet the demands of an MQTT server with many device connections. Therefore, we have to modify kernel parameters for EMQX.

## Tune the maximum limit of file descriptors

In Linux systems, the maximum number of file descriptors that a process can ultimately use is influenced by several kernel parameters or configuration files. They are:

### /proc/sys/fs/file-max

The value defined in `/proc/sys/fs/file-max` determines the maximum number of file descriptors available to the entire system. We can view the current limit by using the following command:

```
cat /proc/sys/fs/file-max
```

If the current value is smaller than our desired value, we can run the following command to modify it:

```
echo <Number> > /proc/sys/fs/file-max
```

Or

```
sysctl -w fs.file-max = <Number>
```

Both of the above commands can make the changes take effect immediately, but the disadvantage is that the changes are only effective in the current session. Once the user logs out or the system is restarted, our changes will become invalid. If we want to make the changes permanent, we can open the file `/etc/sysctl.conf` and add the following content:

```
fs.file-max = <Number>
```

Execute the following command to make the changes in `/etc/sysctl.conf` take effect immediately:

```
sysctl -p
```

Generally, we recommend setting the maximum number of file descriptors slightly larger than the target value to avoid affecting the normal operation of other services in the system.

### /proc/sys/fs/nr_open

The value defined in `/proc/sys/fs/nr_open` determines the maximum setting for the number of file descriptors that each process can open. It does not directly affect the process but determines the maximum value other parameters can be set to.

It is similar to `/proc/sys/fs/file-max`, view the current value:

```
cat /proc/sys/fs/nr_open
```

Temporary modification:

```
echo <Number> > /proc/sys/fs/nr_open
```

Or

```
sysctl -w fs.nr_open = <Number>
```

Permanent changes can be made by adding the following line to the file `/etc/sysctl.conf`:

```
fs.nr_open = <Number>
```

Then execute the following command to make the changes take effect immediately:

```
sysctl -p
```

### /etc/security/limits.conf

In this file, we can set limits for various resources for users who log in through [PAM](https://en.wikipedia.org/wiki/Linux_PAM) (Pluggable Authentication Modules), such as the maximum number of processes, and the maximum number of open file descriptors. When we use the `emqx` command with the option `console` or `start` to start EMQX, the maximum number of file descriptors that EMQX can open is limited by `/etc/security/limits.conf`.

Each line in `limits.conf` uses the following format to describe a limit for the user.

```
<domain> <type> <item> <value>
```

`<domain>` determines which users this limit applies to. We can use a username, or group name (preceded by @ to distinguish it from usernames), or directly use the wildcard * to limit all users.

`<type>` determines whether this is a soft or hard limit. The soft limit is the current actual resource limit, while the hard limit is the upper limit to which the soft limit can be set. After the limits in `limits.conf` take effect, only the root user can increase their hard limit. Common users can only adjust their soft limit within the range of the hard limit or decrease the hard limit.

`<item>` is used to specify the type of resource. For example, **nproc** represents the maximum number of processes, **nofile** represents the maximum number of open file descriptors. The available `<item>` list can be viewed in `/etc/security/limits.conf`. In addition, we should also note the difference between different resource limits. For example, **nproc** is used to limit the maximum number of processes that a user can create simultaneously, but **nofile** is not the maximum number of file descriptors that a user can open simultaneously. It's an independent limit for each process created by the user.

`<value>` is the specific limit size.

Here is a simple example. It indicates that the maximum number of file descriptors that `root` and `emqx` users can open is 65535 by default, but the `root` user can break this limit at any time, the `emqx` user cannot. The maximum number of file descriptors that all other users can open is 1024 by default, but can be adjusted up to 4096:

```
root soft nofile 65535
root hard nofile 65535
emqx soft nofile 65535
emqx hard nofile 65535
*   soft nofile 1024
*   hard nofile 4096
```

The soft and hard limits of **nofile** cannot exceed `/proc/sys/fs/nr_open`, which is something to pay special attention to. This is because Linux will not check and limit our modifications, but if we exceed this limit, it will cause the system to be unable to log in.

After we have made changes to `/etc/security/limits.conf`, we must log out of the session and log back in again for the changes to take effect. After logging back in, we can use the following command to confirm whether the changes have been successfully applied:

```
ulimit -n
```

We can also use the `-Sn` and `-Hn` options to view the currently effective soft and hard limits separately:

```
ulimit -Sn
ulimit -Hn
```

### ulimit -n

Changes in the file `/etc/security/limits.conf` are permanent, but sometimes we may want to make temporary changes. In this case, we can use the `ulimit` command. We just introduced how to use it to view the current resource limits, we will see how to use it to modify resource limits, for example, modifying both soft and hard limits simultaneously:

```
ulimit -n <Number>
```

Or modify the soft and hard limits separately:

```
ulimit -Sn <Number>
ulimit -Hn <Number>
```

Please note that we can never the soft limit exceed the hard limit, and non-root users can only reduce the hard limit, only the `root` user can freely increase the hard limit. However, no matter what, the soft and hard limits modified by `ulimit` should not exceed the value defined in `/proc/sys/fs/nr_open`.

The changes that the `ulimit` command makes to resource limits are temporary, and they only apply to the current Shell and the processes it creates. For example, when we run the following command to create a sub-shell and modify the maximum number of file descriptors in it, this change will not take effect in the parent Shell:

```
$ (ulimit -n 2000; ulimit -n)
2000
$ ulimit -n
65535
```

Or when we use the `su` command to switch to another user, the system will create a new Shell, which will also cause our changes to become ineffective. In the following example, we list the current Shell's PID to prove that this is a new Shell:

```
$ echo "The current shell's PID is $$"
The current shell's PID is 2083
$ ulimit -n
65535
$ su - emqx
$ echo "The current shell's PID is $$"
The current shell's PID is 7837
$ ulimit -n
32768
```

This is why sometimes we find that the changes made by `ulimit` do not take effect.

Taking EMQX as an example, if we installed it through a software package or package management tool, EMQX would automatically create an `emqx` user during installation and switch to this user at startup. This means that changes we made in the current Shell by running the `ulimit` command as a non-emqx user will be ineffective when EMQX is started with `emqx start` and switched the user. In this case, the resource limits of EMQX are determined directly by `/etc/security/limits.conf`.

For these reasons, we generally recommend modifying `/etc/security/limits.conf` directly.

### /etc/systemd/system.conf

The file `/etc/security/limits.conf` can only set resource limits for users logging in through PAM, it does not affect the resource limits of [system services](https://en.wikipedia.org/wiki/Systemd).

So when we start the EMQX service with `sudo systemctl start emqx` or `sudo service emqx start`, this service will not be affected by the limitations in `/etc/security/limits.conf`.

The maximum number of file descriptors available to system services is determined by the parameter `DefaultLimitNOFILE` in the file `/etc/systemd/system.conf` or the parameter `LimitNOFILE` in the file `/usr/lib/systemd/system/<Service Name>.service`. The former is a global default setting applied to all system services, while the latter is an optional individual limit for each service. `LimitNOFILE` will override `DefaultLimitNOFILE`.

Changes in `/etc/systemd/system.conf` are global and always require a server reboot to take effect. Changes in each service's own unit file can take effect by simply running the command `sudo systemctl daemon-reload` to reload the systemd configuration file. So the latter is our recommended configuration method.

In terms of configuration format, `LimitNOFILE` and DefaultLimitNOFILE are the same. We can set both soft and hard limits at the same time.

`LimitNOFILE` and `DefaultLimitNOFILE` have the same configuration format, using `LimitNOFILE` as an example, we can set both hard and soft limits:

```
LimitNOFILE = <Number>
```

We can also set soft and hard limits separately:

```
LimitNOFILE = <Soft Limit>:<Hard Limit>
```

The currently effective `DefaultLimitNOFILE` can be viewed with the command `systemctl show --property DefaultLimitNOFILE`, and `LimitNOFILE` can be viewed with the command `systemctl show emqx -p LimitNOFILE`. However, both of them can only view hard limits, not soft limits.

EMQX sets `LimitNOFILE` to 1048576 by default in the unit file `/usr/lib/systemd/system/emqx.service`. If we have modified it, we can run the following command to make the changes take effect:

```
systemctl daemon-reload
systemctl restart emqx
```

Note that the LimitNOFILE limit should also not exceed the value defined in `/proc/sys/fs/nr_open`, or the service will fail to start.

## Quick Verification

Suppose now we want EMQX to be able to accept 500,000 client connections, we can configure it like this:

1. Open the `/etc/sysctl.conf`, and add the following two lines:

   ```
   fs.file-max = 520000
   fs.nr_open = 510000
   ```

   Run `sysctl -p` to make the changes take effect.

2. Open the `/etc/security/limits.conf`, and add the following two lines:

   ```
   emqx soft nofile 510000
   emqx hard nofile 510000
   ```

   Log out of the session and log back in to make the changes take effect.

3. Open the EMQX unit file `/usr/lib/systemd/system/emqx.service` and modify the parameter `LimitNOFILE`:

   ```
   LimitNOFILE = 510000
   ```

   Run `systemctl daemon-reload` to make the changes take effect.

4. Start EMQX with `emqx start` or `sudo systemctl emqx start`. After successful startup, use the command `ps aux | grep emqx` to get the PID of the EMQX process. Then, we can check the effective resource limits of the current process with the following command:

   ```
   $ cat /proc/<PID>/limits
   Limit                     Soft Limit           Hard Limit           Units
   ...
   Max open files            510000               510000               files
   ...
   ```

## The maximum connection limit of EMQX

After correctly modifying the above system parameters, the number of connections to EMQX has finally reached our expectations. However, as long as the number of clients continues to increase, it is still possible to exceed our modified limits. 

Since the basic services of EMQX will also request file descriptors, if the client connections have already occupied all available file descriptors, the operating system will return an **EMFILE** error (The per-process limit of open file descriptors has been reached) or an **ENFILE** error (The system limit on the total number of open files has been reached). This will cause EMQX to be unable to continue to operate normally.

Therefore, we recommend enabling the maximum connection limit of EMQX, with EMQX actively restricting the number of connections to ensure that the number of open file descriptors does not exceed the system's resource limit. This restriction mechanism is disabled by default, we need to enable it by ourselves.

Taking EMQX 5.3.0 as an example, we can access the listener page of the Dashboard, then click on the listener name to enter the corresponding configuration page, and change `Max Connections` to a value less than the current system limit:

![01emqxconfiguration.png](https://assets.emqx.com/images/0cd9c928e91a3d62d6f660f3f4968e3f.png)

## Conclusion

In Linux systems, there are quite a few parameters that affect the maximum number of file descriptors we can ultimately use. We can only modify the correct parameters according to different situations after understanding their respective uses and scopes. The following diagram can help us further clarify and memorize their relationship:

![02allparametersen.jpg](https://assets.emqx.com/images/4d36befd96f730763cba2a1035b1964d.jpg)

In subsequent blogs, we will continue to bring more optimization guides for kernel parameters that affect the performance of EMQX on Linux systems.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
