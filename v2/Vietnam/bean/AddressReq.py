class AddressReq:
    def __init__(self, address, city, postalCode, phone, countryCode):
        if address is not None:
            self.address = address
        if city is not None:
            self.city = city
        if postalCode is not None:
            self.postalCode = postalCode
        if phone is not None:
            self.phone = phone
        if countryCode is not None:
            self.countryCode = countryCode

    def print_info(self):
        print(f"{self.address} {self.city} {self.postalCode} {self.phone} {self.countryCode}")