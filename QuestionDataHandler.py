from pandas import DataFrame


class QuestionDataHandler():

    def __init__(self) -> None:
        return

    @staticmethod
    def GetCandidateNum(question_data: DataFrame, candidate_key: str) -> int:
        """ get candidate num

        Args:
            question_data (DataFrame): question data
            candidate_key (str): candidate key

        Returns:
            int: the number of candidates
        """

        count = 0
        candidate_num = 0
        while (True):

            if candidate_key + str(count) in question_data:
                candidate_num += 1
            else:
                break

            count += 1

        return candidate_num

    @staticmethod
    def GetCandidateList(question_data: DataFrame, candidate_key: str) -> list:
        """ get candidate list

        Args:
            question_data (DataFrame): question data
            candidate_key (str): candidate key

        Returns:
            list: list of candidates
        """

        # get candidates
        candidate_num = QuestionDataHandler.GetCandidateNum(question_data, candidate_key)

        candidate_list = []
        for i in range(0, candidate_num):

            key = candidate_key + str(i)
            candidate_list.append(question_data[key])

        return candidate_list

    @staticmethod
    def ConfirmAnswer(question_data: DataFrame, answer_key: str, input: int) -> bool:
        """ confirm answer

        Args:
            question_data (DataFrame): question data
            answer_key (str): key for answer
            input (int): input from gui

        Returns:
            bool: True: the input is right, False: the input is not right
        """

        # check answer
        if question_data[answer_key] == input:
            return True
        else:
            return False
