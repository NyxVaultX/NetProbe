#!/usr/bin/env ruby
require 'socket'
require 'open3'
require 'rbconfig'

# Get MAC address using ARP
def get_mac(ip)
  output, _ = Open3.capture2("arp -a #{ip}")
  line = output.lines.find { |l| l.include?(ip) }
  return "N/A" unless line

  if /(([0-9a-f]{2}-){5}[0-9a-f]{2})/i =~ line
    return $1
  else
    return "N/A"
  end
end

# Get local IPv4 address
def local_ipv4
  Socket.ip_address_list.detect(&:ipv4_private?)&.ip_address
end

# Ping the IP address (platform dependent)
def ping?(ip)
  if RbConfig::CONFIG['host_os'] =~ /mswin|mingw/
    system("ping -n 1 -w 100 #{ip} >nul 2>&1")
  else
    system("ping -c 1 -W 1 #{ip} > /dev/null 2>&1")
  end
end

# Scan local /24 subnet
def scan_network(base_ip)
  subnet = base_ip.split('.')[0..2].join('.')

  # Print CSV header
  puts "IP,MAC,Port,Protocol,IPV4,IPV6,Location"

  (1..254).each do |i|
    ip = "#{subnet}.#{i}"
    next unless ping?(ip)

    mac = get_mac(ip)
    port = 80
    protocol = "TCP"
    ipv4 = ip
    ipv6 = ""
    location = ""

    puts "#{ip},#{mac},#{port},#{protocol},#{ipv4},#{ipv6},#{location}"
  end
end

# Start scanning
if (local_ip = local_ipv4)
  scan_network(local_ip)
else
  warn "Could not determine local IP address."
end
