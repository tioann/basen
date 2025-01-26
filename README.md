# Arbitrary base encoding

The initial idea for this project was to allow storing binary data to JSON as efficiently as possible. For example, common encodings like Base64 can be used for this but the data is expanded by 33.3%. By using the max number of available ASCII characters in a JSON string we can do better.

As per the RFC (http://www.ietf.org/rfc/rfc4627.txt) a JSON string may include almost every unicode character. We limit ourselves to ASCII because it's easier to argue about the encoding efficiency, so we can use all characters from space (char 32) up to tilde (`~` char 126) and excluding double quotes `"` and backslash `\`. This gives us a max of 93 characters to use for the encoding, which can be done by a simple conversion from base 256 (8-bit bytes) to base 93 and mapping of each of the 93 values to a distinct character and an "optimal" data expansion of only 22.3%

# Refinements and performance improvements

Converting large byte sequences to base 93 can be a slow, computationally expensive process, so we split large byte sequences to fixed length segments that we then convert to base 93 individually. This reduces the efficiency but we can minimize the loss by choosing an optimal length for the fragments and there is a method that does exactly that in the code.

Another issue with splitting into segments is how to deal with the last part that is typically not going to be of the exact segment length. The solution applied here is to simply convert the last part to base 93 regardless of size. As base 93 only encodes less than 8 bits in each character, the length of the encoded string will always correspond to a specific integer segment length so no length indicators or padding is needed.

There is nothing magical about the number 93. The exact same technique can be used for any number of encoding characters. This means that this code can sort of be used to simulate other popular encodings such as base16, base32, base64 and base58. This actually gives us the exact same results as the proper encoding under some conditions, for example we can get the exact same results as base64 encoding by specifying the right sequence of characters and setting a segment size of 3.

# Usage in the real world

baseN encoding is neat and does save space, but it is not really recommended for production use. It saves a significant space only for large enough byte sequences and it is quite slow for those sequences. So this is mostly useless but still a fun project :-)
