from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from functools import reduce

# //////////////////// PARSING & TYPES /////////////////////////

class ChunkType(Enum):
    FILE = 1,
    FREE_SPACE = 2

@dataclass
class Block:
    chunk: "Chunk"
    position: int

@dataclass
class Chunk:
    id: int
    type: ChunkType
    blocks: list[Block] = field(default_factory=list)

def parse_input(data: str, part: str) -> list[Chunk]:
    
    chunks: list[Chunk] = []
    
    block_position = 0
    file_id = 0
    for i, num in enumerate(map(int, list(data))):
        chunk_type = ChunkType.FILE if i % 2 == 0 else ChunkType.FREE_SPACE
        chunk = Chunk(file_id, chunk_type)
        chunks.append(chunk)
        
        chunk.blocks = [Block(chunk, i) for i in range(block_position, block_position + num)]
        block_position += num
        
        if i % 2 == 0:
            file_id += 1
        
    return chunks


# //////////////////// PARTS /////////////////////////

def run_a(data: list[Chunk]):
    free_space_chunks = list(filter(lambda c: c.type == ChunkType.FREE_SPACE, data))
    file_chunks = list(filter(lambda c: c.type == ChunkType.FILE, data))
    
    free_space_blocks: list[Block] = reduce(lambda a, b: a + b, list(map(lambda c: c.blocks, free_space_chunks)))
    file_blocks: list[Block] = reduce(lambda a, b: a + b, list(map(lambda c: list(reversed(c.blocks)), list(reversed(file_chunks[1:])))))
    
    free_block_index = 0
    for file_block in file_blocks:
        free_block = free_space_blocks[free_block_index]
        
        if file_block.position < free_block.position:
            continue
        
        pos = free_block.position
        free_block.position = file_block.position
        file_block.position = pos
        
        free_block_index += 1
        
    total = 0
    for file_chunk in file_chunks:
        total += sum(map(lambda b: b.position * file_chunk.id, file_chunk.blocks))
        
    print(f"Total: {total}") 
        

def run_b(data: list[Chunk]):
    free_space_chunks = list(filter(lambda c: c.type == ChunkType.FREE_SPACE, data))
    file_chunks = list(filter(lambda c: c.type == ChunkType.FILE, data))
    
    free_space_map = {}
    for chunk in free_space_chunks:
        if len(chunk.blocks) > 0:
            free_space_map[chunk.blocks[0].position] = len(chunk.blocks)
    
    
    
    reversed_file_chunks = list(reversed(file_chunks[1:]))
    for chunk in reversed_file_chunks:
        
        free_spaces: list[int] = list(free_space_map.keys())
        free_spaces.sort()
        
        for i in free_spaces:
            chunk_length = len(chunk.blocks)
            free_space_length = free_space_map[i]
            
            if i > min(map(lambda b: b.position, chunk.blocks)):
                break
            
            if free_space_length >= chunk_length:
                del free_space_map[i]
                
                if free_space_length - chunk_length > 0:
                    free_space_map[i + chunk_length] = free_space_length - chunk_length
                    
                for bp, block in enumerate(chunk.blocks):
                    block.position = i + bp    
                
                break
        
    total = 0
    for file_chunk in file_chunks:
        total += sum(map(lambda b: b.position * file_chunk.id, file_chunk.blocks))
        
    print(f"Total: {total}") 