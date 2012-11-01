from sqlobject import classregistry, SQLObjectNotFound

from turbogears.config import get as getconfig
from turbogears.identity.soprovider import SqlObjectIdentityProvider

import ldap


class LdapSqlObjectIdentityProvider(SqlObjectIdentityProvider):
    """IdentityProvider that uses LDAP for authentication."""

    def __init__(self):
        super(LdapSqlObjectIdentityProvider, self).__init__()

        self.ldap = ("%s://%s:%s"
                     % (getconfig("identity.soldapprovider.protocol", "ldap"),
                        getconfig("identity.soldapprovider.host", "localhost"),
                        getconfig("identity.soldapprovider.port", 389)))
        self.cacert = getconfig("identity.soldapprovider.cacertfile", None)
        self.basedn  = getconfig("identity.soldapprovider.basedn",
                                 "dc=localhost")
        self.filter_id  = getconfig("identity.soldapprovider.filter_id", "uid")
        self.autocreate = getconfig("identity.soldapprovider.autocreate",
                                    False)

        userclass_path = getconfig('identity.soprovider.model.user')
        self.userclass_name = userclass_path.split(".")[-1]

    def validate_identity(self, user_name, password, visit_key):
        """Validate the identity represented by user_name using the password.

        The `visit_key` parameter is completely ignored, but that's how the
        TurboGears API is supposed to be.
        """
        if self.autocreate:
            # Try creating the user if it doesn't exist in the database
            # This is useful to automatically populate the application DB with
            # the users from the LDAP, the first time they try logging in.
            user_class = classregistry.findClass(self.userclass_name)

            try:
                user = user_class.by_user_name(user_name)

            except SQLObjectNotFound as e:
                # Set an empty password, it doesn't matter anyway as it is
                # checked from LDAP, not the application DB
                user = user_class(user_name=user_name, password='')

        return super(self.__class__, self).validate_identity(user_name,
                                                             password,
                                                             visit_key)

    def validate_password(self, user, user_name, password):
        """Validates user_name and password against an AD domain.

        The `user` parameter is completely ignored, but that's how TG expects
        the API to be.
        """
        if self.cacert:
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.cacert)

        ldapcon = ldap.initialize(self.ldap)
        filter = "(%s=%s)" % (self.filter_id, user_name)
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
