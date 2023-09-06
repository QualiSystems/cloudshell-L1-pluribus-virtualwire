from __future__ import annotations


class MappingHelpers:
    @staticmethod
    def parse_ports(ports: str) -> list[str]:
        port_list: list[str] = []
        for record in ports.split(","):
            if "-" in record:
                start, end = map(int, record.split("-"))
                range_list = list(map(str, range(start, end + 1)))
            else:
                range_list = [record]
            port_list.extend(range_list)
        return port_list
