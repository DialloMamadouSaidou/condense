
class file_verify:
    def __init__(self, image, video, document):
        self.image = image
        self.video = video
        self.document = document
        self.message_error = {}


    def verifie_image(self):
        terminaison_image = ['jpg', 'jpeg', 'png']
        termine = self.image.split('.')[-1]
        if not termine in terminaison_image:
            self.message_error['imageF'] = "Le format dimage nest pas respecté!"
        return self.message_error

    def verifie_video(self):
        terminaison_video = ['mp4', 'avi']
        termine = self.video.split('.')[-1]
        if not termine in terminaison_video:
            self.message_error["videoF"] = "Le format de video nest pas respecté!"
            #return self.message_error
        return self.message_error
    def verifie_document(self):
        terminaison_document = ['pdf', 'docx', 'odt', 'txt', 'tar']
        termine = self.document.split('.')[-1]
        if not termine in terminaison_document:
            self.message_error["docF"] = "Le format de document nest pas respecté!"
        return self.message_error

    def general(self):
        self.verifie_image()
        self.verifie_video()
        self.verifie_document()
        return self.message_error

    def __str__(self):
        return f"limage est {self.image}, la video est {self.video}, le document est {self.document}"

if __name__=="__main__":
    context = {}
    verifie = file_verify('saiou.pnga', 'said.mp4', 'saidou.pdf')
    context = verifie.general()
    print(len(context))