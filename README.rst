==============
Stormlock
==============

|status| |version|

.. |status| image:: https://github.com/tmccombs/stormlock/workflows/Main/badge.svg
    :alt: Build Status
    :target: https://github.com/tmccombs/stormlock/actions
.. |version| image:: https://img.shields.io/pypi/v/stormlock
    :alt: Version

.. note:: Stormlock is beta quality and not ready for production use.

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

Concepts
--------

resource
    A unique resource that is protected by a lock. The resource name is used as the key for storing
    the lock in the backend.
principal
    Who is holding the lock. When a lock is held, an identifier for the principal is stored in the 
    backend so that it is easy to see who currently has the lock.
backend
    Some form of database which stores the state of the lock. Multiple backends are supported, and
    it is possible to implement your own plugin to support additional backends.
ttl
    Time to live. How long a lease on a lock should live before expiring. Renewing a lease sets
    a new time to live.
lease
    A handle on an actively held lock. You hold the lock for a resource from the time you acquire 
    a lease to the time you release it, or the lease expires. Only one lease can exist for a 
    resource at a time.
lease id
    A unique, opaque identifier for a lease. This id is needed to perform operations on a lease,
    such as releasing it and renewing it. This id helps ensure multiple leases are not held
    for the same resource at the same time.

Configuration
-------------

By default, `stormlock` searches for a configuration file in the following locations (in order):

#. `.stormlock.cfg` in the current directory
#. `$XDG_CONFIG_HOME/stormlock.cfg` (with a default of `XDG_CONFIG_HOME=$HOME/.config`)
#. `$HOME/.stormlock.cfg`

The configuration file is an INI-style config file that looks like this:

.. code-block:: ini

    # Default section is used for default configuration for locks.
    # If a configuration isn't specified in a more specific section it falls back
    # to values in here.
    [default]
    # ttl is the maximum time a lock can be held without renewing
    ttl = 1 days
    # principal is an identifier of who is holding the lock
    principal = me@example.com
    # specify which backend to use
    backend = etcd

    # Specify configuration for a specific lock
    [special]
    ttl = 30 minutes
    backend = redis

    # Backend sections have configuration specific to the backend
    [backend.etcd]
    host = etcd.example.com

    [backend.redis]
    url = redis://example.com:6379

Usage
-----

The `stormlock` command can be used to operate on locks using the configuration described above.

The supported operations are:

stormlock acquire [--ttl=\ *TTL*\ ] *RESOURCE*
    Attempt to acquire a lease on *RESOURCE*. If successful prints the lease id. Otherwise exit
    with an error code.
stormlock release *RESOURCE* *LEASE_ID*
    Release the given lease for the given resource. The lease id should be ther result of calling
    ``stormlock acquire``.
stormlock renew [--ttl=\ *TTL*\ ] *RESOURCE* *LEASE_ID*
    Attempt to renew the given lease on the given resource. If the lease is no longer the
    active lease for the resource, returns an error code.
stormlock current [--id-only] *RESOURCE*
    Retrieve information about the current lease on a resource, if any. 

    If a lease is active returns a line containing the principal, time the lease was created,
    and the lase id seperated by tabs.  If ``--id-only`` is passed, only the lease id is printed.

    If no lease is active an error message is printed and an error code is returned.
stormlock is-held *RESOURCE* *LEASE_ID*
    Test if a lease is currently active. Returns a 0 status code if it is, otherwise returns a 
    non-zero status code.

A specific configuration file can be specified by either supplying a file with the ``-c`` or
``--config`` options, or with the ``STORMLOCK_CONFIG`` environment variable.

Backends
--------

The currently supported backends are:

* Etcd
    * Renewing a lock always uses the same TTL as the original acquisition
* Redis
* DynamoDB
* PostgreSQL

It's also possible to implement your own backend by implementing the ``stormlock.Backend`` interface and registering the class in the
``stormlock.backends`` entry point in python.
