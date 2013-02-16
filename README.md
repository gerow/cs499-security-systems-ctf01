cs499-security-systems-ctf01
============================
Proposed roadmap:

I think our first goal should be to implement all the encryption and
decryption algorithms.  We can all inherit off a common
EncryptorDecryptor interface that might support methods like
set_key(key), encrypt(plaintext), decrypt(ciphertext), and
generate_key(args) which would generate a random key given some
arguments (like length).  Also, we should probably implement some kind
of dump_key() method that will return a string representation of the
key so that it can easily be shared between machines (this method
should also likely include information about the encryption type and
length).

After that we can think about how to actually attack these things.
One huge issue is how to tell when we've successfully decrypted
something.  We don't know what the original message is so we can't
just check against something, so we'll need some kind of function that
takes a string and checks how "correct" it looks.  An easy first step
for doing this would be to have a dictionary of all the english words
and determine what percentage of the words in the string qualify as
english words and return a number between 0 and 1 noting this. There
are also more sophisticated methods we might want to look into.

After that we should probably just implement some naive key cracking
algorithms for every case, just to make sure we can at least do
_something_ for each encryption type.  From then we can look into more
sophisticated ways of solving each method (likely going from the
easiest to solve to the hardest to solve).
