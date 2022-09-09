# secret-key-vals

Store encrypted key-value pairs

![Animation](https://user-images.githubusercontent.com/56612310/189370734-0d816f85-ebbe-4751-8cf3-96cd354e0992.gif)



## Install

```
pip install git+https://github.com/alancampag/secret-key-vals
```

## Disclaimer

Your master password is never stored and there is no password recovery functionality. The first password provided, via environment variable or cli, will be used to generate the encryption key. Losing that password means every secret is unrecoverable.

Interacting with the application using the wrong master password is also not possible. To reset the entire application remove the ~/.skv/secrets.json file, that will delete every stored secret so only do it if really necessary.


## Getting started

#### Configuring environment
Set the master password as an environment variable:
```
export SECRETKV_MASTERPASS=<your-master-password>
```
Optionally you can provide extra configuration values with:
```
export SECRETKV_SEED=<your-random-seed>
export SECRETKV_TAG=<your-random-tag>
```
More on what these values mean on the [How it works](#how-it-works) section.

#### Setting a value
```
skv set gmail 123456
```
If you don't want to set the environment variable, you use the `-p` option with the cli:
```
skv set gmail 123456 -p <your-master-password>
```
If the password isn't provided in any way, you will be prompted for it.

#### Getting a value
```
skv get gmail
```
```
{
  "values": [
    "123456"
  ]
}
```
If you set an existing key you can still retrieve old value with `--history`
```
skv set amazon 123456
skv set amazon abcdef
skv get amazon --history
```
```
{
  "values": [
    "abcdef",
    "123456"
  ]
}

```
#### Deleting values
```
skv delete gmail
```
Deleting actually only sets value to null and hides it from listing, you can still retrieve it with `--history`
```
skv get gmail --history
```
```
{
  "values": [
    null,
    "123456"
  ]
}
```

#### Listing keys
```
skv list
```
```
{
  "keys": [
    "amazon"
  ]
}
```
If you want listing to include deleted keys use `--all`:
```
skv list --all
```
```
{
  "keys": [
    "gmail",
    "amazon"
  ]
}
```

#### Dumping and Restoring
These features have not been implemented yet.

## Usage

```
usage: skv [-h]  ...

optional arguments:
  -h, --help  show this help message and exit

subcommmands:
  
    list      list every key
    get       get secret
    set       set secret
    delete    delete secret
    dump      dump all secrets
    restore   restore from dump file
```

## How it works

The encryption key is derived from the master password using PBKDF2, to make the derivation deterministic a seed value is required. You can provide your own random seed using the `SECRETKV_SEED` environment variable. The PBKDF2 will take the last 16 bits of the sha256 hash of the seed as its salt value. If no seed is provided the master password will be reused as seed.

Both keys and values are encrypted using AES in CBC mode with a 128-bit key. Keys are used to index the values, so they need to be encrypted in a deterministic way, the first 16 bytes of the seed are used as the IV for the CBC cipher. The actual secret values are encrypted with a different random IV every time.

All encrypted messages are authenticated with HMAC using SHA256, that guarantees decryption only succeeds with the correct key.

Neither the key nor the master password are ever stored on disk, not even their hashes. The first time a master password is provided a sample value is encrypted and stored, every time after that the password is validated by trying to decrypt that sample value, since messages are authenticated if decryption is successful we can be sure the key is correct.

The sample value used for validation is called a tag and isn't allowed to be used as a regular key. By default, its value is hardcoded uuid `03d39895-5416-4db5-b743-e10c94e4227c`. You can provide your own tag value using the environment variable `SECRETKV_TAG`.
