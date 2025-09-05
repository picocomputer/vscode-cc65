#!/usr/bin/env python3
#
# Copyright (c) 2025 Rumbledethumps
#
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-License-Identifier: Unlicense

# Developer tool for RP6502

import os
import re
import time
import serial
import binascii
import argparse
import configparser
import platform
import sys
import select
from typing import Union

try:
    import tty
except:
    pass


class Console:
    """Manages the RP6502 console over a serial connection."""

    DEFAULT_TIMEOUT = 0.5
    UART_BAUDRATE = 115200

    def __init__(self, name: str, timeout: float = DEFAULT_TIMEOUT):
        """Initialize console over serial connection."""
        self.serial = serial.Serial()
        self.serial.setPort(name)
        self.serial.timeout = timeout
        self.serial.baudrate = self.UART_BAUDRATE
        self.serial.open()

    def code_page(self, timeout: float = DEFAULT_TIMEOUT) -> str:
        """Fetch code page to use for for terminal"""
        self.serial.write(bytes("set cp", "ascii"))
        self.serial.write(b"\r")
        self.wait_for_prompt(":", timeout)
        result = self.serial.read_until().decode("ascii")
        return f"cp{re.sub(r"[^0-9]", "", result)}"

    def terminal(self, cp):
        """Dispatch to the correct terminal emulator"""
        if "tty" in globals():
            self.term_posix(cp)
        else:
            self.term_windows(cp)

    def term_posix(self, cp: str):
        """POSIX terminal emulator for Linux, BSD, MacOS, etc."""
        print("Console terminal. CTRL-A then B for break or X for exit.")
        tty.setraw(sys.stdin.fileno())
        ctrl_a_pressed = False
        while True:
            ready, _, _ = select.select([sys.stdin, self.serial], [], [], None)
            if sys.stdin in ready:
                char = sys.stdin.read(1)
                if char:
                    if char == "\x01":  # CTRL-A
                        ctrl_a_pressed = True
                        self.serial.write(char.encode(cp))
                    elif ctrl_a_pressed and char.lower() in "bf":  # f is minicom
                        self.send_break()  # eats prompt
                        sys.stdout.write("\r\n]")  # fake prompt
                        ctrl_a_pressed = False
                    elif ctrl_a_pressed and char.lower() in "xq":  # q is minicom
                        sys.stdout.write("\r\n")
                        os.system("stty sane")
                        break
                    else:
                        ctrl_a_pressed = False
                        self.serial.write(char.encode(cp))
            if self.serial in ready:
                data = self.serial.read(1)
                if len(data) > 0:
                    try:
                        sys.stdout.write(data.decode(cp))
                    except UnicodeDecodeError:
                        sys.stdout.write(f"\\x{data[0]:02x}")
                    sys.stdout.flush()

    def term_windows(self, cp):
        """Windows terminal emulator"""
        # TODO
        pass

    def send_break(self, duration: float = 0.01, retries: int = 1):
        """Stop the 6502 and return to monitor."""
        self.serial.read_all()
        self.serial.send_break(duration)
        try:
            self.wait_for_prompt("]")
            return
        except TimeoutError as te:
            if retries <= 0:
                raise te
        self.send_break(duration, retries - 1)

    def command(self, cmd: str, timeout: float = DEFAULT_TIMEOUT):
        """Send one command and wait for next monitor prompt."""
        self.serial.write(bytes(cmd, "ascii"))
        self.serial.write(b"\r")
        self.wait_for_prompt("]", timeout)

    def reset(self):
        """Start the 6502."""
        self.serial.write(b"RESET\r")
        self.serial.read_until()

    def binary(self, addr: int, data: bytes):
        """Send data to memory using BINARY command."""
        command = f"BINARY ${addr:04X} ${len(data):03X} ${binascii.crc32(data):08X}\r"
        self.serial.write(bytes(command, "utf-8"))
        self.serial.write(data)
        self.wait_for_prompt("]")

    def upload(self, file, name: str):
        """Upload readable file to remote file "name"."""
        self.serial.write(bytes(f"UPLOAD {name}\r", "ascii"))
        self.wait_for_prompt("}")
        file.seek(0)
        while True:
            chunk = file.read(1024)
            if len(chunk) == 0:
                break
            command = f"${len(chunk):03X} ${binascii.crc32(chunk):08X}\r"
            self.serial.write(bytes(command, "ascii"))
            self.serial.write(chunk)
            self.wait_for_prompt("}")
        self.serial.write(b"END\r")
        self.wait_for_prompt("]")

    def send_rom(self, rom):
        """Send rom."""
        addr, data = rom.next_rom_data(0)
        while data is not None:
            self.binary(addr, data)
            addr += len(data)
            addr, data = rom.next_rom_data(addr)

    def wait_for_prompt(self, prompt: str, timeout: float = DEFAULT_TIMEOUT):
        """Wait for a specific prompt from the device."""
        prompt_bytes = bytes(prompt, "ascii")
        start = time.monotonic()
        while True:
            if len(prompt) == 1:
                data = self.serial.read()
            else:
                data = self.serial.read_until()
            if data.startswith(b"?"):
                monitor_result = data.decode("ascii")
                monitor_result += self.serial.read_until().decode("ascii").strip()
                raise RuntimeError(monitor_result)
            if data == prompt_bytes:
                break
            if len(data) == 0:
                if time.monotonic() - start > timeout:
                    raise TimeoutError()


class ROM:
    """Virtual ROM aka The RP6502 ROM."""

    def __init__(self):
        """ROMs begin with up to a screen of help text"""
        """followed by a sparse array of virtual ROM."""
        self.help = []
        self.data = [0 for i in range(0x20000)]
        self.alloc = [0 for i in range(0x20000)]

    def add_help(self, string: str):
        """Add help string."""
        if len(string) > 80:
            raise RuntimeError("Help line > 80 cols")
        self.help.append(string)
        if len(self.help) > 24:
            raise RuntimeError("Help lines > 24 rows")

    def add_binary_data(self, data: bytes, addr: int):
        """Add binary data to ROM."""
        length = len(data)
        self.allocate_rom(addr, length)
        for i in range(length):
            self.data[addr + i] = data[i]

    def add_nmi_vector(self, addr: int):
        """Set NMI vector in $FFFA and $FFFB."""
        if not (0 <= addr <= 0xFFFF):
            raise RuntimeError(f"Invalid NMI vector: ${addr:04X}")
        self.allocate_rom(0xFFFA, 2)
        self.data[0xFFFA] = addr & 0xFF
        self.data[0xFFFB] = addr >> 8

    def add_reset_vector(self, addr: int):
        """Set reset vector in $FFFC and $FFFD."""
        if not (0 <= addr <= 0xFFFF):
            raise RuntimeError(f"Invalid reset vector: ${addr:04X}")
        self.allocate_rom(0xFFFC, 2)
        self.data[0xFFFC] = addr & 0xFF
        self.data[0xFFFD] = addr >> 8

    def add_irq_vector(self, addr: int):
        """Set IRQ vector in $FFFE and $FFFF."""
        if not (0 <= addr <= 0xFFFF):
            raise RuntimeError(f"Invalid IRQ vector: ${addr:04X}")
        self.allocate_rom(0xFFFE, 2)
        self.data[0xFFFE] = addr & 0xFF
        self.data[0xFFFF] = addr >> 8

    def add_binary_file(self, file: str, **addr):
        """Add binary memory data from file. The addr kwargs are: data, nmi, reset, and irq."""
        """Data is where to load the data, the rest are CPU vectors for $FFFA-$FFFF."""
        """Addresses should be an int, None to not provide, or True to read from the file."""
        """Vectors are read from the file in the order listed above."""
        with open(file, "rb") as f:
            data = f.read()
        if addr["data"] is None:
            raise RuntimeError("Address for data is required.")
        if addr["data"] is True:
            if len(data) < 2:
                raise RuntimeError("No data address found in file.")
            addr["data"] = data[0] + data[1] * 256
            data = data[2:]
        if addr["nmi"] is True:
            if len(data) < 2:
                raise RuntimeError("No nmi address found in file.")
            addr["nmi"] = data[0] + data[1] * 256
            data = data[2:]
        if addr["nmi"]:
            self.add_nmi_vector(addr["nmi"])
        if addr["reset"] is True:
            if len(data) < 2:
                raise RuntimeError("No reset address found in file.")
            addr["reset"] = data[0] + data[1] * 256
            data = data[2:]
        if addr["reset"]:
            self.add_reset_vector(addr["reset"])
        if addr["irq"] is True:
            if len(data) < 2:
                raise RuntimeError("No irq address found in file.")
            addr["irq"] = data[0] + data[1] * 256
            data = data[2:]
        if addr["irq"]:
            self.add_irq_vector(addr["irq"])
        self.add_binary_data(data, addr["data"])

    def add_rp6502_file(self, file: str):
        """Add RP6502 ROM data from file."""
        with open(file, "rb") as f:
            # Decode first line as cp850 because binary garbage can
            # raise here before our better message gets to the user.
            command = f.readline().decode("cp850")
            if not re.match(r"^#![Rr][Pp]6502(\r|)\n$", command):
                raise RuntimeError(f"Invalid RP6502 ROM file: {file}")
            while True:
                command = f.readline().decode("ascii").rstrip()
                if len(command) == 0:
                    break
                help_match = re.search(r"^ *(# )", command)
                if help_match:
                    self.add_help(command[help_match.start(1) + 2 :])
                    continue
                if re.search(r"^ *#$", command):
                    self.add_help("")
                    continue
                data_match = re.search(r"^ *([^ ]+) *([^ ]+) *([^ ]+) *$", command)
                if data_match:

                    def str_to_address(addr_str: str) -> int:
                        """Supports $FFFF number format."""
                        if addr_str:
                            addr_str = re.sub(r"^\$", "0x", addr_str)
                        if re.match(r"^(0x|)[0-9A-Fa-f]*$", addr_str):
                            return int(addr_str, 0)
                        else:
                            raise RuntimeError(f"Invalid address: {addr_str}")

                    addr = str_to_address(data_match.group(1))
                    length = str_to_address(data_match.group(2))
                    crc = str_to_address(data_match.group(3))
                    self.allocate_rom(addr, length)
                    data = f.read(length)
                    if len(data) != length or crc != binascii.crc32(data):
                        raise RuntimeError(f"Invalid CRC in block address: ${addr:04X}")
                    for i in range(length):
                        self.data[addr + i] = data[i]
                    continue
                raise RuntimeError(f"Corrupt RP6502 ROM file: {file}")

    def allocate_rom(self, addr: int, length: int):
        """Marks a range of memory as used."""
        if (
            (addr < 0x10000 and addr + length > 0x10000)
            or addr + length > 0x20000
            or addr < 0
            or length < 0
        ):
            raise IndexError(
                f"RP6502 invalid address ${addr:04X} or length ${length:03X}"
            )
        for i in range(length):
            if self.alloc[addr + i]:
                raise MemoryError(f"RP6502 ROM data already exists at ${addr+i:04X}")
            self.alloc[addr + i] = 1

    def has_reset_vector(self) -> bool:
        """Returns true if $FFFC and $FFFD have been set."""
        return bool(self.alloc[0xFFFC] and self.alloc[0xFFFD])

    def next_rom_data(self, addr: int):
        """Find next up-to-1k chunk starting at addr."""
        for addr in range(addr, 0x20000):
            if self.alloc[addr]:
                length = 0
                while self.alloc[addr + length]:
                    length += 1
                    if length == 1024 or addr + length == 0x10000:
                        break
                return addr, bytearray(self.data[addr : addr + length])
        return None, None


def exec_args():
    # Give a hint at where the USB CDC mounts on various OSs
    if platform.system() == "Windows":
        default_device = "COM1"
    elif platform.system() == "Darwin":
        default_device = "/dev/tty.usbmodem"
    elif platform.system() == "Linux":
        default_device = "/dev/ttyACM0"
    else:
        default_device = "/dev/tty"

    # Standard library argument parser
    parser = argparse.ArgumentParser(
        description="Interface with RP6502 RIA console. Manage RP6502 ROM packaging."
    )
    parser.add_argument(
        "command",
        choices=["run", "upload", "create"],
        help="{Run} local RP6502 ROM file by sending to RP6502 RAM. "
        "{Upload} any local files to RP6502 USB storage. "
        "{Create} RP6502 ROM file from a local binary file and additional local ROM files. ",
    )
    parser.add_argument("filename", nargs="*", help="Local filename(s).")
    parser.add_argument("-o", dest="out", metavar="name", help="Output path/filename.")
    parser.add_argument(
        "-a",
        "--address",
        dest="address",
        metavar="addr",
        help="Starting address of data or `file` to read from file.",
    )
    parser.add_argument(
        "-n",
        "--nmi",
        dest="nmi",
        metavar="addr",
        help="NMI vector for $FFFA-$FFFB or `file` to read from file.",
    )
    parser.add_argument(
        "-r",
        "--reset",
        dest="reset",
        metavar="addr",
        help="Reset vector for $FFFC-$FFFD or `file` to read from file.",
    )
    parser.add_argument(
        "-i",
        "--irq",
        dest="irq",
        metavar="addr",
        help="IRQ vector for $FFFE-$FFFF or `file` to read from file.",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        metavar="name",
        help=f"Configuration file for console connection.",
    )
    parser.add_argument(
        "-D",
        "--device",
        dest="device",
        metavar="dev",
        default=default_device,
        help=f"Serial device name. Default={default_device}",
    )
    parser.add_argument(
        "-t",
        "--term",
        dest="term",
        metavar="bool",
        default="True",
        help=f"Enables console terminal on run.",
    )
    args = parser.parse_args()

    # Standard library configuration parser
    if args.config:
        config = configparser.ConfigParser()
        if not os.path.exists(args.config):
            config["RP6502"] = {"device": args.device, "term": args.term}
            config.write(open(args.config, "w"))
        else:
            config.read(args.config)
        if config.has_section("RP6502"):
            args.device = config["RP6502"].get("device", args.device)
            args.term = config["RP6502"].get("term", args.term)

    # Because parser is bad at bool
    if args.term.lower() in ["t", "true"] or (args.term.isdigit() and args.term != "0"):
        args.term = True
    else:
        args.term = False

    # Additional validation and conversion
    def str_to_address(parser, str, errmsg):
        """Supports $FFFF number format."""
        if str:
            str = re.sub("^\\$", "0x", str)
            if re.match("^(0x|)[0-9A-Fa-f]*$", str):
                return eval(str)
            elif str.lower() == "file":
                return True
            else:
                parser.error(f"argument {errmsg}: invalid address: '{str}'")

    args.address = str_to_address(parser, args.address, "-a/--address")
    args.nmi = str_to_address(parser, args.nmi, "-n/--nmi")
    args.reset = str_to_address(parser, args.reset, "-r/--reset")
    args.irq = str_to_address(parser, args.irq, "-i/--irq")

    # python3 rp6502.py run
    if args.command == "run":
        print(f"[{os.path.basename(__file__)}] Loading ROM {args.filename[0]}")
        rom = ROM()
        rom.add_rp6502_file(args.filename[0])
        if args.reset != None:
            rom.add_reset_vector(args.reset)
        print(f"[{os.path.basename(__file__)}] Opening device {args.device}")
        console = Console(args.device)
        console.send_break()
        print(f"[{os.path.basename(__file__)}] Sending ROM")
        console.send_rom(rom)
        if args.term:
            code_page = console.code_page()
        if rom.has_reset_vector():
            console.reset()
        else:
            print(f"[{os.path.basename(__file__)}] No reset vector. Not resetting.")
        if args.term:
            console.terminal(code_page)

    # python3 rp6502.py upload
    if args.command == "upload":
        print(f"[{os.path.basename(__file__)}] Opening device {args.device}")
        console = Console(args.device)
        if len(args.filename) > 0:
            console.send_break()
        for file in args.filename:
            print(f"[{os.path.basename(__file__)}] Uploading {file}")
            with open(file, "rb") as f:
                if len(args.filename) == 1 and args.out != None:
                    dest = args.out
                else:
                    dest = os.path.basename(file)
                console.upload(f, dest)

    # python3 rp6502.py create
    if args.command == "create":
        if args.out == None:
            parser.error(f"argument -o required")
        if args.address == None:
            parser.error(f"argument -a/--address required")
        print(f"[{os.path.basename(__file__)}] Creating {args.out}")
        rom = ROM()
        print(f"[{os.path.basename(__file__)}] Adding binary asset {args.filename[0]}")
        rom.add_binary_file(
            args.filename[0],
            data=args.address,
            nmi=args.nmi,
            reset=args.reset,
            irq=args.irq,
        )
        for file in args.filename[1:]:
            print(f"[{os.path.basename(__file__)}] Adding ROM asset {file}")
            rom.add_rp6502_file(file)
        with open(args.out, "wb+") as file:
            file.write(b"#!RP6502\n")
            for help in rom.help:
                file.write(bytes(f"# {help}\n", "ascii"))
            addr, data = rom.next_rom_data(0)
            while data != None:
                file.write(
                    bytes(
                        f"${addr:04X} ${len(data):03X} ${binascii.crc32(data):08X}\n",
                        "ascii",
                    )
                )
                file.write(data)
                addr += len(data)
                addr, data = rom.next_rom_data(addr)


# This file may be included or run like a program. e.g.
#   import importlib
#   rp6502 = importlib.import_module("tools.rp6502")
if __name__ == "__main__":
    # VSCode SIGKILLs the terminal in raw mode, reset to cooked mode
    if platform.system() == "Windows":
        pass  # TODO if needed
    else:
        os.system("stty sane")
    exec_args()
