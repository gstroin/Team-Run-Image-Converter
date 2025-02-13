import zipfile

#this is actual for 0.0116 version

def open_zip_file(path: str) -> tuple[str, str, list[str]]:
    with zipfile.ZipFile(path) as compressed_map:
        with compressed_map.open("state.tres") as file:
            tres = file.read().decode().strip('\n')
        with compressed_map.open("map.trmap") as file:
            info = file.readline().decode().strip('\n')
            object_lines = file.read().decode().strip('\n').split('\n')
    return (tres, info, object_lines)
    

def open_txt_file(path: str) -> tuple[str, str, list[str]]:
    tres = "0;0;8,4375"
    with open(path) as file:
        info = file.readline().strip()
        object_lines = file.read().strip('\n').split('\n')
    return (tres, info, object_lines)

def open_file(path: str) -> tuple[str, str, list[str]]:
    if zipfile.is_zipfile(path):
        return open_zip_file(path)
    return open_txt_file(path)

def add_signature(path: str):
    with open(path, 'rb') as file:
        olddata = file.read()
    data = b"\x89TRMap" + olddata
    with open(path, 'wb') as file:
        file.write(data)

def save_map(map_data: tuple[str, str, list[str]], path: str):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as compressed_map:
        map_str = map_data[1] + '\n' + '\n'.join(map_data[2])
        compressed_map.writestr("map.trmap", map_str)
        compressed_map.writestr("state.tres", map_data[0])
    add_signature(path)

def max_id(objects: list[str]) -> int:
    res = 0
    for line in objects:
        data = line.split(';')
        id = int(data[1])
        if id >= res:
            res = id + 1
    return res

def new_map() -> tuple[str, str, list[str]]:
    tres = "0;0;8,4375" #camera size actually depends on device, but whatever
    info = "0;1;1;808080FF;15;;;;;"
    objects = list()
    return (tres, info, objects)
