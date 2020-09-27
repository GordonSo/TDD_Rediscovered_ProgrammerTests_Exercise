from typing import List, Optional


class Frame(List[int]):

    def __init__(self):
        super().__init__()
        self._next_frame: Optional["Frame"] = None

    is_last: bool = False

    @property
    def next_frame(self) -> "Frame":
        return self._next_frame or Frame()

    @next_frame.setter
    def next_frame(self, frame: "Frame") -> None:
        self._next_frame = frame

    @property
    def is_strike(self) -> bool:
        if self.is_last:
            return self.first_try == 10
        return self.frame_score == 10 and len(self) == 1

    @property
    def is_second_strike(self) -> bool:
        if not self.is_last:
            return False

        return len(self) >= 2 and self[1] == 10

    @property
    def is_spare(self) -> bool:
        if self.is_last:
            return sum(self[:1]) == 10 and len(self) >= 2
        return self.frame_score == 10 and len(self) == 2

    @property
    def is_complete(self) -> bool:
        return self.frame_score == 10 or len(self) >= 2

    def add_score(self, score) -> "Frame":
        self.append(score)
        return self

    @property
    def first_try(self) -> int:
        return next(iter(self), 0)

    @property
    def frame_score(self) -> int:
        if not self:
            return 0
        return sum(self)

    @property
    def score(self) -> int:

        _frame_score = self.frame_score
        if self.is_last:
            return sum(self)

        if self.is_spare:
            if self.next_frame.is_last:
                return _frame_score + self.next_frame.first_try

            if self.next_frame.is_strike:
                return _frame_score + self.next_frame.frame_score + self.next_frame.next_frame.frame_score

            return _frame_score + self.next_frame.first_try

        if self.is_strike:
            if self.next_frame.is_last:
                return self.frame_score + sum(self.next_frame[:2])

            if self.next_frame.is_strike:
                if self.next_frame.next_frame.is_last:
                    return _frame_score + self.next_frame.frame_score + self.next_frame.next_frame.first_try

                return _frame_score + self.next_frame.frame_score + self.next_frame.next_frame.frame_score

            if self.next_frame.is_spare:

                return _frame_score + self.next_frame.frame_score

            return _frame_score + self.next_frame.frame_score

        return self.frame_score


class BowlingScorer:

    @property
    def total_score(self):
        return sum([frame.score for frame in self.frames])

    @property
    def previous_try(self) -> Optional[Frame]:
        return self.frames[-1] if self.frames else None

    def __init__(self):
        self.frames: List[Frame] = []

    def add_try(self, score: int) -> None:
        _previous_try = self.previous_try
        _is_last_frame = len(self.frames) == 10
        if (not _previous_try or _previous_try.is_complete) and not _is_last_frame:
            new_frame = Frame().add_score(score)

            if _previous_try:
                _previous_try.next_frame = new_frame

            self.frames.append(new_frame)
            if len(self.frames) == 10:
                new_frame.is_last = True

        else:
            _previous_try.add_score(score)
