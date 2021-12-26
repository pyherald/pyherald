title: Preventing Unicode-related Gotchas
authors: paul_mcguire
note: Mail by Paul McGuire
source: https://mail.python.org/archives/list/python-dev@python.org/message/GBLXJ2ZTIMLBD2MJQ4VDNUKFFTPPIIMO/
tags: unicode
slug: ---



As part of working on the next edition of “Python in a Nutshell” with Steve, Alex Martelli, and Anna Ravencroft, Alex suggested that I add a cautionary section on homoglyphs, specifically citing “`A`” (LATIN CAPITAL LETTER A) and “`Α`” (GREEK CAPITAL LETTER ALPHA) as an example problem pair. I wanted to look a little further at the use of characters in identifiers beyond the standard 7-bit ASCII, and so I found some of these same issues dealing with Unicode NFKC normalization. The first discovery was the overlapping normalization of “`ªº`” with “`ao`”. This was quite a shock to me, since I assumed that the inclusion of Unicode for identifier characters would preserve the uniqueness of the different code points. Even ligatures can be used, and will overlap with their multi-character ASCII forms. So we have added a second note in the upcoming edition on the risks of using these “homonorms” (which is a word I just made up for the occasion).

To explore the extreme case, I wrote a pyparsing transformer to convert identifiers in a body of Python source to mixed font, equivalent to the original source after NFKC normalization. Here are hello.py, and a snippet from unittest/utils.py:


```
def 𝚑𝓮𝖑𝒍𝑜():

	try:

		𝔥e𝗅𝕝𝚘︴ = "Hello"

		𝕨𝔬r𝓵ᵈ﹎ = "World"

		ᵖ𝖗𝐢𝘯𝓽(f"{𝗵ｅ𝓵𝔩º_}, {𝖜ₒ𝒓lⅆ︴}!")

	except 𝓣𝕪ᵖｅ𝖤𝗿ᵣ𝖔𝚛 as ⅇ𝗑c:

		𝒑rℹₙₜ("failed: {}".𝕗𝗼ʳᵐªｔ(ᵉ𝐱𝓬))

if _︴ⁿ𝓪𝑚𝕖__ == "__main__":

	𝒉eℓˡ𝗈()

# snippet from unittest/util.py

_𝓟Ⅼ𝖠𝙲𝗘ℋ𝒪Lᴰ𝑬𝕽﹏𝕷𝔼𝗡 = 12

def _𝔰ʰ𝓸ʳ𝕥𝙚𝑛(𝔰, p𝑟𝔢ﬁ𝖝𝕝𝚎𝑛, ｓᵤ𝑓𝗳𝗂𝑥𝗹ₑ𝚗):

	ˢ𝗸ｉ𝗽 = 𝐥ｅ𝘯(𝖘) - ｐr𝚎𝖋𝐢x𝗅ᵉ𝓷 - 𝒔𝙪ﬀｉ𝘅𝗹𝙚ₙ

	if sｋi𝘱 > _𝐏𝗟𝖠𝘊𝙴H𝕺Ｌ𝕯𝙀𝘙﹏L𝔈𝒩:

		𝘴 = '%s[%d chars]%s' % (𝙨[:𝘱𝐫𝕖𝑓𝕚ｘℓ𝒆𝕟], ₛ𝚔𝒊p, 𝓼[𝓁𝒆𝖓(𝚜) - 𝙨𝚞𝒇ﬁx𝙡ᵉ𝘯:])

	return ₛ

```

You should able to paste these into your local UTF-8-aware editor or IDE and execute them as-is.

(If this doesn’t come through, you can also see this as a GitHub gist at Hello, World rendered in a variety of Unicode characters (github.com) https://gist.github.com/ptmcg/bf35d5ada416080d481d789988b6b466 . I have a second gist containing the transformer, but it is still a private gist atm.)

Some other discoveries:

“`·`” (ASCII 183) is a valid identifier body character, making “`_···`” a valid Python identifier. This could actually be another security attack point, in which “`s·join(‘x’)`” could be easily misread as “`s.join(‘x’)`”, but would actually be a call to potentially malicious method “`s·join`”.

“`_`” seems to be a special case for normalization. Only the ASCII “`_`” character is valid as a leading identifier character; the Unicode characters that normalize to “`_`” (any of the characters in “`︳︴﹍﹎﹏＿`”) can only be used as identifier body characters. “`︳`” especially could be misread as “`|`” followed by a space, when it actually normalizes to “`_`”.

Potential beneficial uses:

I am considering taking my transformer code and experimenting with an orthogonal approach to syntax highlighting, using Unicode groups instead of colors. Module names using characters from one group, builtins from another, program variables from another, maybe distinguish local from global variables. Colorizing has always been an obvious syntax highlight feature, but is an accessibility issue for those with difficulty distinguishing colors. Unlike the “ransom note” code above, code highlighted in this way might even be quite pleasing to the eye.

-- Paul McGuire