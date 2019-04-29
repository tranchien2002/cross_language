from google import google
import argparse
import translator
from google.cloud import translate
import six
# text = "Me llamoiletype"
# target ="eng"
# translate_client = translate.Client()
# if isinstance(text, six.binary_type):
#         text = text.decode('utf-8')
# result = translate_client.translate(text, target_language=target)
#
# print(result['translatedText'])
# translation= translator.translate("hello", dest="vi")
# print(translation.text)
# num_page = 3
search_results = google.search("The system uses an English-Vietnamese translation system filetype:pdf", num_page)
for result in search_results:
    print(result.link)

print(translator("xin chao", "en"))