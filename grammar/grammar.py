from language_tool import LanguageTool


def check_spelling(sentence):
    # Inisialisasi objek LanguageTool untuk bahasa Inggris
    tool = LanguageTool("en-US")

    # Memeriksa ejaan dalam kalimat
    matches = tool.check(sentence)

    # Menampilkan kesalahan ejaan
    if len(matches) > 0:
        print("Kesalahan ejaan ditemukan:")
        for match in matches:
            print("Pada posisi", match.offset, ":", match.message)
    else:
        print("Tidak ada kesalahan ejaan.")


# Contoh pemanggilan fungsi
kalimat = "I like to reed buks."
check_spelling(kalimat)


# Contoh pemanggilan fungsi
kalimat = "I like to reed buks."
check_spelling(kalimat)
