from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import language_tool_python


def check_writing_style(text):
    tool = language_tool_python.LanguageTool("id")
    matches = tool.check(text)

    errors = []
    for match in matches:
        if match.ruleId != "WHITESPACE_RULE":
            error = {
                "message": match.message,
                "context": match.context,
                "replacements": match.replacements,
            }
            errors.append(error)

    return errors


# Contoh penggunaan
text = "asuransi mobil yang bagus"
errors = check_writing_style(text)
if len(errors) > 0:
    print("Terdapat kesalahan dalam penulisan:")
    for error in errors:
        print(f"Kesalahan: {error['message']}")
        print(f"Konteks: {error['context']}")
        print(f"Rekomendasi: {', '.join(error['replacements'])}")
        print()
else:
    print("Tidak ditemukan kesalahan dalam penulisan.")
