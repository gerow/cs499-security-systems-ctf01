#!/bin/sh

# Create polyalphabetic
cat etc/decrypted/message_01.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_01.txt
cat etc/decrypted/message_02.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_02.txt
cat etc/decrypted/message_03.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_03.txt
cat etc/decrypted/message_04.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_04.txt
cat etc/decrypted/message_05.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_05.txt
cat etc/decrypted/message_06.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_06.txt
cat etc/decrypted/message_07.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_07.txt
cat etc/decrypted/message_08.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_08.txt
cat etc/decrypted/message_09.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_09.txt
cat etc/decrypted/message_10.txt | ./encdec_polyalphabetic.py e keys/pa.key > etc/pa_cracking/message_10.txt

# Create polygram
cat etc/decrypted/message_01.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_01.txt
cat etc/decrypted/message_02.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_02.txt
cat etc/decrypted/message_03.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_03.txt
cat etc/decrypted/message_04.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_04.txt
cat etc/decrypted/message_05.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_05.txt
cat etc/decrypted/message_06.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_06.txt
cat etc/decrypted/message_07.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_07.txt
cat etc/decrypted/message_08.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_08.txt
cat etc/decrypted/message_09.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_09.txt
cat etc/decrypted/message_10.txt | ./encdec_polygram.py e keys/pg.key > etc/pg_cracking/message_10.txt

# Create short polyalphabetic
cat etc/decrypted/message_01.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_01.txt
cat etc/decrypted/message_02.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_02.txt
cat etc/decrypted/message_03.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_03.txt
cat etc/decrypted/message_04.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_04.txt
cat etc/decrypted/message_05.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_05.txt
cat etc/decrypted/message_06.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_06.txt
cat etc/decrypted/message_07.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_07.txt
cat etc/decrypted/message_08.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_08.txt
cat etc/decrypted/message_09.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_09.txt
cat etc/decrypted/message_10.txt | ./encdec_polyalphabetic.py e keys/pa_short.key > etc/pa_short_cracking/message_10.txt
