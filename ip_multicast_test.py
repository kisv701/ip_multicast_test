import socket
import argparse
import select
import struct


def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('--if_addr', type=str, default='0.0.0.0', help='Ip address of interface which we want to join the multicast group on. If 0.0.0.0 (default) the multicast group will be joined on each interface individually.')
  parser.add_argument('--multicast_group', type=str, default='239.0.0.0', help='Multicast group to join. Default is 239.0.0.0.')
  parser.add_argument('--multicast_port', type=int, default=40000, help='Port to bind to multicast group. Default is 40000.')
  parser.add_argument('--print_data', action='store_true', help='If set the payload coming in over IP multicast will be printed as hex payload (e.g DE AD BE EF).')

  args = parser.parse_args()
  return args

def init_socket(group, port, if_addr):

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  # "4s4s" is a format specifier for 2 4-byte strings.
  mreq = struct.pack("4s4s", socket.inet_aton(group), socket.inet_aton(if_addr))
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  sock.bind((if_addr, port))

  return sock


def main():
  RECV_SIZE = 4096
  args = parse_arguments()
  
  join_on_all_interfaces = args.if_addr == '0.0.0.0'
  if_addr = args.if_addr
  
  
  listening_sockets = []

  if join_on_all_interfaces:
    system_if_list = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)
    for interfaces in system_if_list:
      _, _, _, _, (if_addr,_) = interfaces
      sock = init_socket(args.multicast_group, args.multicast_port, if_addr)
      listening_sockets.append(sock)
      print(f'Joining {args.multicast_group}:{args.multicast_port} from interface with ip {if_addr}')
  else:
    sock = init_socket(args.multicast_group, args.multicast_port, args.if_addr)
    listening_sockets.append(sock)
    print(f'Joining {args.multicast_group}:{args.multicast_port} from interface with ip {args.if_addr}')
  
  print(f"Listening...")

  while True:
    readable, _, _  = select.select(listening_sockets, [], [], 1.0)
    for sock in readable:
      ip, port = sock.getsockname()
      data, (sender_addr, sender_port) = sock.recvfrom(RECV_SIZE) 
      print(f"New data ({len(data)}) from: {sender_addr:15} -> {args.multicast_group} -> {ip:15}:{port}")
      if args.print_data:
        print(" ".join([f"{byte:02X}" for byte in data]))

if __name__ == '__main__':
  main()