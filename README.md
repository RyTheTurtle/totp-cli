# totp-cli
CLI interface that generates RFC6238 valid OTP codes. Purpose is to learn and understand how time based one-time passwords are generated for 2FA applications. 

## Usage 
```python totp.py <secretKey>```

```secretKey``` should be a base32 encoded sequence of bytes. Refer to the [RFC](https://www.rfc-editor.org/rfc/rfc6238) for more details 