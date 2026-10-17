import unittest
from agent import submission_payload, validate_result


def result(task_id="a", answer="42"):
    return dict(task_id=task_id, answer=answer, confidence=0.8, sources=[], limitations="")


class SubmissionTests(unittest.TestCase):
    def test_complete_payload_and_trim(self):
        payload = submission_payload([{"task_id": "a"}], [result(answer=" 42\n")],
                                     "test", "https://huggingface.co/spaces/test/agent/tree/main")
        self.assertEqual(payload["answers"], [{"task_id": "a", "submitted_answer": "42"}])

    def test_reject_missing_duplicate_or_extra(self):
        for rows in ([], [result(), result()], [result("b")]):
            with self.assertRaises(ValueError):
                submission_payload([{"task_id": "a"}], rows, "test",
                                   "https://huggingface.co/spaces/test/agent/tree/main")

    def test_reject_other_identity_source(self):
        with self.assertRaises(ValueError):
            submission_payload([{"task_id": "a"}], [result()], "test",
                               "https://huggingface.co/spaces/someone/agent/tree/main")

    def test_reject_invalid_model_output(self):
        for value in ({}, result(answer=42), {**result(), "confidence": 2}):
            with self.assertRaises(ValueError):
                validate_result(value)


if __name__ == "__main__":
    unittest.main()
