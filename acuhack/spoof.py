import logging
import socket
from ipaddress import IPv4Interface
from asyncio.subprocess import create_subprocess_exec, PIPE, STDOUT

from psutil import net_if_addrs

logger = logging.getLogger(__name__)


async def spoof(interface_name):
    addrs = net_if_addrs()[interface_name]
    ip4addr = [addr for addr in addrs if addr.family == socket.AF_INET][0]
    interface = IPv4Interface(ip4addr.address + '/' + ip4addr.netmask)
    acuhub = interface.ip + 1

    dnsmasq = await create_subprocess_exec(
        'dnsmasq', '--log-facility=-', '--keep-in-foreground', '--log-queries', '--log-dhcp',
        '--address', f'/#/{interface.ip}',
        '--interface', 'eth0',
        '--dhcp-range', f'{acuhub},{acuhub}', stdout=PIPE, stderr=STDOUT)
    async for line in dnsmasq.stdout:
        logger.info(line.decode().strip())
