from typing import List

import pytest

from main import BowlingScorer


def test_vanilla_bowling_score():
    bowling_scorer = BowlingScorer()
    assert bowling_scorer.total_score == 0


@pytest.mark.parametrize("score", [1, 2, 3, 4, 5])
def test_first_try(score):
    bowling_scorer = BowlingScorer()
    bowling_scorer.add_try(score)
    assert bowling_scorer.total_score == score


@pytest.mark.parametrize(
    "score, second_score", [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5)]
)
def test_second_try(score: int, second_score: int):
    bowling_scorer = BowlingScorer()
    bowling_scorer.add_try(score)
    bowling_scorer.add_try(second_score)
    assert bowling_scorer.total_score == 10


@pytest.mark.parametrize(
    "scores", [[1, 9, 1], [2, 8, 1], [3, 7, 1], [4, 6, 1], [5, 5, 1]]
)
def test_bowling_score_first_spare_then_less_than_ten(scores: List[int]):
    bowling_scorer = BowlingScorer()
    for score in scores:
        bowling_scorer.add_try(score)
        print(bowling_scorer.total_score)
    assert bowling_scorer.total_score == 12


@pytest.mark.parametrize(
    "score, second_score", [(10, 9), (10, 8), (10, 7), (10, 6), (10, 5)]
)
def test_bowling_score_first_strike_then_less_than_ten(score: int, second_score: int):
    bowling_scorer = BowlingScorer()
    bowling_scorer.add_try(score)
    print(bowling_scorer.total_score)
    bowling_scorer.add_try(second_score)
    print(bowling_scorer.total_score)
    print(bowling_scorer.frames)
    assert bowling_scorer.total_score == score + second_score * 2


@pytest.mark.parametrize(
    "scores, expected_total",
    (
        [
            (
                [9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0],
                90,
            ),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0], 240),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0], 270),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 0], 288),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0], 290),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 300),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 0], 267),
            ([10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 1, 9], 278),
        ]
    ),
)
def test_game_final_set(scores: List[int], expected_total):
    bowling_scorer = BowlingScorer()
    for score in scores:
        bowling_scorer.add_try(score)
        print(bowling_scorer.previous_try.frame_score)

    assert bowling_scorer.total_score == expected_total


@pytest.mark.parametrize(
    "scores, expected_total",
    ([([1, 9, 10, 10, 9], 87), ([1, 9, 10, 10, 9, 1, 10], 110)]),
)
def test_bowling_spare_then_strike_then_strike(scores: List[int], expected_total):
    bowling_scorer = BowlingScorer()
    for score in scores:
        bowling_scorer.add_try(score)
        print(bowling_scorer.total_score)
        print(bowling_scorer.previous_try.is_spare)

    assert bowling_scorer.total_score == expected_total
