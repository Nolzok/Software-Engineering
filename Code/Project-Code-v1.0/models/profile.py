class Profile:
    def __init__(self, name, email, phoneNumber, address, bio, friend_code, friends):
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address
        self.bio = bio
        self.friend_code = friend_code
        self.friends = friends

    def update_profile(self, name, email, phone, address, bio):
        self.name = name
        self.email = email
        self.phoneNumber = phone
        self.address = address
        self.bio = bio
