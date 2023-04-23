import collections

# XOR encryption function
def xor_encrypt(plaintext, key):
    ciphertext = ""
    # Iterate through the plaintext characters
    for i, c in enumerate(plaintext):
        # Encrypt the character by XORing it with the corresponding key character
        # (wrap around the key if it"s shorter than the plaintext)
        ciphertext += chr(ord(c) ^ ord(key[i % len(key)]))
    return ciphertext

# XOR decryption function (uses the same logic as encryption)
def xor_decrypt(ciphertext, key):
    return xor_encrypt(ciphertext, key)

# Function to estimate the key length used in an XOR cipher using the autocorrelation method
def estimate_key_length(ciphertext, min_key_length=2, max_key_length=None):
    # If the maximum key length is not specified, set it to half of the ciphertext length
    # as a reasonable upper limit for key lengths to consider
    if max_key_length is None:
        max_key_length = len(ciphertext) // 2

    # Initialize variables to store the best key length found so far and its correlation
    best_key_length = 0
    best_correlation = -1

    # Iterate through possible key lengths from the minimum to the maximum key length
    for key_length in range(min_key_length, max_key_length + 1):
        correlation = 0

        # Iterate through the ciphertext, comparing characters at positions i and i + key_length
        # to calculate the similarity between the original ciphertext and the shifted ciphertext
        for i in range(len(ciphertext) - key_length):
            # If the characters at positions i and i + key_length are the same, increment the correlation
            if ciphertext[i] == ciphertext[i + key_length]:
                correlation += 1

        # Normalize the correlation by dividing it by the number of character comparisons made
        # This ensures that key lengths with more comparisons don"t have an unfair advantage
        correlation /= (len(ciphertext) - key_length)

        # If the current correlation is higher than the best correlation found so far,
        # update the best key length and the best correlation
        if correlation > best_correlation:
            best_correlation = correlation
            best_key_length = key_length

    # Return the best key length found during the iteration
    return best_key_length

# Function to break the XOR cipher by brute-forcing the most common character
def break_xor_cipher(ciphertext, plaintext_alphabet, min_key_length=2, max_key_length=None):
    # Estimate the key length
    key_length = estimate_key_length(ciphertext, min_key_length=min_key_length,
                                     max_key_length=max_key_length)
    key = ""

    # Iterate through the key positions
    for i in range(key_length):
        # Create a block containing every i-th character from the ciphertext
        block = ciphertext[i::key_length]
        # Calculate the frequency of each character in the block
        freqs = collections.Counter(block)
        # Find the most common character in the block
        most_common = freqs.most_common(1)[0][0]

        best_score = -1
        best_key_char = ""

        # Iterate through the characters in the plaintext alphabet
        for char in plaintext_alphabet:
            # Guess the key character by XORing the most common character with the current character
            guessed_key = ord(most_common) ^ ord(char)
            # Decrypt the block using the guessed key character
            plaintext_candidate = xor_decrypt(block, chr(guessed_key))

            # Calculate the frequency of each character in the candidate plaintext
            candidate_freqs = collections.Counter(plaintext_candidate)

            # Calculate the score based on the frequency of characters in the plaintext alphabet
            score = sum(candidate_freqs[c] for c in plaintext_alphabet)

            # Penalize the score for characters not in the plaintext_alphabet
            score -= sum(candidate_freqs[c] for c in candidate_freqs if c not in plaintext_alphabet)

            # Update the best key character and score if the current score is higher
            if score > best_score:
                best_score = score
                best_key_char = chr(guessed_key)

        # Append the best key character to the key
        key += best_key_char

    # Decrypt the ciphertext using the recovered key
    plaintext = xor_decrypt(ciphertext, key)
    return plaintext, key

min_key_length = 2
max_key_length = 16
key = "qwertzuiop"
plaintext_alphabet = "abcdefghijklmnopqrstuvwxyz "
plaintext = "lorem ipsum dolor sit amet consectetur adipiscing elit vivamus nec imperdiet dolor id convallis lectus etiam nec facilisis ligula a accumsan dolor cras feugiat ante augue ut porta in urna sed gravida cras scelerisque sed turpis sed maximus nam euismod eros sit amet mattis suscipit etiam nulla lorem lobortis a magna vel dapibus hendrerit magna suspendisse bibendum purus sed accumsan vestibulum urna nulla consectetur libero nec ultricies quam diam sit amet metus ut ut semper nisi integer dui nisl bibendum eget elementum eget vulputate sit amet odio morbi sollicitudin neque nec commodo vestibulum vivamus mattis porta sodales sed mollis lobortis maximus"

ciphertext = xor_encrypt(plaintext, key)
print("Ciphertext:", ciphertext.encode("utf-8"))

decrypted_text, recovered_key = break_xor_cipher(ciphertext, plaintext_alphabet, min_key_length, max_key_length)
print("Decrypted text:", decrypted_text)
print("Recovered key:", recovered_key)

