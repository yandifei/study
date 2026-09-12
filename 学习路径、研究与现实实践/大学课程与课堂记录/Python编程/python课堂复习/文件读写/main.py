# f = open("test.txt", "w+", encoding="utf-8")
# f.write("11")
# f.seek(0)
# print(f.read())
# f.close()
#
# pic_f = open(r"D:\PS分辨率.png", "rb")
# print(repr(pic_f.read()))
# pic_f.close()


import pathlib
path = pathlib.Path("test.txt")
new_dir_path = pathlib.Path("./project_files/assets/images")
new_dir_path.mkdir(parents=True, exist_ok=True)
