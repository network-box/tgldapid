import logging

from sqlobject import classregistry, SQLObjectNotFound

from turbogears.config import get as getconfig
from turbogears.identity.soprovider import (SqlObjectIdentity,
                                            SqlObjectIdentityProvider)

import ldap


log = logging.getLogger('turbogears.identity.soprovider')


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
        self.filter = ("(%s=%s)"
                       % (getconfig("identity.soldapprovider.filter_id", "uid"),
                          "%s")
        self.autocreate = getconfig("identity.soldapprovider.autocreate",
                                    False)

        userclass_path = getconfig('identity.soprovider.model.user')
        self.userclass_name = userclass_path.split(".")[-1]

    def __get_ldap_connection(self):
        """Initialize the connection to the LDAP server."""
        if self.cacert:
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.cacert)

        return ldap.initialize(self.ldap)

    def __get_ldap_user_record(self, user_name):
        """Return the record representing the user in LDAP.

        If no user exist in LDAP with this `user_name`, return `None`.
        """
        ldapcon = self.__get_ldap_connection()
        rc = ldapcon.search(self.basedn, ldap.SCOPE_SUBTREE,
                            self.filter % user_name)
        objects = ldapcon.result(rc)[1]

        if(len(objects) == 0):
            log.warning("No such LDAP user: %s" % user_name)
            return None
        elif(len(objects) > 1):
            log.error("Too many users: %s" % user_name)
            return None

        return objects[0]

    def __ensure_user_in_database(self, user_name):
        """Make sure the user exists in the application DB

        If needed, autocreate it. This is useful to automatically populate the
        application DB with users from the LDAP, the first time they try to
        log in.
        """
        user_class = classregistry.findClass(self.userclass_name)

        try:
            user = user_class.by_user_name(user_name)

        except SQLObjectNotFound:
            if self.autocreate:
                # Set an empty password, it doesn't matter anyway as it is
                # checked from LDAP, not from the application DB
                user = user_class(user_name=user_name, password='')

            else:
                log.warning("No such user: %s", user_name)
                return None

    def validate_identity(self, user_name, password, visit_key):
        """Validate the identity."""
        # Make sure the user exists in the LDAP...
        user_record = self.__get_ldap_user_record(user_name)
        if not user_record:
            return None

        # ... and in the application DB
        if not self.__ensure_user_in_database(user_name):
            return None

        if not self.validate_password(user_record, user_name, password):
            log.info("Passwords don't match for user: %s", user_name)
            return None

        log.info("Associating user (%s) with visit (%s)", user_name, visit_key)
        return SqlObjectIdentity(visit_key, user)

    def validate_password(self, user, user_name, password):
        """Validates user_name and password against an AD domain.

        The `user` parameter is **not** an instance of the user model class,
        as would normally be the case in TurboGears identity providers.

        Instead, it is an LDAP record representing the user.

        The `user_name` parameter is completely ignored, but that's how TG
        expects the API to be.
        """
        dn = user[0]

        try:
            ldapcon = self.__get_ldap_connection()
            rc = ldapcon.simple_bind(dn, password)
            ldapcon.result(rc)
        except ldap.INVALID_CREDENTIALS:
            return False

	return True
