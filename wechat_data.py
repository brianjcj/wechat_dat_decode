import os
import glob
import ctypes

DAT_DIR = "C:/Users/brian/Documents/WeChat Files/brianjcj/FileStorage/MsgAttach"

MY_HASH = 104
SAMPLE_FILE = "C:/Users/brian/Documents/WeChat Files/brianjcj/FileStorage/MsgAttach/2bc8f8e256fc8f293f4c127060a71def/Image/2023-02/3ad5640990150353912432709b2a5deb.dat"  # jpg
# SIMPLE_FILE = "C:/Users/brian/Documents/WeChat Files/brianjcj/FileStorage/MsgAttach/0449459086b236bdee06ec07c71faee4/Image/2023-02/0f5c4798944a48eab8660b208a5516cc.dat"  # png

DATA_FILES = "./wechat_data_files.txt"

# https://gist.github.com/leommoore/f9e57ba2aa4bf197ebc5
# File Magic Numbers

# var bmp = new byte[] { 0x42, 0x4D };               // BMP "BM"
# var gif87a = new byte[] { 0x47, 0x49, 0x46, 0x38, 0x37, 0x61 };     // "GIF87a"
# var gif89a = new byte[] { 0x47, 0x49, 0x46, 0x38, 0x39, 0x61 };     // "GIF89a"
# var png = new byte[] { 0x89, 0x50, 0x4e, 0x47, 0x0D, 0x0A, 0x1A, 0x0A };   // PNG "\x89PNG\x0D\0xA\0x1A\0x0A"
# var tiffI = new byte[] { 0x49, 0x49, 0x2A, 0x00 }; // TIFF II "II\x2A\x00"
# var tiffM = new byte[] { 0x4D, 0x4D, 0x00, 0x2A }; // TIFF MM "MM\x00\x2A"
# var jpeg = new byte[] { 0xFF, 0xD8, 0xFF };        // JPEG JFIF (SOI "\xFF\xD8" and half next marker xFF)
# var jpegEnd = new byte[] { 0xFF, 0xD9 };           // JPEG EOI "\xFF\xD9"

JPEG = bytes([0xFF, 0xD8, 0xFF])
PNG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
BMP = bytes([0x42, 0x4D])
GIF = bytes([0x47, 0x49, 0x46, 0x38, 0x39, 0x61])
GIF_2 = bytes([0x47, 0x49, 0x46, 0x38, 0x37, 0x61])
TIFF = bytes([0x49, 0x49, 0x2A, 0x00])
TIFF_2 = bytes([0x4D, 0x4D, 0x00, 0x2A])


def detect_image_format(buf: bytes):
    if buf.startswith(JPEG):
        return "jpg"
    elif buf.startswith(PNG):
        return "png"
    elif buf.startswith(BMP):
        return "bmp"
    elif buf.startswith(GIF):
        return "gif"
    elif buf.startswith(GIF_2):
        return "gif"
    elif buf.startswith(TIFF):
        return "tiff"
    elif buf.startswith(TIFF_2):
        return "tiff"
    else:
        print("unknown format:", buf)
        return "unknown"


def detect_file_type(file_name):
    with open(file_name, 'rb') as f:
        b = f.read(10)
        return detect_file_type_by_bytes(b)


def detect_file_type_by_bytes(b0):
    hh = MY_HASH
    b = bytearray(b0)
    b = decode_bytes(b, hh)
    format = detect_image_format(b)
    return format


def decode_bytes(b, hh):
    for i in range(0, len(b)):
        b[i] ^= hh
    return b


def get_my_hash(file_name):
    with open(file_name, 'rb') as f:
        b0 = f.read(10)
        for hh in range(0, 0xff):
            b = bytearray(b0)
            b = decode_bytes(b, hh)
            format = detect_image_format(b)
            if format != "unknown":
                print('my hash:', hh)
                return hh
    raise "failed to calc my hash"


def list_files():
    # r = os.listdir(
    #     "C:/Users/brian/Documents/WeChat Files/brianjcj/FileStorage/MsgAttach/")
    # for f in r:
    #     print(f)
    r = glob.glob(
        "C:/Users/brian/Documents/WeChat Files/brianjcj/FileStorage/MsgAttach/**/*.dat", recursive=True)
    print(len(r))
    with open(DATA_FILES, 'w', encoding='utf-8') as f:
        for p in r:
            f.write(p)
            f.write("\n")


def display_head(b):
    hh = MY_HASH
    if True:
        print('-' * 100, hh)
        for c in b:
            c ^= hh
            a = ''
            if chr(c).isascii():
                a = chr(c)
            print("%02x" % c, "%03d" % c, a)


def decode_image_dat(file_name):
    format = ""
    with open(file_name, 'rb') as f:
        print('goooooo----')
        b0 = f.read()
        if format == "":
            format = detect_file_type_by_bytes(b0[0:10])
        b = bytearray(b0)
        hh = MY_HASH
        for i in range(0, len(b)):
            b[i] ^= hh
        out_path = "C:/Users/brian/ooo." + format
        print("output to file:", out_path)
        with open(out_path, "wb") as fw:
            fw.write(b)
        print('done--------')


def check_format():
    info = {}
    with open(DATA_FILES, "r") as f:
        i = 0
        for l in f:
            format = detect_file_type(l.strip())
            if format == "unknown":
                print(l)
            if info.get(format) is None:
                info[format] = 1
            else:
                info[format] += 1
            i += 1
            # if i > 100:
            #     break
    print(info)


def go():
    lib_wechat_dd = ctypes.CDLL("./wechat_dat_decode.dll")
    with open(DATA_FILES, "r") as f:
        c_len = len(DAT_DIR) + 1
        i = 0
        for l in f:
            i += 1
            l = l.strip()
            p = l[c_len:]
            bname = os.path.basename(p)
            dname = os.path.dirname(p)
            bname_stem = os.path.splitext(bname)[0]
            output_dir = f'output/{dname}'
            output_file_path = f'{output_dir}/{bname_stem}'
            # print(f'create dir "{output_dir}" and write to file "{bname_stem}"')

            if not os.path.isdir(output_dir):
                print(f'create dir: {output_dir}')
                os.makedirs(output_dir)

            # call c dll function to convert file. python is too slow for that.
            ret =lib_wechat_dd.decode_wechat_dat_file(
                ctypes.c_char_p(l.encode('utf-8')),
                ctypes.c_char_p(output_file_path.encode('utf-8')),
                MY_HASH)
            # print("call dll ret", ret)
            if ret < 0:
                print(f'failed to decode_wechat_dat_file({l}). ret={ret}')
                break

            # if i > 100:
            #     print('.', end='')
            #     break


def main():
    global MY_HASH
    # list_files()
    # MY_HASH = get_my_hash(SAMPLE_FILE)
    # detect_file_type(SAMPLE_FILE)
    # check_format()
    go()


if __name__ == '__main__':
    main()
