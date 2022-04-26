from ensurepip import version
import qrcode
import qrcode.image.svg



class info:
    def __init__(self,pemesan,option,qty,price) -> None:
        self.pemesan = pemesan
        self.option = option
        self.qty = qty
        self.price = price

    def create_qr(self):
        name = "creator: " + str(self.pemesan)+", option: " + str(self.option) + ", qty: "+ str(self.qty) +  ", price: " + str(self.price)
        qr = qrcode.QRCode(
            version = 1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size = 10,
            border = 4,
        )
        qr.add_data(name)
        qr.make(fit=True)
        image = qr.make_image(fill_color="black",back_color="white")
        return image
    
information = info("Pandu",2,3,10000)
img = information.create_qr()

img.save('qr.png',format="png")