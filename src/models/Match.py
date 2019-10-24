class Match:
    def __init__(self, first_team, second_team, first_team_score, second_team_score):
        self.first_team = first_team
        self.second_team = second_team
        self.first_team_score = first_team_score
        self.second_team_score = second_team_score
        self.commentary = []

    def __repr__(self):
        return str(self.__dict__)
        