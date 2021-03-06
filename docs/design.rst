Design and Goals
================

Use Cases for the Design
------------------------

Use Case: Crash Reports
^^^^^^^^^^^^^^^^^^^^^^^

The initial use for this format was the secure storage of crash reports containing sensitive customer data. Because these crash reports where for performance/availability reasons collected by an internet connected system, any data exposure had to be prevented by design. The crash reports were in some cases large, therefore the encryption had to be done *while* receiving the files.

After transferring the crash reports to a server inside the company network, they were decoded using the private key which was stored in the HSM, processed and stored in a database.

Use Case: User Data Encryption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another use case is the storage of user related data in a secure way. For each user, an RSA key pair is generated and stored in the HSM attached to the server. The public key is stored in the database of the receiving server. Any userdata is automatically encrypted using the public key, before it is stored at the storage location.

In case of a breach, the attacker can only copy the encrypted data, but not the private keys which are required to access the data. An offline decryption after a data leak is prevented by this approach. The only way to access the data would be by running own code on the server which is processing the data - which is by definition not impossible, but much harder to do unnoticed.

Searching or decoding large amounts of random amounts of data on these servers would generate alerts. Slowing down these operations would help to stay unnoticed, but would also be impractical.


Goals
-----

Archive Data
^^^^^^^^^^^^

This file encryption format was designed to archive/store data in a securely encrypted format on servers where a breach cannot be confidentially excluded. The format allows automatic processes to efficiently encrypt and store received files using a locally stored public key.

Ease of Use
^^^^^^^^^^^

Proper encryption is difficult, so it is if often done wrong. The algorithms for the encryption used in this format are chosen carefully in a way to allow the best protection of the files.

Intentionally, there are no choices of encryption strength, algorithms, key-sizes and such. This library shall be safe out of the box and allow no accidentally weakening of the encryption.

In case any problems with the used algorithms are uncovered, the format shall be updated to automatically use the better and improved algorithms while providing backward compatibility for the *decryption* process.

Minimal Dependencies
^^^^^^^^^^^^^^^^^^^^

Too many dependencies can be a huge risk. Therefore, this library only depends on ``cryptography``, a well established and maintained crypto library based on OpenSSL.

Large Files
^^^^^^^^^^^

The file format is designed in a way, to efficiently encrypt large files, if the size of the source file is known. The order of the blocks is arranged in a way, to allow combining hashing and encryption over the source file, without the need to read the same data twice.

Encrypting while streaming large amounts of data is also supported. This allows to encrypt data in memory while reading it from e.g. a network source and also stream it to a storage provider.

Separate Metadata Block
^^^^^^^^^^^^^^^^^^^^^^^

A custom block of metadata allows to store all details of the original file and any important context data. The metadata is stored in a separate block. Therefore, it is possible to quickly extract just the metadata from the file.

Prevention of Data Loss/Theft on Breach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If there is a breach on the encrypting server, the already encrypted files are safe, even the stored public key is copied. The private key to decrypt the data is stored outside the server environment and therefore not accessible for the attacker.

By including a hash for the encrypting public key, this key can be changed on a time or even file basis. In case of data breaches, where the attacker will create a copy of the data with the goal to obtain the private key with a later attack, this will further limit the exposure. By using a time based rotation scheme, where e.g. every month a new kay pair is generated and older keys are stored in an offline location.

Protection from Data Corruption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A SHA3-512 checksum is created for the metadata, the file data and the whole file. These checksums allow scanning the files for any data corruption.

While the checksums for the metadata block and file data are encrypted, the checksum for the whole file is stored unencrypted and allows quick checks for file corruption.


Non-Goals
---------

Multiple Keys / Trust Networks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This library or file format is not intended to be a replacement for tools like PGP/GPG, where files can be encrypted with multiple public keys. It is meant to work automatically as part of a server process or application.

Protection from Maliciously Manipulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While the files use checksums to detect any data corruptions, these checksums are not signed with a private key. Therefore, there is a *slim* chance the file can be manipulated in a way which can not be detected.

If an attacker gains access to a server, it will also gain access to the public key and is able to encrypt arbitrary files - which makes manipulating existing files easy, by just replacing them.

The checksums for the metadata and file data are encrypted with the same symmetric key to prevent guesses/comparison about the contents of the encrypted data. This encryption provides a protection about bit-flip attacks on the AES-CBC encrypted data - but it is only detected after encrypting the data using the private key.


Used Algorithms and Hashes
--------------------------

The used encryption is strong, open and well established:

- For the key pairs, RSA 4096 keys are used.
- The symmetric key is encrypted using the RSA public key, using OAEP.
- OAEP us used with MGF1 with SHA256.
- For the actual data encryption, AES-256/CBC is used with random keys and IVs.
- An SHA3-512 digest are used to verify the integrity of the metadata and data.
- The metadata, data and the digests are encrypted with an individual random IV.
- The file digest is not encrypted to easily check for data corruption.

File Sizes
----------

By design, the format was made for files in a range of megabytes up to several terabytes.

Encrypting a large amount of small files generates lots of additional data. In these cases, consider collecting these files into a container (e.g. ZIP container) first, then encrypt this container.

Files up to 10 TB should prove no problem, as the used AES-256/CBC encryption is efficient and fast.

There is an *arbitrary limit* for files greater than 10 TB. This limit is set to have a reasonable limit to verify the file integrity. Technically, the limit is at 18 Exabyte, because a 64bit value is used to store the size.

