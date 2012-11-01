from turbogears.config import get as getconfig
from turbogears.identity.soprovider import SqlObjectIdentityProvider

import ldap


class SoLdapIdentityProvider(SqlObjectIdentityProvider):
    """IdentityProvider that uses LDAP for authentication."""

    def __init__(self):
        super(SoLdapIdentityProvider, self).__init__()

        self.host = getconfig("identity.soldapprovider.host", "localhost")
        self.port = getconfig("identity.soldapprovider.port", 389)
        self.basedn  = getconfig("identity.soldapprovider.basedn",
                                 "dc=localhost")
        self.autocreate = getconfig("identity.soldapprovider.autocreate",
                                    False)

    def validate_password(self, user, user_name, password):
        """Validates user_name and password against an AD domain."""
        ldapcon = ldap.open(self.host, self.port)
        filter = "(sAMAccountName=%s)" % user_name
        rc = ldapcon.search(self.basedn, ldap.SCOPE_SUBTREE, filter)
                            
        objects = ldapcon.result(rc)[1]

        if(len(objects) == 0):
            log.warning("No such LDAP user: %s" % user_name)
            return False
        elif(len(objects) > 1):
            log.error("Too many users: %s" % user_name)
            return False

        dn = objects[0][0]

        try:
            rc = ldapcon.simple_bind(dn, password)
            ldapcon.result(rc)
        except ldap.INVALID_CREDENTIALS:
            log.error("Invalid password supplied for %s" % user_name)
            return False

	return True
