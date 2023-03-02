#include <stdio.h>

// https://www.bilibili.com/read/cv13076769?from=search

const unsigned char JPEG[] = {0xFF, 0xD8, 0xFF};
const unsigned char PNG[] = {0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A};
const unsigned char BMP[] = {0x42, 0x4D};
const unsigned char GIF[] = {0x47, 0x49, 0x46, 0x38, 0x39, 0x61};
const unsigned char GIF_2[] = {0x47, 0x49, 0x46, 0x38, 0x37, 0x61};
const unsigned char TIFF[] = {0x49, 0x49, 0x2A, 0x00};
const unsigned char TIFF_2[] = {0x4D, 0x4D, 0x00, 0x2A};

const char *detect_format(const char *buf)
{
	if (memcmp(JPEG, buf, sizeof(JPEG)) == 0)
	{
		return "jpg";
	}
	if (memcmp(PNG, buf, sizeof(PNG)) == 0)
	{
		return "png";
	}
	if (memcmp(BMP, buf, sizeof(BMP)) == 0)
	{
		return "bmp";
	}
	if (memcmp(GIF, buf, sizeof(GIF)) == 0)
	{
		return "gif";
	}
	if (memcmp(GIF_2, buf, sizeof(GIF_2)) == 0)
	{
		return "gif";
	}
	if (memcmp(TIFF, buf, sizeof(TIFF)) == 0)
	{
		return "tiff";
	}
	if (memcmp(TIFF_2, buf, sizeof(TIFF_2)) == 0)
	{
		return "tiff";
	}

	return "unknown";
}

// https://stackoverflow.com/questions/69066922/accessing-dll-function-using-ctypes
// cl.exe /D_USRDL /D_WINDLL main.c /MT /link /DLL /OUT:wechat_dat_decode.dll /MACHINE:X86

__declspec(dllexport) int decode_wechat_dat_file(const char *data_file, const char *to_file, unsigned char hash);

__declspec(dllexport) int decode_wechat_dat_file(const char *data_file, const char *to_file, unsigned char hash)
{
	printf("decode_wechat_dat_file '%s'\n", data_file);

	FILE *f = fopen(data_file, "rb");
	if (f == NULL)
	{
		printf("failed to open dat file");
		return -1;
	}
	FILE *f_out = NULL;

	unsigned char buf[1024 * 64];

	size_t total_size = 0;
	while (1)
	{
		size_t n = fread(buf, 1, sizeof(buf), f);
		// printf("read %zd bytes\n", n);

		if (n <= 0)
			break;
		for (size_t i = 0; i < n; i++)
		{
			buf[i] ^= hash;
		}

		if (total_size == 0)
		{
			// detech the format
			const char *format = detect_format(buf);
			printf("format is %s\n", format);
			char to_file_path[2000];
			snprintf(to_file_path, 2000, "%s.%s", to_file, format);
			printf("write to file '%s'\n", to_file_path);
			f_out = fopen(to_file_path, "w+b");
			if (f_out == NULL)
			{
				printf("failed to open write file");
				return -1;
			}
		}

		total_size += n;

		size_t wn = fwrite(buf, 1, n, f_out);
		// printf("write %zd bytes\n", wn);
		if (wn != n)
		{
			printf("no enought bytes write!");
			return -1;
		}
	}

	printf("total size: %zd\n", total_size);

	fclose(f);
	if (f_out)
		fclose(f_out);

	return total_size;
}

int main(int argc, char *argv[])
{
	printf("hello, cl\n");

	unsigned char hash = 104;

	const char *wechat_dat_file = "C:/Users/brian/Documents/WeChat Files/brianjcj/FileStorage/MsgAttach/2bc8f8e256fc8f293f4c127060a71def/Image/2023-02/3ad5640990150353912432709b2a5deb.dat";
	const char *out_file = "C:\\Users\\brian\\outout";

	int ret = decode_wechat_dat_file(wechat_dat_file, out_file, hash);
	printf("decode result(size): %d\n", ret);

	return 0;
}
