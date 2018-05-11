import sys, socket

hostname = socket.gethostname()
result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
print([x[4][0] for x in result][-1])
