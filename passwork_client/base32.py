class Base32:
    def __init__(self):
        """
        Base32 class with a custom alphabet
        """

        # custom alphabet for Base32 encoding/decoding
        self.alphabet = "0123456789abcdefghjkmnpqrtuvwxyz"

        # alias mapping for common character confusions
        self.alias = {"o": 0, "i": 1, "l": 1, "s": 5}

        # invert "alphabet"
        self.lookup = {char: index for index, char in enumerate(self.alphabet)}

        # splice in "alias"
        self.lookup.update(self.alias)

        self.encoder = self.Encoder(self)
        self.decoder = self.Decoder(self)

    class Encoder:
        def __init__(self, base32_instance):
            self.alphabet = base32_instance.alphabet
            self.bit_buffer, self.bit_count = 0, 0
            self.output = ""

        def reset(self):
            # resets the encoder"s state for a new encoding operation
            self.bit_buffer, self.bit_count = 0, 0
            self.output = ""

        def update(self, input_string):
            # converts input string to bytes and encodes it into Base32
            input_bytes = bytearray(input_string, "utf-8")
            for byte in input_bytes:
                # updates the bit buffer with the new byte and increments the bit count
                self.bit_buffer = (self.bit_buffer << 8) + byte
                self.bit_count += 8
                # encodes 5-bit groups into Base32 characters
                while self.bit_count >= 5:
                    self.output += self.alphabet[
                        (self.bit_buffer >> (self.bit_count - 5)) & 31
                    ]
                    self.bit_count -= 5
                    self.bit_buffer &= (1 << self.bit_count) - 1

        def finish(self):
            # handles any remaining bits by padding them on the right to form a complete character
            if self.bit_count > 0:
                self.output += self.alphabet[
                    (self.bit_buffer << (5 - self.bit_count)) & 31
                ]
            result = self.output
            self.reset()
            return result

    class Decoder:
        def __init__(self, base32_instance):
            self.lookup = base32_instance.lookup
            self.bit_buffer, self.bit_count = 0, 0
            self.output = bytearray()

        def reset(self):
            # resets the decoder"s state for a new decoding operation
            self.bit_buffer, self.bit_count = 0, 0
            self.output = bytearray()

        def update(self, input_string):
            # processes each Base32 character and decodes it back to the original bytes
            for char in input_string:
                # converts the Base32 character back to its original value using the lookup table
                value = self.lookup.get(char.lower())
                if value is None:
                    continue
                # updates the bit buffer with decoded bits and increments the bit count
                self.bit_buffer = (self.bit_buffer << 5) | value
                self.bit_count += 5
                # decodes into bytes once there are enough bits
                while self.bit_count >= 8:
                    self.output.append((self.bit_buffer >> (self.bit_count - 8)) & 0xFF)
                    self.bit_count -= 8
                    self.bit_buffer &= (1 << self.bit_count) - 1

        def finish(self):
            # decodes any remaining bits (if necessary) and resets the decoder
            # converts the bytearray to a UTF-8 string and returns it
            result = self.output.decode("utf-8")
            self.reset()
            return result

    def encode(self, input_string, finish=True):
        self.encoder.update(input_string)
        if finish:
            return self.encoder.finish()

    def decode(self, input_string, finish=True):
        self.decoder.update(input_string)
        if finish:
            return self.decoder.finish()


base32 = Base32()