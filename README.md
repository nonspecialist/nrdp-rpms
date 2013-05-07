nrdp-server-rpm
===============

This little repo provides the means to build separate NRDP server and client 
RPMs for use on RHEL-type systems

The client RPM makes use of the `alternatives` system to permit different
implementations of `send_nrpd` to be installed concurrently; the version
supplied by this package is written in PHP, however you might feel about
command-line PHP (I personally think it's a catastrophic abomination) but
that's the "reference implementation" supplied by Nagios Enterprises, LLC.

Using
-----

### With rpmbuild ###

1. Make sure you're on a system that can `rpmbuild` properly
1. Type `make`
1. Copy the resulting SRPM and/or RPM from `${HOME}/rpmbuild/{RPMS,SRPMS}`

### With mock ###

1. Make sure you're on a system that can use `mock` properly
1. Type `make mock`
1. Copy the resulting SRPM and/or RPMs from `${MOCK_ROOT/result}`

License
-------

These scripts are licensed under the GPLv3; the actual code contained
within the NRDP server reference implementation, and the PHP-based
`send_nrdp` client are licensed under the Nagios Open Software License.

