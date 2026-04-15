
import xmltodict
import json
import os


# Read the XML file using xmltodict
xml_file = r'file_path\HK_medicine.xml'  # Update this path to your XML file
with open(xml_file, 'r', encoding='utf-8') as f:
    xml_content = f.read()

# Parse XML to dict
data_dict = xmltodict.parse(xml_content)

# Auto-detect top-level tag
top_keys = list(data_dict.keys())
print(f'Top-level keys: {top_keys}')
root_key = top_keys[0]
root = data_dict[root_key]

# Based on your attached sample, the list of entries lives under something like
# root['contents']['pcm'] or directly under root['pcm']. We'll try common patterns.
candidates = []
if isinstance(root, dict):
    candidates.extend(list(root.keys()))
    if 'contents' in root and isinstance(root['contents'], dict):
        candidates.extend(list(root['contents'].keys()))

# Try to find the pcm/list key (commonly 'pcm', 'item', 'items', 'record')
list_key = None
for k in ('pcm', 'item', 'items', 'record', 'entry', 'pcms'):
    if k in root:
        list_key = k
        parent = root
        break
    if 'contents' in root and isinstance(root['contents'], dict) and k in root['contents']:
        list_key = k
        parent = root['contents']
        break

if list_key is None:
    # Fall back to first candidate that looks like a list
    for k in candidates:
        candidate = root.get(k) if isinstance(root, dict) else None
        if isinstance(candidate, list) or isinstance(candidate, dict):
            list_key = k
            parent = root
            break

if list_key is None:
    raise KeyError(f"Couldn't find list of entries under root '{root_key}'. Available keys: {candidates}")

print(f"Using list key: {list_key}")

items_raw = parent[list_key]

# Normalize to list
if isinstance(items_raw, list):
    items = items_raw
elif isinstance(items_raw, dict):
    items = [items_raw]
else:
    raise TypeError('Unexpected type for items: ' + str(type(items_raw)))


def normalize_item(obj):
    """Convert xmltodict-style objects by promoting attributes (keys starting with '@')
    and '#text' into normal keys, and keep nested dicts as-is."""
    if not isinstance(obj, dict):
        return obj
    out = {}
    for k, v in obj.items():
        if k.startswith('@'):
            out[k[1:]] = v
        elif k == '#text':
            out['text'] = v
        else:
            # recursively normalize lists/dicts
            if isinstance(v, list):
                out[k] = [normalize_item(i) for i in v]
            elif isinstance(v, dict):
                out[k] = normalize_item(v)
            else:
                out[k] = v
    return out

# Build the output list
extracted = [normalize_item(it) for it in items]

# Ensure output folder and write file
out_path = os.path.join(os.path.dirname(xml_file), 'HK_medicine.json')
with open(out_path, 'w', encoding='utf-8') as out_f:
    json.dump({root_key: {'contents': {list_key: extracted}}}, out_f, ensure_ascii=False, indent=2)

print(f'Wrote {len(extracted)} entries to {out_path}')
