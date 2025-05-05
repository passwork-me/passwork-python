#!/usr/bin/env python3
from abc import ABC, abstractmethod

class PassworkCommand(ABC):
    """
    Abstract base class for Passwork CLI command strategies.
    """
    @abstractmethod
    def execute(self, client, args):
        """
        Execute the command strategy.
        
        Args:
            client (PassworkClient): Initialized Passwork client
            args (Namespace): Command line arguments
            
        Returns:
            int: Exit code
        """
        pass 