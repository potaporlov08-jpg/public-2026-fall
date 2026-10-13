import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List


class BlobType(Enum):
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    tree_hash: str
    parents: List[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    children: Dict[str, Blob]


def read_blob(path: Path) -> Blob:
    with open(path, 'rb') as f:
        compressed_data = f.read()
    
    data = zlib.decompress(compressed_data)
    
    null_index = data.index(b'\x00')
    header = data[:null_index]
    content = data[null_index + 1:]
    
    type_bytes, length_bytes = header.split(b' ', 1)
    
    return Blob(type_=BlobType.from_bytes(type_bytes), content=content)


def traverse_objects(obj_dir: Path) -> Dict[str, Blob]:
    blobs = {}
    for dir_path in obj_dir.iterdir():
        if not dir_path.is_dir():
            continue
        
        dir_name = dir_path.name
        for file_path in dir_path.iterdir():
            if not file_path.is_file():
                continue
            
            full_hash = dir_name + file_path.name
            blobs[full_hash] = read_blob(file_path)
            
    return blobs


def parse_commit(blob: Blob) -> Commit:
    assert blob.type_ == BlobType.COMMIT
    
    text = blob.content.decode('utf-8')
    parts = text.split('\n\n', 1)
    header = parts[0]
    message = parts[1] if len(parts) > 1 else ''
    
    tree_hash = ''
    parents = []
    author = ''
    committer = ''
    
    for line in header.split('\n'):
        if line.startswith('tree '):
            tree_hash = line[5:]
        elif line.startswith('parent '):
            parents.append(line[7:])
        elif line.startswith('author '):
            author = line[7:]
        elif line.startswith('committer '):
            committer = line[10:]
            
    return Commit(tree_hash=tree_hash, parents=parents, author=author, committer=committer, message=message)


def parse_tree(blobs: Dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    assert tree_root.type_ == BlobType.TREE
    
    content = tree_root.content
    children = {}
    pos = 0
    
    while pos < len(content):
        null_index = content.index(b'\x00', pos)
        header = content[pos:null_index].decode('utf-8')
        
        mode, name = header.split(' ', 1)
        
        hash_bytes = content[null_index + 1 : null_index + 21]
        hash_hex = hash_bytes.hex()
        
        if hash_hex in blobs:
            children[name] = blobs[hash_hex]
            
        pos = null_index + 21
        
    return Tree(children=children)


def find_initial_commit(blobs: Dict[str, Blob]) -> Commit:
    for blob in blobs.values():
        if blob.type_ == BlobType.COMMIT:
            commit = parse_commit(blob)
            if not commit.parents:
                return commit
    raise ValueError("Initial commit not found")


def search_file(blobs: Dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    tree = parse_tree(blobs, tree_root)
    
    if filename in tree.children:
        return tree.children[filename]
    
    for child in tree.children.values():
        if child.type_ == BlobType.TREE:
            result = search_file(blobs, child, filename)
            if result is not None:
                return result
                
    assert False, f"File {filename} not found in tree"