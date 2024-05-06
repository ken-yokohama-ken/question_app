import streamlit as st
import math
from functools import lru_cache
from pandas import DataFrame

from ExcelLoader import ExcelLoader
from QuestionDataHandler import QuestionDataHandler


def next_page():
    st.session_state.page += 1


def previous_page():
    st.session_state.page -= 1
    if st.session_state.page < 0:
        st.session_state.page = 0


def restart():
    st.session_state.page = 0


class Visualization():

    def __init__(self, excel_loader: ExcelLoader, config: list) -> None:
        """ constructor

        Args:
            excel_loader (ExcelLoader): excel loader, which has to be loaded
            config (list): configuration, which has to be loaded
        """

        self.excel_loader: ExcelLoader = excel_loader
        self.config: list = config
        self.excel_id: int = 0

        # preload keys, which frequently use in this class
        self.title_key: str = config["data_structure"]["title_key"]
        self.question_key: str = config["data_structure"]["question_key"]
        self.answer_key: str = config["data_structure"]["answer_key"]
        self.solution_key: str = config["data_structure"]["solution_key"]
        self.candidate_key: str = config["data_structure"]["candidate_key"]

    @lru_cache(maxsize=1)
    def _get_current_question(self, excel_id: int, question_id: int) -> DataFrame | None:
        """ get the current question data

        Args:
            excel_id (int): excel id
            question_id (int): question id

        Returns:
            DataFrame | None: a partial question data
        """

        data_frame = self.excel_loader.get_data_frame(excel_id)
        if data_frame is None:
            return None

        return data_frame.iloc[question_id]

    @lru_cache(maxsize=1)
    def _get_question_num(self, excel_id: int) -> int:
        """ get question num
        Args:
            excel_id (int): excel id

        Returns:
            int: the number of questions
        """

        data_frame = self.excel_loader.get_data_frame(excel_id)
        if data_frame is None:
            return None

        return len(data_frame.index)

    def _get_score(self, excel_id: int) -> float:

        correct_num = 0
        for i, input in enumerate(st.session_state.input_list):

            # get question data
            question_data = self._get_current_question(excel_id, i)
            if QuestionDataHandler.ConfirmAnswer(question_data, self.answer_key, input):
                correct_num += 1

        return math.floor(float(correct_num) * 100 / float(len(st.session_state.input_list)))

    def _refresh_all(self):
        st.session_state.input_list = []

    def _draw_question(self, question_data: DataFrame):

        # draw title
        st.write("# " + str(question_data[self.title_key]))
        # draw question
        st.write(str(question_data[self.question_key]))

    def _draw_candidates(self, question_data: DataFrame, question_id: int):

        # get candidates
        candidate_list = QuestionDataHandler.GetCandidateList(question_data, self.candidate_key)
        # draw candidates
        st.session_state.input_list[question_id] = st.radio(label="", options=candidate_list)

    def _draw_buttons(self, question_data: DataFrame, input: str):

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            # with placeholder.container():
            if st.button("確認"):

                # check if the answer is right
                if QuestionDataHandler.ConfirmAnswer(question_data, self.answer_key, input):

                    # display True
                    st.toast("正解❤️")
                else:

                    # display False
                    st.toast("不正解😢")
        with col2:
            st.button("前へ", on_click=previous_page)
        with col3:
            st.button("次へ", on_click=next_page)

    def _draw_progress_bars(self, question_num: int, question_id: int):

        st.progress(float(question_id) / float(question_num), text="現在の問題/全問題")

    def _draw_final(self, excel_id: int):

        if st.button("採点"):
            score = self._get_score(excel_id)
            st.info(str(score) + "点です")

        st.button("初めに戻る", on_click=restart)

    def _draw_side_bars(self):

        st.sidebar.write("pages")

        for i in range(self.excel_loader.get_file_num()):

            if st.sidebar.button(self.excel_loader.excel_file_list[i].stem):
                self.excel_id = i
                st.session_state.input_list = []

    def visualize(self):

        if "page" not in st.session_state:
            st.session_state.page = 0

        if "input_list" not in st.session_state:
            st.session_state.input_list = []

        question_num = self._get_question_num(self.excel_id)
        if len(st.session_state.input_list) == 0:
            st.session_state.input_list = [""] * question_num
            
        self._draw_side_bars()

        if st.session_state.page < question_num:

            question_data = self._get_current_question(self.excel_id, st.session_state.page)
            # draw progress bars
            self._draw_progress_bars(question_num, st.session_state.page)
            # draw question
            self._draw_question(question_data)
            # draw candidates
            self._draw_candidates(question_data, st.session_state.page)
            # draw buttons
            self._draw_buttons(question_data, st.session_state.input_list[st.session_state.page])

        else:
            self._draw_final(self.excel_id)
