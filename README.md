## Assignment - 1 SNS
#### Author - yashdeep.saini@students.iiit.ac.in
#### Topic  - Secure file transfer ( DHKE + Caesar Shift )

* A simple client server model which performs a key exchange
using a simplistic Diffie Hellman and then by using the key
it performs shift cipher on remaining communication.
* Key is temporary to all sessions.
* Code is written in Python

#### Main code

##### Server.py
> Multithreaded server which provides login, register and file download features.

##### Run Server
```
$ ./server.sh
```
##### Client.py
> Client which provides login, register and file download features. It runs a main loop to take user input and provides a mini shell to list and download files on server.

##### Run Client
```
$ ./server.sh [ IP address of server ]
```

#### Extra files

* password.db - Will hold user credentials for backup and loading.
* client.log - maintains a log session for client operations.
* server.log - maintains a log session for server operations.
* crypto.log - maintains a log for all calls to sendSecure and recvSecure
* client.py and server.py - main code.
* uploads/ - This is the directory it creates or checks which will be used to server files.

#### Modules

##### Caesar
> Performs operations related to all shift operations
and provides wrapper for securely send() and write()

* code - automatically detects the type of input and returns code or decoded value.
* ROT - takes k, s, delim which is key, string to shift and delimiter to skip.
* UNROT - takes k, s, delim which is key, string to unshift and delimiter to skip.
* sendSecure - takes a socket, key to call ROT, plaintext and delimiter. Sends encrypted text over this passed socket.
* recvSecure - takes a socket, key to call UNROT, ciphertext and delimiter. Receives encrypted text over this passed socket and returns plaintext.

##### Diffie
> Takes care of initial key change and appropriate calls to prime module

* randomPrime - returns a random prime
* generateAlpha - takes a prime and returns it primitive root
* genPrivateKey - generates a private key from prime and primitive root.
* genKeyDerivation - derives the session key after parameter exchange.
* initKeyExchg - takes a socket and inits key exchange over it.
* performKeyExchg - takes a socket and performs key exchange over it.

##### fileUtils
> provides utility function for file directory viewing.

* directoryList - returns list of files in serving directory

##### messageUtils
> all forms of packet creation is done via this module

* createLoginRequest - Packet for User registration
* createLoginReply - Packet for User registration
* createAuthRequest - Packet for User Authentication
* createAuthReply- Packet for User Authentication
* createServiceRequest - Packet for Service Request
* createServiceDone - Packet for Service Completion
* packMessage - Trivial serialization
* unpackMessage - Trivial unserialization

##### minilogger
> provides extremely basic logging capabilities

* minilogger.writer - append or fresh log file operations

##### passwordDBUtils
> interface to password.db file and in memory structure

* isUserExist - test if user already registered.
* adduserpasswordDB - add user to system
* testauthpasswordDB - during authentication perform hash check
* loadPasswordDB - on start of server loads password.db file in memory
* dumpPasswordDB - flushed passwords on to password.db file on each new entry

##### prime
> module to perform all prime number calculcations

* is_prime - test if prime or not
* generate_prime_number - returns a prime number
* generate_prime_candidate - limits the bound for prime number
* prim_root - calculates primitive root of the prime number provided
