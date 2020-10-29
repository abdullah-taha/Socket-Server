import unittest
from socket import socket
from server import Server
from unittest.mock import patch
import io
import sys
class Tester(unittest.TestCase):

    def test_socket_creation(self):
        x = Server()
        self.assertIsInstance(x.s,socket)

    def test_socket_binding(self):
        x = Server()
        host = ""
        port = 9998
 
        x.bind_socket(host,port)
        self.assertTrue(x.binded)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_recieve_command(self,mock_stdout):
        #not yet written
        pass


