class Comment:
    def __init__(self, over, description):
        self.over = over
        self.description = description
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __repr__(self):
        # return str(self.__dict__)
        return "over : {}, desc : {}, paras : {}".format(self.over, self.description, self.paragraphs)
