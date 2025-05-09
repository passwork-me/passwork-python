from .modules.item import Item
from .modules.vault import Vault
from .modules.inbox import Inbox
from .modules.user import User
from .modules.shortcut import Shortcut
from .modules.api_client import ApiClient
from .modules.master_key import MasterKeyManager
from .modules.session import SessionManager
from .modules.link import Link
from .modules.batch import Batch
from .exceptions import PassworkError
import urllib3
from urllib3.exceptions import InsecureRequestWarning

class PassworkClient(ApiClient, MasterKeyManager, SessionManager, Item, Vault, Inbox, User, Shortcut, Link, Batch):
    """
    A client for interacting with the Passwork API.
    """
    def __init__(self, host: str, verify_ssl: bool = True, auto_refresh: bool = False):
        if not host:
            raise PassworkError("Host must be specified", "host_not_specified")

        # Initialize ApiClient variables
        self.host = host.rstrip('/')  # Ensure no trailing slash
        self.verify_ssl = verify_ssl
        
        # Disable SSL warnings only if verify_ssl is explicitly set to False
        if not self.verify_ssl:
            urllib3.disable_warnings(InsecureRequestWarning)
            
        self.access_token = None
        self.refresh_token = None
        self.master_key_hash = None
        self.auto_refresh = auto_refresh
        
        # Initialize MasterKeyManager variables
        self.master_key = None
        self.user_private_key = None
        self.user_public_key = None
        self.mk_options = None
        self.is_encrypt = False
        
        # Initialize SessionManager variables
        self.session_path = None
        self.session_encryption_key = None 