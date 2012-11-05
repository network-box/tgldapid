This is an identity provider for the TurboGears web framework.

It has been written and tested for TurboGears 1.1, and might (or might not)
work for later versions.

It allows authenticating users against an LDAP server.

However, the authorization mechanism is left up to the application database
(i.e it doesn't handle groups and permissions itself).

It works only with SQLObject, but an SQLAlchemy provider could be added in the
future.

It is released under the MIT license.
