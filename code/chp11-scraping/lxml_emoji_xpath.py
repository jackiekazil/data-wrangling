from lxml import html

page = html.parse('http://www.emoji-cheat-sheet.com/')

proper_headers = page.xpath('//h2|//h3')
proper_lists = page.xpath('//ul')

all_emoji = []

for header, list_cont in zip(proper_headers, proper_lists):
    section = header.text
    for li in list_cont.getchildren():
        emoji_dict = {}
        spans = li.xpath('div/span')
        if len(spans):
            link = spans[0].get('data-src')
            if link:
                emoji_dict['emoji_link'] = li.base_url + link
            else:
                emoji_dict['emoji_link'] = None
            emoji_dict['emoji_handle'] = spans[1].text_content()
        else:
            emoji_dict['emoji_link'] = None
            emoji_dict['emoji_handle'] = li.xpath('div')[0].text_content()
        emoji_dict['section'] = section
        all_emoji.append(emoji_dict)

print all_emoji
