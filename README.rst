About tgldapid
==============

This is an identity provider for the TurboGears web framework to authenticate
users against an LDAP server.

It has been written and tested for TurboGears 1.1, and might (or might not)
work for later versions.

However, the authorization mechanism is left up to the application database
(i.e it doesn't handle groups and permissions itself).

It works only with SQLObject, but an SQLAlchemy provider could be added in the
future.


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
