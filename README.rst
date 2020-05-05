==============
Stormlock
==============

.. note:: Stormlock is a work in progress and not ready for production use.
  Also documentation is mostly missing at this point.

Stormlock is a simple centralized locking system primarily intended for human operators (although it may also be useful in some
simple scripting scenarios).

The basic idea is that you acquire a lock by running a command, which gives you a "lease id". That lease id can then be used to
release the lock, or extend its duration. All locks are given a duration after which they are automatically released. The lock is
stored in  a backend, which is generally some kind of database.

The intended use case is where you have some kind of operation which happens somewhat infrequently across a distributed system,
and you want to ensure multiple operators don't perform the operation at the same time. For example, this could be used to make sure
to prevent simultaneous attempts to apply infrastructure-as-code changes, database patches, etc. to the same system by different
operators.

This is **not** intended as a general purpose lock. It is designed with the assumption that locks can be held for a long time without
problems (hours or even days), and that the TTL for the lock doesn't need granularity better than a second. Furthermore, the availability
of the lock is a function of the availability of the backend it uses.

Backends
--------

The currently supported backends are:

* Etcd
    - Renewing a lock always uses the same TTL as the original acquisition
* Redis
* DynamoDB
* PostgreSQL

It's also possible to implement your own backend by implementing the ``stormlock.Backend`` interface and registering the class in the
``stormlock.backends`` entry point in python.
