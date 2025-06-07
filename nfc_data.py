def parse_nfc(data_blocks):
    """Parse raw NFC data blocks including header and NDEF records.
    Accepts a list of bytearrays or bytes, returns a dictionary with raw data, header, and TLVs."""
    # Filter out empty and all-null blocks
    safe_blocks = [bytes(b) for b in data_blocks if isinstance(b, (bytes, bytearray)) and any(b)]
    if not safe_blocks:
        return {'raw_data': b'', 'header': None, 'tlvs': []}
    data = b''.join(safe_blocks)
    if not data or not any(data):
        return {'raw_data': b'', 'header': None, 'tlvs': []}
    result = {'raw_data': data}
    # NFC Forum Type 2 Tag header is typically 16 bytes
    if len(data) >= 16:
        header = {
            'magic_number': data[0],
            'version': data[1],
            'memory_size': data[2],
            'access_conditions': data[3],
            'uid': data[4:7],
            'internal': data[7],
            'lock_bytes': data[8:10],
            'cc_bytes': data[12:16],
        }
        result['header'] = header
        tlv_start = 16
    else:
        result['header'] = None
        tlv_start = 0
    tlvs, i = [], tlv_start
    while i < len(data):
        tag = data[i]
        if tag == 0x00: i += 1; continue  # Padding
        if tag == 0xFE: break  # Terminator
        if i + 1 >= len(data): break
        length = data[i+1]
        if length == 0 or i + 2 + length > len(data):
            i += 2 + length
            continue
        value = data[i+2:i+2+length]
        # Only parse NDEF (type 3) messages
        if tag == 0x03 and len(value) > 0:
            # Parse multiple NDEF records from the value, following NFC Forum NDEF spec
            j = 0
            while j < len(value):
                if j + 2 > len(value):
                    break
                header = value[j]
                type_len = value[j+1]
                sr = (header & 0x10) != 0  # Short Record flag
                il = (header & 0x08) != 0  # ID Length flag
                tnf = header & 0x07
                k = j + 2
                # Payload length
                if sr:
                    if k >= len(value): break
                    payload_len = value[k]
                    k += 1
                else:
                    if k + 4 > len(value): break
                    payload_len = (value[k] << 24) | (value[k+1] << 16) | (value[k+2] << 8) | value[k+3]
                    k += 4
                # ID length
                if il:
                    if k >= len(value): break
                    id_len = value[k]
                    k += 1
                else:
                    id_len = 0
                # Type
                if k + type_len > len(value): break
                type_bytes = value[k:k+type_len]
                k += type_len
                # ID
                if id_len:
                    if k + id_len > len(value): break
                    id_bytes = value[k:k+id_len]
                    k += id_len
                else:
                    id_bytes = b''
                # Payload
                if k + payload_len > len(value): break
                payload_bytes = value[k:k+payload_len]
                k += payload_len
                # Decode for display
                try:
                    type_str = type_bytes.decode('utf-8', 'replace')
                except:
                    type_str = str(type_bytes)
                try:
                    payload_str = payload_bytes.decode('utf-8', 'replace')
                except:
                    payload_str = str(payload_bytes)
                try:
                    id_str = id_bytes.decode('utf-8', 'replace') if id_bytes else None
                except:
                    id_str = str(id_bytes)
                tlvs.append({'tag': tag, 'tnf': tnf, 'type': type_str, 'id': id_str, 'payload': payload_str})
                j = k
        else:
            tlvs.append({'tag': tag, 'length': length, 'raw': value})
        i += 2 + length
    result['tlvs'] = tlvs
    return result

def print_data(data):
    """Pretty print the data in a JSON-like format (MicroPython compatible)"""
    def pretty(d, indent=0):
        sp = '  ' * indent
        if isinstance(d, dict):
            s = '{\n'
            for k, v in d.items():
                s += sp + '  ' + repr(k) + ': ' + pretty(v, indent+1) + ',\n'
            s += sp + '}'
            return s
        elif isinstance(d, list):
            s = '[\n'
            for v in d:
                s += sp + '  ' + pretty(v, indent+1) + ',\n'
            s += sp + ']'
            return s
        else:
            return repr(d)
    print(pretty(data))

def read_nfc_raw(dev, tmot):
    """Accepts a device and a timeout in millisecs. Reads data blocks once and returns them."""
    uid = dev.read_passive_target(timeout=tmot)
    data_blocks = []
    if uid is None:
        return None
    else:
        for i in range(0, 512, 4):
            response = dev.mifare_classic_read_block(i)
            if (isinstance(response, bytearray) and all(b == 0 for b in response)) or response is None:
                break
            data_blocks.append(response)
        return data_blocks

def read_nfc_raw_dummy():
    """Returns a hardcoded list of bytearrays simulating NFC data blocks for testing."""
    return (
        bytearray(b'\x04\xb5:\x03\x9eOa\x800H\x00\x00\xe1\x10>\x00'),
        bytearray(b'\x03*\x91\x01\x16T\x02enSPOOL:1'),
        bytearray(b'5\nFILAMENT:5R\n\x03t'),
        bytearray(b'ext/plainHi!\xfe\x00\x00\x00')
    )

def find_spool_filament(data):
    """Search TLVs for a payload containing 'SPOOL:<num>\nFILAMENT:<num>' and return the numbers."""
    tlvs = data.get('tlvs', [])
    for tlv in tlvs:
        payload = tlv.get('payload', '')
        idx1 = payload.find('SPOOL:')
        if idx1 >= 0:
            idx2 = payload.find('\nFILAMENT:', idx1)
            if idx2 > idx1:
                spool_id = payload[idx1+6:idx2].strip()
                idx3 = idx2 + len('\nFILAMENT:')
                idx4 = payload.find('\n', idx3)
                if idx4 == -1:
                    filament_id = payload[idx3:].strip()
                else:
                    filament_id = payload[idx3:idx4].strip()
                if spool_id.isdigit() and filament_id.isdigit():
                    return int(spool_id), int(filament_id)
                else:
                    return spool_id, filament_id
    return None