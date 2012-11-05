About tgldapid
==============

This is an identity provider for the TurboGears web framework to authenticate
users against an LDAP server.

However, the authorization mechanism is left up to the application database
(i.e it doesn't handle groups and permissions itself).

It works only with SQLObject, but an SQLAlchemy provider could be added in the
future.


Install
=======

To use this software, you need:

    - TurboGears == 1.1
      It has only been tested with this version but could probably work or be
      made to work with other versions. Feedback and/or patches are warmly
      welcome.
    - Python == 2.6
      This is the version on EL 6 where I'm developing/testing/running this
      code, but again, it would most likely work fine with other versions.
      Feedback and/or patches will also be gladly taken.

Installing this plugin from the sources should be as simple as running one
command, as root::

    # python setup.py install


Usage
=====

To have your TurboGears application authenticate against your LDAP server
through this identity provider, you will need to set a few options in your
configuration file::

    [global]

    identity.provider = 'soldapprovider'
    identity.soldapprovider.host = 'ldap.acme-corp.com'
    identity.soldapprovider.basedn = 'ou=people,dc=acme-corp,dc=com'
    identity.soldapprovider.filter_id = 'uid'

This will let your application match the user logins to the ``uid`` field of
users in your LDAP at ``ldap.acme-corp.com``, using the provided ``basedn``.

There a few more options available, though. The first one allows connecting to
the LDAP server through a secure SSL connection::

    # Don't use the default `ldap` protocol
    identity.soldapprovider.protocol = 'ldaps'

It is also possible to connect to a different port::

    # Don't use the default `389` port
    identity.soldapprovider.port = 636

If your SSL certificate is self-signed, you might want to specify what CA
certificate to use to verify it::

    identity.soldapprovider.cacertfile = '/etc/pki/tls/certs/my-ca.crt'

Finally, even though the user exists in the LDAP, it **must** also exist in
the application database, so it can be associated to groups, permissions and
visits: tgldapid does **not** handle that at all, it inherits from the
``SqlObjectIdentityProvider`` class and delegates to it for these parts.

However, you might decide that you trust your LDAP records and every user
existing there should also exist in the application database. The following
option will let tgldapid automatically create new users in the application
database **if they exist in the LDAP** on their first login::

    identity.soldapprovider.autocreate = True


Legal
=====

This project is distributed under the terms of the `MIT License`_.

It was written as part of my work at `Network Box`_ as we needed it for our
own products.

We do not require you to assign your copyright or sign a legal document of any
kind before accepting your contributions to this project, so send us patches!

To give credit where credit is due, this project was started from the code
published as `an authentication recipe`_ in the TurboGears documentation.

Unfortunately, there is no licensing information on that recipe. The
TurboGears community usually release their stuff under the MIT license (as is
the case of TurboGears itself), which is also the license I've chosen for
tgldapid.

Hopefully, this won't cause any problem. If you are the original author,
please let me know whether you're ok with this. At the very least, I would
like to give you credit for your work. :)

. _MIT License: http://opensource.org/licenses/MIT

. _Network Box: http://www.network-box.com

. _authentication recipe: http://turbogears.org/1.0/docs/Identity/Recipes.html#authenticate-against-an-ldap-server-updated
